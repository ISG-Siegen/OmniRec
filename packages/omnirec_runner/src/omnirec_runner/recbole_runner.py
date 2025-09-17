import os
from typing import Any

import numpy as np
import pandas as pd
from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from recbole.quick_start import load_data_and_model
from recbole.trainer.trainer import Trainer
from recbole.utils import ModelType, get_model, get_trainer, init_logger, init_seed
from recbole.utils.case_study import full_sort_topk

from omnirec_runner.runner import Runner


class RecBole(Runner):
    def __init__(self) -> None:
        super().__init__()

    def setup_fit(self):
        # RecBole drops tensorboard logs in CWD
        os.chdir(self.checkpoint_dir)

        config_dict = {
            "seed": 42,  # default: "2020" # TODO: Random state propagation
            # "data_path": "./data_sets/", will be set below  # default: "dataset/"
            "checkpoint_dir": self.checkpoint_dir,  # default: "saved/"
            "log_wandb": False,  # default: False
            # "wandb_project": f"{data_set_name} @ {algorithm_name}",  # default: "recbole"
            "benchmark_filename": ["train", "val", "test"],
            # default: None
            "field_separator": ",",  # default: "\t"
            "epochs": 200,  # default: 300
            "train_batch_size": 1024,  # default: 2048
            "learner": "adam",  # default: "adam"
            "learning_rate": 0.01,  # default: 0.001
            "training_neg_sample_args": {
                "distribution": "uniform",  # default: "uniform"
                "sample_num": 1,  # default: 1
                "dynamic": False,  # default: False
                "candidate_num": 0,  # default: 0
            },
            "eval_step": 5,  # default: 1
            "stopping_step": 5,  # default: 10
            "weight_decay": 0.0,  # default: 0.0
            "eval_args": {
                "group_by": "user",  # default: "user"
                "order": "RO",  # default: "RO"
                "split": {
                    # "RS": [8, 1, 1] # default: {"RS": [8, 1, 1]}
                    "LS": "valid_and_test"
                },
                "mode": {
                    "valid": "full",  # default: "full"
                    "test": "full",  # default: "full"
                },
            },
            "metrics": ["NDCG"],
            # "metrics": ["Recall", "MRR", "NDCG", "Hit", "MAP", "Precision", "GAUC", "ItemCoverage", "AveragePopularity",
            #            "GiniIndex", "ShannonEntropy", "TailPercentage"],
            # default: ["Recall", "MRR", "NDCG", "Hit", "Precision"]
            "topk": [10],  # default: 10
            "valid_metric": "NDCG@10",  # default: "MRR@10"
            "eval_batch_size": 32768,  # default: 4096
            # misc settings
            "model": self.algorithm_name,
            "MODEL_TYPE": ModelType.GENERAL,  # default: ModelType.GENERAL
            "dataset": self.dataset_name,  # default: None
        }

        # Some algos like knn need 1 epoch
        if self.algorithm_name in [
            "Pop",
            "ItemKNN",
            "EASE",
            "SLIMElastic",
            "ADMMSLIM",
            "NCEPLRec",
            "Random",
        ]:
            config_dict.update({"epochs": 1})

        config_dict.update(self.algorithm_config)

        config = Config(config_dict=config_dict)
        init_seed(config["seed"], config["reproducibility"])
        init_logger(config)

        atomic_dir = self.tmp_dir / "atomic"
        atomic_dir.mkdir(exist_ok=True)

        for name, file in zip(
            ("train", "val", "test"), (self.train_file, self.val_file, self.test_file)
        ):
            df = pd.read_csv(file)
            df.drop(columns="timestamp", inplace=True, errors="ignore")
            df.rename(
                columns={
                    "user": "user_id:token",
                    "item": "item_id:token",
                    "rating": "rating:float",
                },
                inplace=True,
            )
            df.to_csv(atomic_dir / f"{self.dataset_name}.{name}.inter", index=False)

        config["data_path"] = atomic_dir
        dataset = create_dataset(config)
        self.train_data, _, _ = data_preparation(config, dataset)

        # FIXME: Type error:
        model = get_model(config["model"])(config, self.train_data.dataset).to(
            config["device"]
        )
        self.trainer: Trainer = get_trainer(config["MODEL_TYPE"], config["model"])(
            config, model
        )

        self.trainer.saved_model_file = str(self.checkpoint_dir / "model.pth")

    def fit(self):
        self.trainer.fit(self.train_data)

    def setup_predict(self):
        # RecBole drops tensorboard logs in CWD
        os.chdir(self.checkpoint_dir)

        self.model_file = self.checkpoint_dir / "model.pth"
        self.config, self.model, self.dataset, _, _, self.test_data = (
            load_data_and_model(model_file=str(self.model_file))
        )

        train = pd.read_csv(self.train_file)
        test = pd.read_csv(self.test_file)

        unique_train_users = train["user"].unique()
        unique_test_users = test["user"].unique()
        users_to_predict = np.intersect1d(unique_test_users, unique_train_users)

        self.uid_series = self.dataset.token2id(
            self.dataset.uid_field, list(map(str, users_to_predict))
        )

        self.top_k_score = []
        self.top_k_iid_list = []

    def predict(self) -> dict[Any, Any]:
        rows = []
        for uid in self.uid_series:
            uid_top_k_score, uid_top_k_iid_list = full_sort_topk(
                np.array([uid]),
                self.model,
                self.test_data,
                k=20,
                device=self.config["device"],
            )
            # convert tensor to numpy array and then to list
            items = uid_top_k_iid_list.cpu().numpy().tolist()[0]
            scores = uid_top_k_score.cpu().numpy().tolist()[0]

            for rank, (iid, score) in enumerate(zip(items, scores), start=1):
                rows.append((uid, iid, rank, score))

        # TODO: Put stuff like this in post_predict

        predictions_df = pd.DataFrame(rows, columns=["user", "item", "rank", "score"])
        predictions_df["item"] = self.dataset.id2token(
            "item_id", predictions_df["item"]
        )
        predictions_df["user"] = self.dataset.id2token(
            "user_id", predictions_df["user"]
        )
        predictions_df["item"] = predictions_df["item"].astype(int)
        predictions_df["user"] = predictions_df["user"].astype(int)
        return predictions_df.to_dict(orient="list")


if __name__ == "__main__":
    RecBole.main()
