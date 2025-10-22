from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("Behance")
class Behance(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://mcauleylab.ucsd.edu/public_datasets/gdrive/behance/Behance_appreciate_1M.gz",
            "b25b96fbfa913914b13c0c5ae38b196363d5791f2f87127bc3cdcfddb9d3d793",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        raise NotImplementedError(
            "Download file of behance seems to be corrupt currently."
        )
        df = pd.read_csv(
            source_dir / "Behance_appreciate_1M.gz",
            header=None,
            sep=" ",
            names=["user", "item", "timestamp"],
        )

        df["rating"] = 1
        return df
