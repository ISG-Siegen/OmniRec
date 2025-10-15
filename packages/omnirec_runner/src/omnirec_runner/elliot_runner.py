import importlib
from os import path
from pathlib import Path
from typing import Any, Dict

import elliot.hyperoptimization as ho
import pandas as pd
import tensorflow as tf
import yaml
from elliot.dataset.dataset import DataSetLoader
from elliot.namespace.namespace_model_builder import NameSpaceBuilder
from elliot.utils import logging as el_logging

from omnirec_runner.runner import Runner

here = path.abspath(path.dirname(__file__))


class Elliot(Runner):
    def __init__(self) -> None:
        super().__init__()

    def setup_fit(self):
        self.convert_data()
        self.setup_elliot()

    def fit(self):
        self.model.train()

    def post_fit(self):
        if hasattr(self.model, "_model"):
            if isinstance(self.model._model, tf.keras.Model):
                checkpoint = tf.train.Checkpoint(model=self.model._model)
                model_file = self.checkpoint_dir / "model.ckpt"
                checkpoint.write(str(model_file.resolve()))
            else:
                model_file = self.checkpoint_dir / "model.pkl"
                self.model._model.save_weights(model_file)
        else:
            raise ValueError("_model attribute missing on elliot model object")

    def setup_predict(self):
        self.convert_data()
        self.setup_elliot()

        if hasattr(self.model, "_model"):
            if isinstance(self.model._model, tf.keras.Model):
                checkpoint = tf.train.Checkpoint(model=self.model._model)
                model_file = self.checkpoint_dir / "model.ckpt"
                checkpoint.restore(str(model_file.resolve())).expect_partial()
            else:
                model_file = self.checkpoint_dir / "model.pkl"
                self.model._model.load_weights(model_file)

    def predict(self) -> Dict[Any, Any]:
        recs = self.model.get_recommendations(
            self.model.evaluator.get_needed_recommendations()
        )

        recs = {
            int(key): [[int(t[0]) for t in value], [float(t[1]) for t in value]]
            for key, value in recs[0].items()
        }

        recs_df = pd.DataFrame(
            [
                (uid, item, score)
                for uid, (items, scores) in recs.items()
                for item, score in zip(items, scores)
            ],
            columns=["user", "item", "score"],
        )
        recs_df = recs_df.sort_values(["user", "score"], ascending=[True, False])
        if self.implicit_feedback:
            recs_df["rank"] = recs_df.groupby("user").cumcount() + 1
        else:
            recs_df = recs_df.rename(columns={"score": "rating"})

            # Rescale elliot scores to original rating range
            pred_min = recs_df["rating"].min()
            pred_max = recs_df["rating"].max()
            recs_df["rating"] = self.min_rating + (
                self.max_rating - self.min_rating
            ) * ((recs_df["rating"] - pred_min) / (pred_max - pred_min))

        recs_df.to_csv(
            "D:/Users/baumg/Documents/Uni/ISG/RecSysLib_TEST/el_recs.csv", index=False
        )

        return recs_df.to_dict(orient="list")

    def post_predict(self):
        pass

    def convert_data(self):
        self.train_file_tsv = self.train_file.with_suffix(".tsv")
        self.val_file_tsv = self.val_file.with_suffix(".tsv")
        self.test_file_tsv = self.test_file.with_suffix(".tsv")

        files = (
            (self.train_file, self.train_file_tsv),
            (self.val_file, self.val_file_tsv),
            (self.test_file, self.test_file_tsv),
        )

        min_list = []
        max_list = []

        for csv_file, tsv_file in files:
            df = pd.read_csv(csv_file)
            if "rating" in df.columns:
                min_list.append(df["rating"].min())
                max_list.append(df["rating"].max())

            # Ensure column order
            columns = ["user", "item"]
            for col in ("rating", "timestamp"):
                if col in df.columns:
                    columns.append(col)
            df = df[columns]

            df = df.rename(
                columns={
                    "user": "UserID",
                    "item": "ItemID",
                    "rating": "Rating",
                    "timestamp": "TimeStamp",
                }
            )
            df.to_csv(tsv_file, sep="\t", header=False, index=False)

        if len(min_list) == 3 and len(max_list) == 3:
            self.min_rating = min(min_list)
            self.max_rating = max(max_list)

    def setup_elliot(self):
        """Configures elliot and initializes the model in self.model"""
        has_configuration = True

        if self.algorithm_name in ["SlopeOne", "MostPop"]:
            has_configuration = False

        model: dict[str, dict[str, Any]] = {
            self.algorithm_name: {
                "meta": {"hyper_max_evals": 1, "save_recs": False},
            }
        }

        train_df = pd.read_csv(self.train_file)

        self.implicit_feedback = "rating" not in train_df.columns
        model[self.algorithm_name]["implicit"] = self.implicit_feedback

        if has_configuration:
            model[self.algorithm_name].update(self.algorithm_config)

        config_dict = {
            "experiment": {
                "dataset": f"{self.dataset_name}",
                "path_log_folder": str((self.checkpoint_dir / "elliot_logs").resolve()),
                "data_config": {
                    "strategy": "fixed",
                    "train_path": str(self.train_file_tsv.resolve()),
                    "valid_path": str(self.val_file_tsv.resolve()),
                    "test_path": str(self.test_file_tsv.resolve()),
                },
                "models": model,
                "evaluation": {"simple_metrics": ["nDCG"], "cutoffs": [10]},
                "top_k": 20,
            }
        }

        config_path = (
            self.tmp_dir / f"./elliot_{self.dataset_name}_{self.algorithm_name}.yaml"
        )

        with open(config_path, "w") as file:
            yaml.dump(config_dict, file, sort_keys=False, default_flow_style=False)

        builder = NameSpaceBuilder(
            config_path, here, path.abspath(path.dirname(config_path))
        )

        builder = NameSpaceBuilder(
            config_path, here, path.abspath(path.dirname(config_path))
        )

        base = builder.base
        base.base_namespace.evaluation.relevance_threshold = getattr(
            base.base_namespace.evaluation, "relevance_threshold", 0
        )

        dataloader = DataSetLoader(config=base.base_namespace)

        data_test_list = dataloader.generate_dataobjects()
        key, model_base = list(builder.models())[0]
        data_test = data_test_list[0]

        el_logging.init(
            Path(__file__).parent / "elliot_logger_config.yml",
            base.base_namespace.path_log_folder,
        )
        el_logging.prepare_logger(key, base.base_namespace.path_log_folder)

        model_class = getattr(importlib.import_module("elliot.recommender"), key)
        model_placeholder = ho.ModelCoordinator(
            data_test, base.base_namespace, model_base, model_class, 0
        )

        self.model = model_placeholder.model_class(
            data=model_placeholder.data_objs[0],
            config=model_placeholder.base,
            params=model_placeholder.params,
        )


if __name__ == "__main__":
    Elliot.main()
