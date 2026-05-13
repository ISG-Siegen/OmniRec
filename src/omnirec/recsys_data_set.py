import copy
import re
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from pprint import pformat
from time import time
from typing import Generic, Optional, TypeVar, cast, overload

import pandas as pd

from omnirec.data_loaders import registry
from omnirec.data_loaders.datasets import DataSet
from omnirec.data_variants import DataVariant, FoldedData, RawData, SplitData
from omnirec.preprocess.trace import Trace
from omnirec.types import CountSummary
from omnirec.util import util
from omnirec.util.util import get_data_dir

logger = util._root_logger.getChild("data")


# TODO: Document methods

# TODO: Raw Initialization, i.e. from dataframe?

# TODO (Python 3.12+): Replace TypeVar with inline generic syntax `class Box[T](...)`
T = TypeVar("T", bound=DataVariant)
R = TypeVar("R", bound=DataVariant)


@dataclass
class DatasetMeta:
    canon_pth: Optional[Path] = None
    raw_dir: Optional[Path] = None
    name: str = "UnnamedDataset"

    def format_details(self) -> str:
        lines = [f"Name: {self.name}"]
        lines.append(
            f"Canonical path: {self.canon_pth if self.canon_pth is not None else 'unknown'}"
        )
        lines.append(
            f"Raw dir: {self.raw_dir if self.raw_dir is not None else 'unknown'}"
        )
        return "\n".join(lines)


class RecSysDataSet(Generic[T]):
    _folds_file_pattern = re.compile(r"(\d+)\/(?:train|val|test)\.csv")
    _lineage: list[Trace]

    def __init__(
        self, data: Optional[T] = None, meta: Optional[DatasetMeta] = None
    ) -> None:
        self._lineage = []

        if data:
            self._data = data

        if meta is None:
            meta = DatasetMeta()
        self._meta = meta

    @staticmethod
    def _append_field(
        lines: list[str], label: str, value: object, indent_level: int = 1
    ) -> None:
        prefix = "  " * indent_level

        if value is None:
            rendered = "unknown"
        elif isinstance(value, (dict, list, tuple, set)):
            rendered = pformat(value, sort_dicts=False)
        else:
            rendered = str(value)

        rendered_lines = rendered.splitlines()
        if len(rendered_lines) == 1:
            lines.append(f"{prefix}{label}: {rendered_lines[0]}")
            return

        lines.append(f"{prefix}{label}:")
        lines.extend(f"{prefix}  {line}" for line in rendered_lines)

    def _data_variant_name(self) -> str:
        if not hasattr(self, "_data"):
            return "Uninitialized"
        return type(self._data).__name__

    def _interaction_summary(self) -> CountSummary | None:
        if not hasattr(self, "_data"):
            return None
        return self.num_interactions()

    def _column_summary(self) -> CountSummary | None:
        if not hasattr(self, "_data"):
            return None
        return self.num_columns()

    @property
    def meta(self) -> DatasetMeta:
        """Return a shallow copy of the dataset metadata."""
        return copy.copy(self._meta)

    @property
    def lineage(self) -> tuple[Trace, ...]:
        """Return the recorded preprocessing lineage as a read-only snapshot."""
        return tuple(copy.deepcopy(self._lineage))

    def format_lineage(self, details: bool = False) -> str:
        """Render the dataset lineage in either compact or detailed form."""
        if not self._lineage:
            return "No preprocessing lineage recorded."

        if not details:
            return "\n".join(
                f"{index}. {trace!r}"
                for index, trace in enumerate(self._lineage, start=1)
            )

        return "\n\n".join(
            "\n".join((f"Step {index}", trace.format_details()))
            for index, trace in enumerate(self._lineage, start=1)
        )

    def format_details(
        self, include_lineage: bool = True, lineage_details: bool = False
    ) -> str:
        """Render a human-readable summary of the dataset and its provenance."""
        lines = [f"RecSysDataSet: {self._meta.name}"]
        self._append_field(lines, "Variant", self._data_variant_name())
        self._append_field(lines, "Interactions", self._interaction_summary())
        self._append_field(lines, "Columns", self._column_summary())

        lines.append("  Metadata:")
        lines.extend(f"    {line}" for line in self._meta.format_details().splitlines())

        self._append_field(lines, "Lineage steps", len(self._lineage))
        if include_lineage:
            lines.append("  Lineage:")
            formatted_lineage = self.format_lineage(details=lineage_details)
            lines.extend(f"    {line}" for line in formatted_lineage.splitlines())

        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            "RecSysDataSet("
            f"name={self._meta.name!r}, "
            f"variant={self._data_variant_name()!r}, "
            f"interactions={self._interaction_summary()!r}, "
            f"columns={self._column_summary()!r}, "
            f"lineage_steps={len(self._lineage)}"
            ")"
        )

    __str__ = __repr__

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
            canon_dir = get_data_dir() / "canon"
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
                    pd.to_datetime(ts, unit="s", errors="coerce", utc=True).astype(
                        "int64"
                    )
                    // 10**9
                )
            else:
                ts = (
                    pd.to_datetime(ts, errors="coerce", utc=True).astype("int64")
                    // 10**9
                )
            self._data.df["timestamp"] = ts
            logger.info("Done.")

    def replace_data(self, new_data: R) -> "RecSysDataSet[R]":
        new = cast(RecSysDataSet[R], copy.copy(self))
        new._data = new_data
        new._lineage = list(self._lineage)
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
    def num_interactions(self: "RecSysDataSet[T]") -> CountSummary: ...

    def num_interactions(self) -> CountSummary:
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

    @overload
    def num_columns(self: "RecSysDataSet[RawData]") -> int: ...

    @overload
    def num_columns(self: "RecSysDataSet[SplitData]") -> dict[str, int]: ...

    @overload
    def num_columns(
        self: "RecSysDataSet[FoldedData]",
    ) -> dict[int, dict[str, int]]: ...

    @overload
    def num_columns(self: "RecSysDataSet[T]") -> CountSummary: ...

    def num_columns(self) -> CountSummary:
        if isinstance(self._data, RawData):
            return len(self._data.df.columns)
        elif isinstance(self._data, SplitData):
            return {split: len(df.columns) for split, df in self._data.iter_splits()}
        elif isinstance(self._data, FoldedData):
            return {
                fold_num: {
                    split: len(df.columns) for split, df in fold_data.iter_splits()
                }
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
        from omnirec.rsds.dispatcher import save_dataset

        file = Path(file)
        if not file.suffix:
            file = file.with_suffix(".rsds")

        save_dataset(self, file)

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
        from omnirec.rsds.dispatcher import load_dataset

        file = Path(file)

        ds = load_dataset(file)
        return cast(RecSysDataSet[T], ds)

    # endregion
