import pickle
from typing import Any

import numpy as np
import pandas as pd
from pandas import DataFrame
from recpack.algorithms import NMF, SVD, Algorithm, ItemKNN
from scipy.sparse import csr_matrix

from omnirec_runner.runner import Runner


class RecPack(Runner):
    def __init__(self) -> None:
        super().__init__()
        self.algorithms: dict[str, type[Algorithm]] = {
            "SVD": SVD,
            "NMF": NMF,
            "ItemKNN": ItemKNN,
        }

    def setup_fit(self):
        if self.algorithm_name in self.algorithms.keys():
            self.model = self.algorithms[self.algorithm_name](**self.algorithm_config)
        else:
            raise ValueError(f"Algorithm {self.algorithm_name} not found.")

        train, _, _, shape = self.load_data()
        self.train = self.make_csr(train, shape)

    def fit(self):
        self.model.fit(self.train)

    def post_fit(self):
        with open(self.checkpoint_dir / "model.pkl", "wb") as f:
            pickle.dump(self.model, f)

    def setup_predict(self):
        with open(self.checkpoint_dir / "model.pkl", "rb") as f:
            self.model: Algorithm = pickle.load(f)

        train, _, test, shape = self.load_data()
        self.train = self.make_csr(train, shape)

        unique_train_users = train["user"].unique()
        unique_test_users = test["user"].unique()
        self.users_to_predict = np.intersect1d(unique_test_users, unique_train_users)

    def predict(self) -> dict[Any, Any]:
        predictions = self.model.predict(self.train)
        predictions = predictions - predictions.multiply(
            self.train.astype(bool).astype(self.train.dtype)
        )

        # TODO: Move this post_predict once the signature changes
        row_ind, col_ind = predictions.nonzero()
        data = predictions.data

        df = pd.DataFrame({"user": row_ind, "item": col_ind, "score": data})
        df = df[df["user"].isin(self.users_to_predict)]
        df = df.sort_values(["user", "score"], ascending=[True, False])
        df["rank"] = df.groupby("user").cumcount() + 1

        return df.to_dict(orient="list")

    def post_predict(self):
        pass

    def make_csr(self, data_in: DataFrame, shape_in: tuple[int, int]) -> csr_matrix:
        data_indices = data_in[["user", "item"]].values
        data_indices = data_indices[:, 0], data_indices[:, 1]

        data_out = csr_matrix(
            (np.ones(data_in.shape[0]), data_indices), shape=shape_in, dtype=np.float32
        )
        return data_out

    def load_data(self) -> tuple[DataFrame, DataFrame, DataFrame, tuple[int, int]]:
        train = pd.read_csv(self.train_file)
        val = pd.read_csv(self.val_file)
        test = pd.read_csv(self.test_file)

        for df in (train, val, test):
            if "rating" in df.columns:
                raise ValueError(
                    'RecPack only supports implicit feedback. Convert the dataset first to implicit by using preprocessor "MakeImplicit"'
                )

        user_max = max(
            train["user"].max(),
            val["user"].max(),
            test["user"].max(),
        )
        item_max = max(
            train["item"].max(),
            val["item"].max(),
            test["item"].max(),
        )
        shape = (int(user_max + 1), int(item_max + 1))
        return train, val, test, shape


if __name__ == "__main__":
    RecPack.main()
