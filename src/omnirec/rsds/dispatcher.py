import zipfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Any
from zipfile import ZipFile

from pydantic import Field, RootModel

from omnirec.recsys_data_set import RecSysDataSet
from omnirec.rsds import v1, v2

MANIFEST_FILENAME = "manifest.json"
LEGACY_VERSION_FILENAME = "VERSION"
LATEST_SCHEMA_VERSION = 2

Manifest = Annotated[
    v1.ManifestV1 | v2.ManifestV2, Field(discriminator="schema_version")
]


type RsdsLoadFn[ManifestT: Manifest] = Callable[
    [ZipFile, ManifestT], RecSysDataSet[Any]
]
type RsdsSaveFn[ManifestT: Manifest] = Callable[
    [ZipFile, RecSysDataSet[Any], ManifestT], None
]
type RsdsBuildManifestFn[ManifestT: Manifest] = Callable[
    [RecSysDataSet[Any]], ManifestT
]


class ManifestSchema(RootModel):
    root: Manifest


@dataclass(frozen=True)
class RsdsCodec[ManifestT: Manifest]:
    build_manifest: RsdsBuildManifestFn[ManifestT]
    load: RsdsLoadFn[ManifestT]
    save: RsdsSaveFn[ManifestT]


LOADERS: dict[int, RsdsCodec[Any]] = {
    1: RsdsCodec(build_manifest=v1.build_manifest, load=v1.load, save=v1.save),
    2: RsdsCodec(build_manifest=v2.build_manifest, load=v2.load, save=v2.save),
}


def load_dataset(file: Path) -> RecSysDataSet[Any]:
    with ZipFile(file, "r", zipfile.ZIP_STORED) as zf:
        manifest = _read_manifest(zf)
        return _get_codec(manifest.schema_version).load(zf, manifest)


def save_dataset(
    dataset: RecSysDataSet[Any],
    file: Path,
    schema_version: int = LATEST_SCHEMA_VERSION,
) -> None:
    with ZipFile(file, "w", zipfile.ZIP_STORED) as zf:
        codec = _get_codec(schema_version)
        manifest = codec.build_manifest(dataset)
        codec.save(zf, dataset, manifest)
        _write_manifest_metadata(zf, manifest)


def detect_schema_version(zf: ZipFile) -> int:
    return _read_manifest(zf).schema_version


def _read_manifest(zf: ZipFile) -> Manifest:
    if MANIFEST_FILENAME in zf.namelist():
        return _read_dispatch_manifest(zf)

    if LEGACY_VERSION_FILENAME in zf.namelist():
        return _read_legacy_manifest(zf)

    raise ValueError("Unable to detect RSDS schema version or manifest.")


def _get_codec(schema_version: int) -> RsdsCodec[Any]:
    try:
        return LOADERS[schema_version]
    except KeyError as exc:
        raise ValueError(f"Unsupported RSDS schema version: {schema_version}") from exc


def _read_dispatch_manifest(zf: ZipFile) -> Manifest:
    return ManifestSchema.model_validate_json(zf.read(MANIFEST_FILENAME)).root


def _read_legacy_manifest(zf: ZipFile) -> Manifest:
    legacy_version = zf.read(LEGACY_VERSION_FILENAME).decode().strip()

    if legacy_version == v1.LEGACY_VERSION:
        schema_version = 1
    else:
        raise ValueError(f"Unsupported legacy RSDS version: {legacy_version}")

    if schema_version == 1:
        return v1.ManifestV1(format="rsds", schema_version=1)

    raise ValueError(f"Unsupported legacy RSDS schema version: {schema_version}")


def _write_manifest_metadata(zf: ZipFile, manifest: Manifest) -> None:
    if isinstance(manifest, v1.ManifestV1):
        zf.writestr(LEGACY_VERSION_FILENAME, v1.LEGACY_VERSION)

    else:
        zf.writestr(MANIFEST_FILENAME, manifest.model_dump_json())
