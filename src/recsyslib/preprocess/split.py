import sys
from collections import defaultdict

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, train_test_split

from recsyslib.data_variants import (
    FoldedData,
    RawData,
    SplitData,
    SplitDataDict,
    # empty_split_dict,
)
from recsyslib.preprocess.base import Preprocessor
from recsyslib.recsys_data_set import RecSysDataSet
from recsyslib.util.util import get_random_state


class DataSplit(Preprocessor):
    def __init__(self, validation_size: float | int) -> None:
        super().__init__()
        self._valid_size = validation_size


class UserHoldout(DataSplit):
    def __init__(self, validation_size: float | int, test_size: float | int) -> None:
        super().__init__(validation_size)
        self._test_size = test_size

    def process(self, dataset: RecSysDataSet[RawData]) -> RecSysDataSet[SplitData]:
        df = dataset._data.df

        indices = {"train": np.array([]), "valid": np.array([]), "test": np.array([])}
        df.reset_index(drop=True, inplace=True)
        for user, items in df.groupby("user").indices.items():
            train, test = train_test_split(
                items, test_size=self._test_size, random_state=get_random_state()
            )
            train, valid = train_test_split(
                train,
                test_size=self._valid_size / (1 - self._test_size),
                random_state=get_random_state(),
            )
            indices["train"] = np.append(indices["train"], train)
            indices["valid"] = np.append(indices["valid"], valid)
            indices["test"] = np.append(indices["test"], test)

        return dataset.replace_data(
            SplitData(
                df.iloc[indices["train"]],
                df.iloc[indices["valid"]],
                df.iloc[indices["test"]],
            )
        )


class UserCrossValidation(DataSplit):
    def __init__(self, num_folds: int, validation_size: float | int) -> None:
        super().__init__(validation_size)
        self._num_folds = num_folds

    def process(self, dataset: RecSysDataSet[RawData]) -> RecSysDataSet[FoldedData]:
        data_splits: dict[int, dict[str, list[pd.DataFrame]]] = {}
        for fold in range(self._num_folds):
            data_splits[fold] = {"train": [], "val": [], "test": []}
        data = dataset._data.df
        data.reset_index(drop=True, inplace=True)
        for user, interaction_index in data.groupby("user").groups.items():
            if len(interaction_index) < self._num_folds:
                self.logger.critical(
                    f"User {user} has less interactions than the number of folds ({self._num_folds}). Unable to split."
                )
                sys.exit(1)
            folds = KFold(
                n_splits=self._num_folds, shuffle=True, random_state=get_random_state()
            )
            for fold_idx, (train_index, test_index) in enumerate(
                # FIXME: Type error here:
                folds.split(interaction_index)
            ):
                train, test = (
                    interaction_index[train_index],
                    interaction_index[test_index],
                )
                if self._valid_size is not None:
                    train, valid = train_test_split(
                        train,
                        test_size=self._valid_size / (1 - (1 / self._num_folds)),
                        random_state=get_random_state(),
                    )
                    data_splits[fold_idx]["val"].append(data.iloc[valid])
                data_splits[fold_idx]["train"].append(data.iloc[train])
                data_splits[fold_idx]["test"].append(data.iloc[test])

        concatenated_data_splits: dict[int, SplitDataDict] = {}
        for fold in range(self._num_folds):
            for partition in ["train", "val", "test"]:
                if len(data_splits[fold][partition]) > 0:
                    concatenated_data_splits.setdefault(fold, {})[partition] = (
                        pd.concat(data_splits[fold][partition])
                    )
                else:
                    del data_splits[fold][partition]

        return dataset.replace_data(
            FoldedData.from_split_dict(concatenated_data_splits)
        )


class RandomHoldout(DataSplit):
    def __init__(self, validation_size: float | int, test_size: float | int) -> None:
        super().__init__(validation_size)
        self._test_size = test_size

    def process(self, dataset: RecSysDataSet[RawData]) -> RecSysDataSet[SplitData]:
        data = dataset._data.df

        train, test = train_test_split(
            data, test_size=self._test_size, random_state=get_random_state()
        )
        train, valid = train_test_split(
            train,
            test_size=self._valid_size / (1 - self._test_size),
            random_state=get_random_state(),
        )
        return dataset.replace_data(SplitData(train, valid, test))


class RandomCrossValidation(DataSplit):
    def __init__(self, num_folds: int, validation_size: float | int) -> None:
        super().__init__(validation_size)
        self._num_folds = num_folds

    def process(self, dataset: RecSysDataSet[RawData]) -> RecSysDataSet[FoldedData]:
        data = dataset._data.df
        data_splits: dict[int, SplitDataDict] = {}

        folds = KFold(
            n_splits=self._num_folds, shuffle=True, random_state=get_random_state()
        )
        for fold, (train_index, test_index) in enumerate(folds.split(data)):
            train, test = data.iloc[train_index], data.iloc[test_index]
            train, valid = train_test_split(
                train,
                test_size=self._valid_size / (1 - (1 / self._num_folds)),
                random_state=get_random_state(),
            )
            data_splits[fold] = {
                "train": train,
                "val": valid,
                "test": test,
            }

        return dataset.replace_data(FoldedData.from_split_dict(data_splits))
