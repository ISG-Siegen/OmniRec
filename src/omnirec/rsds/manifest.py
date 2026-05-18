from pydantic import BaseModel, ConfigDict


class ManifestBase[Version: int](BaseModel):
    model_config = ConfigDict(frozen=True)

    format: str
    schema_version: Version
