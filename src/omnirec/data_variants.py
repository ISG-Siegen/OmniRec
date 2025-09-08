import sys
from dataclasses import dataclass
from typing import Generator, Literal, TypedDict

import pandas as pd

from omnirec.util import util

logger = util._root_logger.getChild("data")


class DataVariant: ...


# TODO: Maybe Raw is a bit misleading, since after e.g. Core and Subsample it would still be Raw. Maybe change.
# TODO: DOC
@dataclass
class RawData(DataVariant):
    df: pd.DataFrame


@dataclass
class SplitData(DataVariant):
    train: pd.DataFrame
    val: pd.DataFrame
    test: pd.DataFrame

    def get(self, split: Literal["train", "val", "test"]) -> pd.DataFrame:
        """Helper method for getting a portion of the split by specifying the name as a str.

        Args:
            split (Literal["train", "val", "test"]): The name of the split's portion to retrieve. Can be "train", "val" or "test".

        Returns:
            pd.DataFrame: Pandas `DataFrame` containing the split portion's data.

        Example:
            ```Python
            splits: SplitData = ...

            # Retrieve all splits in e.g. a loop:
            for split_name in ["train", "val", "test"]:
                data = splits.get(split_name)

            # The above example would be a lot move verbose without the get method.
            ```
        """
        if split == "train":
            return self.train
        elif split == "val":
            return self.val
        elif split == "test":
            return self.test
        else:
            logger.critical(f"Uknown split: {split}")
            sys.exit(1)

    # TODO: Doc
    def iter_splits(
        self,
    ) -> Generator[tuple[Literal["train", "val", "test"], pd.DataFrame], None, None]:
        for split in ("train", "val", "test"):
            yield split, self.get(split)


class SplitDataDict(TypedDict, total=False):
    """TypedDict for representing split data in a dictionary format. Values are expected to be DataFrames for the keys "train", "val", and "test"."""

    train: pd.DataFrame
    val: pd.DataFrame
    test: pd.DataFrame


@dataclass
class FoldedData(DataVariant):
    folds: dict[int, SplitData]

    @classmethod
    def from_split_dict(cls, raw: dict[int, SplitDataDict]):
        """Creates a FoldedData instance from a dictionary of split data.

        Args:
            raw (dict[int, SplitDataDict]): A dictionary mapping fold indices to their corresponding split data.

        Returns:
            FoldedData: An instance of FoldedData containing the folded data.
        """
        folds = {k: SplitData(**v) for k, v in raw.items()}
        return cls(folds)
