import sys
from typing import TypeVar

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, train_test_split

from omnirec.data_variants import (
    DataVariant,
    FoldedData,
    RawData,
    SplitData,
    SplitDataDict,
    # empty_split_dict,
)
from omnirec.preprocess.base import Preprocessor
from omnirec.recsys_data_set import RecSysDataSet
from omnirec.util.util import get_random_state

T = TypeVar("T", bound=DataVariant)
U = TypeVar("U", bound=DataVariant)


class DataSplit(Preprocessor[T, U]):
    def __init__(self, validation_size: float | int) -> None:
        super().__init__()
        self._valid_size = validation_size


class UserHoldout(DataSplit[RawData, SplitData]):
    def __init__(self, validation_size: float | int, test_size: float | int) -> None:
        """Applies the user holdout split to the dataset. Ensures that each user has interactions in the training, validation, and test sets.

        Args:
            validation_size (float | int): float: The proportion (between 0 and 1) of the dataset to include in the validation split.
                                            int: The absolute number of interactions to include in the validation split.
            test_size (float | int): float: The proportion (between 0 and 1) of the dataset to include in the test split.
                                        int: The absolute number of interactions to include in the test split.
        """
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


class UserCrossValidation(DataSplit[RawData, FoldedData]):
    def __init__(self, num_folds: int, validation_size: float | int) -> None:
        """Applies user-based cross-validation to the dataset. Ensures that each user has interactions in the training, validation, and test sets in each fold.

        Args:
            num_folds (int): The number of folds to use for cross-validation.
            validation_size (float | int): float: The proportion (between 0 and 1) of the dataset to include in the validation split.
                                            int: The absolute number of interactions to include in the validation split.
        """
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


class RandomHoldout(DataSplit[RawData, SplitData]):
    def __init__(self, validation_size: float | int, test_size: float | int) -> None:
        """Applies a random holdout split to the dataset. Randomly splits the dataset into training, validation, and test sets.

        Args:
            validation_size (float | int): float: The proportion (between 0 and 1) of the dataset to include in the validation split.
                                            int: The absolute number of interactions to include in the validation split.
            test_size (float | int): float: The proportion (between 0 and 1) of the dataset to include in the test split.
                                        int: The absolute number of interactions to include in the test split.
        """
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


class RandomCrossValidation(DataSplit[RawData, FoldedData]):
    def __init__(self, num_folds: int, validation_size: float | int) -> None:
        """Applies random cross-validation to the dataset. Randomly splits the dataset into training, validation, and test sets for each fold.

        Args:
            num_folds (int): The number of folds to use for cross-validation.
            validation_size (float | int): float: The proportion (between 0 and 1) of the dataset to include in the validation split.
                                            int: The absolute number of interactions to include in the validation split.
        """
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


class TimeBasedHoldout(DataSplit[RawData, SplitData]):
    def __init__(
        self,
        validation: float | int | pd.Timestamp,
        test: float | int | pd.Timestamp,
    ) -> None:
        """Applies a time-based hold-out split on a dataset. Splits the dataset into a train, test and validation split based on the timestamp. Can either use proportions, absolute numbers or timestamps as cut-off criteria.

        Args:
            validation (float | int | pd.Timestamp): float: The proportion (between 0 and 1) of newest interactions in the dataset to include in the validation split.
                                                    int: The absolute number of newest interactions to include in the validation split.
                                                    pd.Timestamp: The timestamp to use as a cut-off for the validation split. Interactions after this timestamp (newer) are included in the validation split.
            test (float | int | pd.Timestamp): float: The proportion (between 0 and 1) of newest interactions in the dataset to include in the test split.
                                                int: The absolute number of newest interactions to include in the test split.
                                                pd.Timestamp: The timestamp to use as a cut-off for the test split. Interactions after this timestamp (newer) are included in the test split.
        """
        super().__init__(0)

        if type(validation) is not type(test):
            self.logger.critical("Validation and test size must be the same type")
            sys.exit(1)

        self._valid_size = validation
        self._test_size = test

    def process(self, dataset: RecSysDataSet[RawData]) -> RecSysDataSet[SplitData]:
        df = dataset._data.df
        df = df.sort_values("timestamp").reset_index(drop=True)
        n = len(df)

        if isinstance(self._valid_size, float) and isinstance(self._test_size, float):
            test_num = int(n * self._test_size)
            test_cutoff = n - test_num
            val_cutoff = n - test_num - int(n * self._valid_size)
        elif isinstance(self._valid_size, int) and isinstance(self._test_size, int):
            test_cutoff = n - self._test_size
            val_cutoff = n - self._test_size - self._valid_size
        elif isinstance(self._valid_size, pd.Timestamp) and isinstance(
            self._test_size, pd.Timestamp
        ):
            test_cutoff = df[df["timestamp"] >= self._test_size.timestamp()].index[0]
            val_cutoff = df[df["timestamp"] >= self._valid_size.timestamp()].index[0]
        else:
            raise ValueError(
                f"Unknown validation or test size type. Got {type(self._valid_size)=}, {type(self._test_size)=}"
            )

        train = df.iloc[:val_cutoff]
        val = df.iloc[val_cutoff:test_cutoff]
        test = df.iloc[test_cutoff:]

        return dataset.replace_data(SplitData(train, val, test))
