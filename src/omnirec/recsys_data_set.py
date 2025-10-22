import copy
import json
import re
import sys
import zipfile
from dataclasses import asdict, dataclass
from os import PathLike
from pathlib import Path
from time import time
from typing import Generic, Optional, TypeVar, cast, overload

import pandas as pd

from omnirec.data_loaders import registry
from omnirec.data_loaders.datasets import DataSet
from omnirec.data_variants import DataVariant, FoldedData, RawData, SplitData
from omnirec.util import util
from omnirec.util.util import _DATA_DIR

logger = util._root_logger.getChild("data")


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
    name: str = "UnnamedDataset"


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
        data_set: DataSet | str,
        raw_dir: Optional[PathLike | str] = None,  # TODO: Name that right
        canon_path: Optional[PathLike | str] = None,  # TODO: Name that right
        force_download=False,
        force_canonicalize=False,
    ) -> "RecSysDataSet[RawData]":
        """Loads a dataset using a registered DataLoader. If not already done the data set is downloaded and canonicalized.
        Canonicalization means duplicates are dropped, identifiers are normalized and the data is saved in a standardized format.

        Args:
            data_set (DataSet | str): The name of the dataset from the DataSet enum. Must be a registered DataLoader name.
            raw_dir (Optional[PathLike | str], optional): Target directory where the raw data is stored. If not provided, the data is downloaded to the default raw data directory (_DATA_DIR).
            canon_path (Optional[PathLike | str], optional): Path where the canonicalized data should be saved. If not provided, the data is saved to the default canonicalized data directory (_DATA_DIR / "canon").
            force_download (bool, optional): If True, forces re-downloading of the raw data even if it already exists. Defaults to False.
            force_canonicalize (bool, optional): If True, forces re-canonicalization of the data even if a canonicalized file exists. Defaults to False.

        Returns:
            RecSysDataSet[RawData]: The loaded dataset in canonicalized RawData format.

        Example:
            ```Python
            # Load the MovieLens 100K dataset using the registered DataLoader
            # Download the raw data to the default directory and save the canonicalized data to the default path
            dataset = RecSysDataSet.use_dataloader(data_set_name=DataSet.MovieLens100K)
            ```
        """
        if isinstance(data_set, DataSet):
            data_set_name = data_set.value
        else:
            data_set_name = data_set
        dataset = RecSysDataSet[RawData]()

        dataset._meta.name = data_set_name

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
    def _canonicalize(
        self,
        drop_duplicates=True,
        normalize_identifiers=True,
        normalize_timestamps=True,
    ) -> None:
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
        if normalize_timestamps:
            self._normalize_timestamps()
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

    def _normalize_timestamps(self) -> None:
        # HACK: We might implement it for the other data variants if needed
        if not isinstance(self._data, RawData):
            logger.error("Cannot normalize identifiers on non raw data, aborting!")
            return
        if "timestamp" in self._data.df.columns:
            logger.info("Normalizing timestamps...")
            ts = self._data.df["timestamp"]
            if pd.api.types.is_numeric_dtype(ts):
                ts = (
                    pd.to_datetime(ts, unit="s", errors="coerce", utc=True).view(
                        "int64"
                    )
                    // 10**9
                )
            else:
                ts = (
                    pd.to_datetime(ts, errors="coerce", utc=True).view("int64") // 10**9
                )
            self._data.df["timestamp"] = ts
            logger.info("Done.")

    def replace_data(self, new_data: R) -> "RecSysDataSet[R]":
        new = cast(RecSysDataSet[R], copy.copy(self))
        new._data = new_data
        return new

    # region Dataset Statistics

    @overload
    def num_interactions(self: "RecSysDataSet[RawData]") -> int: ...

    @overload
    def num_interactions(self: "RecSysDataSet[SplitData]") -> dict[str, int]: ...

    @overload
    def num_interactions(
        self: "RecSysDataSet[FoldedData]",
    ) -> dict[int, dict[str, int]]: ...

    @overload
    def num_interactions(
        self: "RecSysDataSet[T]",
    ) -> int | dict[str, int] | dict[int, dict[str, int]]: ...

    def num_interactions(self):
        if isinstance(self._data, RawData):
            return len(self._data.df)
        elif isinstance(self._data, SplitData):
            return {split: len(df) for split, df in self._data.iter_splits()}
        elif isinstance(self._data, FoldedData):
            return {
                fold_num: {split: len(df) for split, df in fold_data.iter_splits()}
                for fold_num, fold_data in self._data.folds.items()
            }
        else:
            logger.error("Unknown data variant!")
            return -1

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
        """Saves the RecSysDataSet object to a file with the default suffix .rsds.

        Args:
            file (str | PathLike): The path where the file is saved.
        """
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
        """Loads a RecSysDataSet object from a file with the .rsds suffix.

        Args:
            file (str | PathLike): The path to the .rsds file.

        Returns:
            RecSysDataSet[T]: The loaded RecSysDataSet object.
        """
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
            return cast(RecSysDataSet[T], RecSysDataSet(data, meta))

    # endregion
