import zipfile
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("FilmTrust")
class FilmTrust(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://guoguibing.github.io/librec/datasets/filmtrust.zip",
            "de4a55cb4ae26f663d88e9ad1ba1fae2d0d6d7a7499e37dc5245bab470c2d13c",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        with zipfile.ZipFile(source_dir / "filmtrust.zip", "r") as zipf:
            with zipf.open("ratings.txt") as file:
                return pd.read_csv(
                    file,
                    header=None,
                    delim_whitespace=True,
                    names=["user", "item", "rating"],
                )
