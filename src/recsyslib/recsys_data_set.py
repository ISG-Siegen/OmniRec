import copy
import json
import re
import sys
import zipfile
from dataclasses import asdict, dataclass
from os import PathLike
from pathlib import Path
from time import time
from typing import Generic, Literal, Optional, TypedDict, TypeVar, cast

import pandas as pd

from recsyslib import util
from recsyslib.data_loaders import registry
from recsyslib.util import _DATA_DIR

logger = util._logger.getChild("dataset")


class DataVariant: ...


# TODO: Maybe Raw is a bit misleading, since after e.g. Core and Subsample it would still be Raw. Maybe change.
# TODO: DOC
@dataclass
class RawData(DataVariant):
    df: pd.DataFrame


# TODO: DOC
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
            ```
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


class SplitDataDict(TypedDict):
    train: pd.DataFrame
    val: pd.DataFrame
    test: pd.DataFrame


# TODO: DOC
@dataclass
class FoldedData(DataVariant):
    folds: dict[int, SplitData]

    @classmethod
    def from_split_dict(cls, raw: dict[int, SplitDataDict]):
        folds = {k: SplitData(**v) for k, v in raw.items()}
        return cls(folds)


# TODO: Document methods

# TODO: Raw Initialization, i.e. from dataframe?

# TODO: __str__ and __repr__ methods

# TODO (Python 3.12+): Replace TypeVar with inline generic syntax `class Box[T](...)`
T = TypeVar("T", bound=DataVariant)
R = TypeVar("R", bound=DataVariant)


@dataclass
class _DatasetMeta:
    canon_pth: Optional[Path] = None
    raw_dir: Optional[Path] = None


class RecSysDataSet(Generic[T]):
    _folds_file_pattern = re.compile(r"(\d+)\/(?:train|val|test)\.csv")

    def __init__(
        self, data: Optional[T] = None, meta: _DatasetMeta = _DatasetMeta()
    ) -> None:
        if data:
            self._data = data
        self._meta = meta

    @staticmethod
    def use_dataloader(
        data_set_name: str,
        raw_dir: Optional[PathLike | str] = None,  # TODO: Name that right
        canon_path: Optional[PathLike | str] = None,  # TODO: Name that right
        force_download=False,
        force_canonicalize=False,
    ) -> "RecSysDataSet[RawData]":
        dataset = RecSysDataSet[RawData]()
        if canon_path:
            dataset._meta.canon_pth = Path(canon_path)
        else:
            canon_dir = _DATA_DIR / "canon"
            canon_dir.mkdir(parents=True, exist_ok=True)
            dataset._meta.canon_pth = (canon_dir / data_set_name).with_suffix(".csv")
        if dataset._meta.canon_pth.exists() and not (
            force_canonicalize or force_download
        ):
            logger.info(
                "Canonicalized data set already exists, skipping download and canonicalization."
            )
            dataset._data = RawData(pd.read_csv(dataset._meta.canon_pth))
            return dataset

        if raw_dir:
            dataset._meta.raw_dir = Path(raw_dir)

        dataset._data = RawData(
            registry._run_loader(data_set_name, force_download, dataset._meta.raw_dir)
        )
        dataset._canonicalize()
        return dataset

    # TODO: Expose drop dup and norm id params to public API somehow
    def _canonicalize(self, drop_duplicates=True, normalize_identifiers=True) -> None:
        # HACK: We might implement it for the other data variants if needed
        if not isinstance(self._data, RawData):
            logger.error("Cannot canonicalize non raw data, aborting!")
            return
        start_time = time()
        logger.info("Canonicalizing raw data...")

        if drop_duplicates:
            self._drop_duplicates()
        if normalize_identifiers:
            self._normalize_identifiers()
        # self.check_and_order_columns() # TODO: Ask Lukas about the complex checking logic in the OG. Why the ordering, since columns are named?
        # self.check_and_convert_data_types() # TODO: Check back with Lukas, this might be the wrong place to do that, since after writing/loading from csv dtypes are different again: Result: Do that in adapters! Be careful, str may work, but lib may do it as category.
        stop_time = time()
        logger.info(f"Canonicalized raw data in {(stop_time - start_time):.4f}s.")
        logger.info(f"Saving to {self._meta.canon_pth}...")
        self._data.df.to_csv(self._meta.canon_pth, index=False)

    def _drop_duplicates(self) -> None:
        # HACK: We might implement it for the other data variants if needed
        if not isinstance(self._data, RawData):
            logger.error("Cannot drop duplicated on non raw data, aborting!")
            return
        logger.info("Dropping duplicate interactions...")
        logger.info(f"Number of interactions before: {self.num_interactions()}")
        self._data.df.drop_duplicates(
            subset=["user", "item"], keep="last", inplace=True
        )
        logger.info(f"Number of interactions after: {self.num_interactions()}")

    def _normalize_identifiers(self) -> None:
        # HACK: We might implement it for the other data variants if needed
        if not isinstance(self._data, RawData):
            logger.error("Cannot normalize identifiers on non raw data, aborting!")
            return
        logger.info("Normalizing identifiers...")
        for col in ["user", "item"]:
            unique_ids = {
                key: value for value, key in enumerate(self._data.df[col].unique())
            }
            self._data.df[col] = self._data.df[col].map(unique_ids)
        logger.info("Done.")

    def replace_data(self, new_data: R) -> "RecSysDataSet[R]":
        new = cast(RecSysDataSet[R], copy.copy(self))
        new._data = new_data
        return new

    # region Dataset Statistics

    def num_interactions(self) -> int:
        # TODO: # HACK: I feel like these should easily implemented
        if not isinstance(self._data, RawData):
            logger.error("Cannot get num_interactions on non raw data, aborting!")
            return -1
        return len(self._data.df)

    def min_rating(self) -> float | int:
        # TODO: # HACK: I feel like these should easily implemented
        if not isinstance(self._data, RawData):
            logger.error("Cannot get min_rating on non raw data, aborting!")
            return -1
        return self._data.df["rating"].min()
        # TODO: Do we need that line: ?
        # if self.feedback_type == "explicit" else None

    def max_rating(self) -> float | int:
        # TODO: # HACK: I feel like these should easily implemented
        if not isinstance(self._data, RawData):
            logger.error("Cannot get max_rating on non raw data, aborting!")
            return -1
        return self._data.df["rating"].max()
        # TODO: Do we need that line: ?
        # if self.feedback_type == "explicit" else None

    # endregion

    # region File IO

    # TODO: Logging in save function
    # TODO: check if path already exists
    # TODO: Error handling: logger.critical and sys.exit(1) if any step causes an error
    def save(self, file: str | PathLike):
        file = Path(file)
        if not file.suffix:
            file = file.with_suffix(".rsds")
        with zipfile.ZipFile(file, "w", zipfile.ZIP_STORED) as zf:
            if isinstance(self._data, RawData):
                with zf.open("data.csv", "w") as data_file:
                    self._data.df.to_csv(data_file, index=False)
                zf.writestr("VARIANT", "RawData")
            elif isinstance(self._data, SplitData):
                for filename, data in zip(
                    ["train", "val", "test"],
                    [self._data.train, self._data.val, self._data.test],
                ):
                    with zf.open(filename + ".csv", "w") as data_file:
                        data.to_csv(data_file, index=False)
                zf.writestr("VARIANT", "SplitData")
            elif isinstance(self._data, FoldedData):
                # TODO: Leveraging the new SplitData.get method this can be simplified:
                def write_fold(fold: int, split: str, data: pd.DataFrame):
                    with zf.open(f"{fold}/{split}.csv", "w") as data_file:
                        data.to_csv(data_file, index=False)

                for fold, splits in self._data.folds.items():
                    write_fold(fold, "train", splits.train)
                    write_fold(fold, "val", splits.val)
                    write_fold(fold, "test", splits.test)

                zf.writestr("VARIANT", "FoldedData")

            else:
                logger.critical(
                    f"Unknown data variant: {type(self._data).__name__}! Aborting save operation..."
                )
                sys.exit(1)

            zf.writestr("META", json.dumps(asdict(self._meta), default=str))
            # HACK: Very simple versioning implementation in case we change anything in the future
            zf.writestr("VERSION", "1.0.0")

    # TODO: Check file exists
    # TODO: Error handling: logger.critical and sys.exit(1) if any step causes an error
    @staticmethod
    def load(file: str | PathLike) -> "RecSysDataSet[T]":
        with zipfile.ZipFile(file, "r", zipfile.ZIP_STORED) as zf:
            version = zf.read("VERSION").decode()
            # HACK: Very simple versioning implementation in case we change anything in the future
            if version != "1.0.0":
                logger.critical(f"Unknown rsds-file version: {version}")
                sys.exit(1)

            variant = zf.read("VARIANT").decode()

            if variant == "RawData":
                with zf.open("data.csv", "r") as data_file:
                    data = RawData(pd.read_csv(data_file))
            elif variant == "SplitData":
                dfs: list[pd.DataFrame] = []

                for filename in ["train", "val", "test"]:
                    with zf.open(filename + ".csv", "r") as data_file:
                        dfs.append(pd.read_csv(data_file))

                data = SplitData(dfs[0], dfs[1], dfs[2])
            elif variant == "FoldedData":
                folds: dict[int, SplitData] = {}

                for p in zf.namelist():
                    match = RecSysDataSet._folds_file_pattern.match(p)
                    if not match:
                        continue

                    fold = match.group(1)
                    folds.setdefault(
                        int(fold), SplitData(*[pd.DataFrame() for _ in range(3)])
                    )

                # TODO: Leveraging the new FoldedData.from_split_dict method this can be simplified:
                def read_fold(fold: int, split: str) -> pd.DataFrame:
                    with zf.open(f"{fold}/{split}.csv", "r") as data_file:
                        return pd.read_csv(data_file)

                for fold, split_data in folds.items():
                    split_data.train = read_fold(fold, "train")
                    split_data.val = read_fold(fold, "val")
                    split_data.test = read_fold(fold, "test")

                data = FoldedData(folds)
            else:
                logger.critical(
                    f"Unknown data variant: {variant}! Aborting load operation..."
                )
                sys.exit(1)

            meta = zf.read("META").decode()
            meta = _DatasetMeta(**json.loads(meta))
            return cast(RecSysDataSet[T], RecSysDataSet(data))

    # endregion
