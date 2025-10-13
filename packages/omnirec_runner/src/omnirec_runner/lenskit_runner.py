from pathlib import Path

import binpickle
import numpy as np
import pandas as pd
from lenskit.als import (
    BiasedMFConfig,
    BiasedMFScorer,
    ImplicitMFConfig,
    ImplicitMFScorer,
)
from lenskit.basic.popularity import PopConfig, PopScorer
from lenskit.batch import predict, recommend
from lenskit.data import from_interactions_df
from lenskit.funksvd import FunkSVDConfig, FunkSVDScorer
from lenskit.knn import ItemKNNConfig, ItemKNNScorer, UserKNNConfig, UserKNNScorer
from lenskit.pipeline import predict_pipeline, topn_pipeline
from lenskit.pipeline.components import Component
from lenskit.training import TrainingOptions
from pydantic import BaseModel

from omnirec_runner.runner import Runner


class Lenskit(Runner):
    def __init__(self) -> None:
        super().__init__()
        self.algorithms: dict[str, tuple[type[Component], type[BaseModel]]] = {
            a.__name__: (a, c)
            for a, c in [
                (PopScorer, PopConfig),
                (ItemKNNScorer, ItemKNNConfig),
                (UserKNNScorer, UserKNNConfig),
                (ImplicitMFScorer, ImplicitMFConfig),
                (BiasedMFScorer, BiasedMFConfig),
                (FunkSVDScorer, FunkSVDConfig),
            ]
        }

    def setup_fit(self):
        self.model_file = self.checkpoint_dir / "model.bpk"
        self.train = pd.read_csv(self.train_file)

        if "rating" in self.train.columns:
            self.algorithm_config["feedback"] = "explicit"
        else:
            self.algorithm_config["feedback"] = "implicit"

        if self.algorithm_name in self.algorithms.keys():
            algo_cls, config_cls = self.algorithms[self.algorithm_name]
            scorer = algo_cls(config_cls(**self.algorithm_config))

            if "rating" in self.train.columns:
                self.model = predict_pipeline(scorer)
            else:
                self.model = topn_pipeline(scorer)
        else:
            raise ValueError(f"Algorithm {self.algorithm_name} not found.")

    def fit(self):
        dataset = from_interactions_df(self.train)
        self.model.train(dataset, TrainingOptions())

    def post_fit(self):
        # TODO:
        # fit_log_dict = {
        #         "model_file": model_file,
        #         "data_set_name": data_set_name,
        #         "algorithm_name": algorithm_name,
        #         "algorithm_config_index": algorithm_config,
        #         "algorithm_configuration": configurations[algorithm_config],
        #         "fold": fold,
        #         "setup_time": setup_end_time - setup_start_time,
        #         "training_time": fit_end_time - fit_start_time
        #     }
        binpickle.dump(self.model, self.model_file)

    def setup_predict(self):
        self.model_file = self.checkpoint_dir / "model.bpk"
        self.model = binpickle.load(self.model_file)

        self.train = pd.read_csv(self.train_file)
        self.test = pd.read_csv(self.test_file)

        unique_train_users = self.train["user"].unique()
        unique_test_users = self.test["user"].unique()
        self.users_to_predict = np.intersect1d(unique_test_users, unique_train_users)

    def predict(self):
        # TODO:
        # predict_log_dict = {
        #     "model_file": model_file,
        #     "data_set_name": data_set_name,
        #     "algorithm_name": algorithm_name,
        #     "algorithm_config_index": algorithm_config,
        #     "algorithm_configuration": configurations[algorithm_config],
        #     "fold": fold,
        # }
        # predict_log_dict.update(
        #     {
        #         "train_users": len(unique_train_users),
        #         "test_users": len(unique_test_users),
        #         "users_to_predict": len(users_to_predict),
        #         "prediction_time": end_prediction - start_prediction,
        #     }
        # )
        # predict_log_dict.update(
        #     {
        #         "test_interactions": test_interactions, # This was len(test) OG
        #         "prediction_time": end_prediction - start_prediction,
        #     }
        # )

        # Lenskit automatically finds the id, but it has to be suffixed with "_id"
        self.test.rename(columns={"user": "user_id", "item": "item_id"}, inplace=True)

        if "rating" in self.train.columns:
            self.test.drop(columns="rating", inplace=True)
            predictions = predict(self.model, self.test)
        else:
            predictions = recommend(self.model, self.test)

        predictions_df = predictions.to_df()
        predictions_df.rename(
            columns={"user_id": "user", "item_id": "item"},
            inplace=True,
        )
        if "rating" in self.train.columns:
            predictions_df.rename(columns={"score": "rating"}, inplace=True)
        return predictions_df.to_dict(orient="list")


if __name__ == "__main__":
    Lenskit.main()
