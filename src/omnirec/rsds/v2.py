from typing import Any, Literal
from zipfile import ZipFile

from pydantic import TypeAdapter

from omnirec.preprocess.trace import Trace
from omnirec.recsys_data_set import DatasetMeta, RecSysDataSet
from omnirec.rsds.manifest import ManifestBase
from omnirec.rsds.v1 import (
    DATASET_META_ADAPTER,
    DatasetVariantName,
    _detect_dataset_variant_name,
    _read_data,
    _write_data,
)
from omnirec.types import CountSummary

LINEAGE_FILENAME = "lineage.json"


class ManifestV2(ManifestBase):
    format: str = "rsds"
    schema_version: Literal[2] = 2
    dataset_variant: DatasetVariantName


LINEAGE_ADAPTER = TypeAdapter(list[Trace])


def build_manifest(dataset: RecSysDataSet[Any]) -> ManifestV2:
    return ManifestV2(
        format="rsds",
        schema_version=2,
        dataset_variant=_detect_dataset_variant_name(dataset),
    )


def load(zf: ZipFile, manifest: ManifestV2) -> RecSysDataSet[Any]:
    data = _read_data(manifest.dataset_variant, zf)
    meta = _read_meta(zf)
    dataset = RecSysDataSet(data, meta)
    dataset._lineage = _read_lineage(zf)

    return dataset


def save(zf: ZipFile, dataset: RecSysDataSet[Any], manifest: ManifestV2) -> None:
    _write_data(dataset._data, zf)
    _write_meta(dataset._meta, zf)
    _write_lineage(dataset._lineage, zf)


def _read_meta(zf: ZipFile):
    meta_json = zf.read("meta.json").decode()
    return DATASET_META_ADAPTER.validate_json(meta_json)


def _write_meta(meta: DatasetMeta, zf: ZipFile):
    zf.writestr("meta.json", DATASET_META_ADAPTER.dump_json(meta))


def _read_lineage(zf: ZipFile) -> list[Trace]:
    if LINEAGE_FILENAME not in zf.namelist():
        return []

    lineage_json = zf.read(LINEAGE_FILENAME).decode()
    return LINEAGE_ADAPTER.validate_json(lineage_json)


def _write_lineage(lineage: list[Trace], zf: ZipFile) -> None:
    zf.writestr(LINEAGE_FILENAME, LINEAGE_ADAPTER.dump_json(lineage))


def _count_summary_to_json(count_summary: CountSummary | None) -> Any:
    if count_summary is None or isinstance(count_summary, int):
        return count_summary

    return {
        str(key): _count_summary_to_json(value) for key, value in count_summary.items()
    }


def _count_summary_from_json(raw_count_summary: Any) -> CountSummary | None:
    if raw_count_summary is None or isinstance(raw_count_summary, int):
        return raw_count_summary

    if all(_is_int_like(key) for key in raw_count_summary):
        return {
            int(key): {str(split): int(count) for split, count in split_counts.items()}
            for key, split_counts in raw_count_summary.items()
        }

    return {str(key): int(value) for key, value in raw_count_summary.items()}


def _is_int_like(value: object) -> bool:
    return isinstance(value, int) or (isinstance(value, str) and value.isdigit())
