import sys
from typing import Any, Literal
from zipfile import ZipFile

import pandas as pd
from pydantic import TypeAdapter

from omnirec.data_variants import DataVariant, FoldedData, RawData, SplitData
from omnirec.recsys_data_set import DatasetMeta, RecSysDataSet
from omnirec.rsds.manifest import ManifestBase
from omnirec.util import util

logger = util._root_logger.getChild("rsds")

LEGACY_VERSION = "1.0.0"

type DatasetVariantName = Literal["RawData", "SplitData", "FoldedData"]


class ManifestV1(ManifestBase):
    format: str = "rsds"
    schema_version: Literal[1] = 1


DATASET_META_ADAPTER = TypeAdapter(DatasetMeta)


def build_manifest(dataset: RecSysDataSet[Any]) -> ManifestV1:
    return ManifestV1(format="rsds", schema_version=1)


def load(zf: ZipFile, manifest: ManifestV1) -> RecSysDataSet[Any]:
    variant = zf.read("VARIANT").decode()

    data = _read_data(variant, zf)
    meta = _read_meta(zf)

    return RecSysDataSet(data, meta)


def save(zf: ZipFile, dataset: RecSysDataSet[Any], manifest: ManifestV1) -> None:
    _write_data(dataset._data, zf)
    _write_meta(dataset._meta, zf)

    variant = _detect_dataset_variant_name(dataset)
    zf.writestr("VARIANT", variant)


def _read_meta(zf: ZipFile):
    meta_json = zf.read("META").decode()
    return DATASET_META_ADAPTER.validate_json(meta_json)


def _read_data(variant: str, zf: ZipFile) -> DataVariant:
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
            folds.setdefault(int(fold), SplitData(*[pd.DataFrame() for _ in range(3)]))

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
        logger.critical(f"Unknown data variant: {variant}! Aborting load operation...")
        sys.exit(1)

    return data


def _write_meta(meta: DatasetMeta, zf: ZipFile):
    zf.writestr("META", DATASET_META_ADAPTER.dump_json(meta))


def _write_data(data: DataVariant, zf: ZipFile):

    if isinstance(data, RawData):
        with zf.open("data.csv", "w") as data_file:
            data.df.to_csv(data_file, index=False)

    elif isinstance(data, SplitData):
        for filename, dataframe in zip(
            ["train", "val", "test"],
            [data.train, data.val, data.test],
        ):
            with zf.open(filename + ".csv", "w") as data_file:
                dataframe.to_csv(data_file, index=False)

    elif isinstance(data, FoldedData):
        # TODO: Leveraging the new SplitData.get method this can be simplified:
        def write_fold(fold: int, split: str, data: pd.DataFrame):
            with zf.open(f"{fold}/{split}.csv", "w") as data_file:
                data.to_csv(data_file, index=False)

        for fold, splits in data.folds.items():
            write_fold(fold, "train", splits.train)
            write_fold(fold, "val", splits.val)
            write_fold(fold, "test", splits.test)

    else:
        logger.critical(
            f"Unknown data variant: {type(data).__name__}! Aborting save operation..."
        )
        sys.exit(1)


def _detect_dataset_variant_name(dataset: RecSysDataSet[Any]) -> DatasetVariantName:
    data = dataset._data

    if isinstance(data, RawData):
        return "RawData"
    if isinstance(data, SplitData):
        return "SplitData"
    if isinstance(data, FoldedData):
        return "FoldedData"

    raise ValueError(f"Unsupported dataset variant: {type(data).__name__}")
