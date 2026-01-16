import zipfile
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("CiaoDVD")
class CiaoDVD(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://guoguibing.github.io/librec/datasets/CiaoDVD.zip",
            "e36e06034dcf767f0f5cac120b03f262caef68cba86690e451571c13fa3236dd",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        with zipfile.ZipFile(source_dir / "CiaoDVD.zip") as zipf:
            with zipf.open("movie-ratings.txt") as file:
                return pd.read_csv(
                    file,
                    header=None,
                    sep=",",
                    names=[
                        "user",
                        "item",
                        "1",
                        "2",
                        "rating",
                        "timestamp",
                    ],
                    usecols=[
                        "user",
                        "item",
                        "rating",
                        "timestamp",
                    ],
                )
