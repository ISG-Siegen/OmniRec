from pathlib import Path

import pandas as pd
from pandas.core.api import DataFrame as DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("Gowalla")
class Gowalla(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://snap.stanford.edu/data/loc-gowalla_totalCheckins.txt.gz",
            "c1c3e19effba649b6c89aeab3c1f9459fad88cfdc2b460fc70fd54e295d83ea0",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        df = pd.read_csv(
            source_dir / "loc-gowalla_totalCheckins.txt.gz",
            compression="gzip",
            names=[
                "user",
                "timestamp",
                "latitude",
                "longitude",
                "item",
            ],
            header=None,
            sep="\t",
        )
        df["rating"] = 1
        return df[["user", "item", "rating", "timestamp"]]
