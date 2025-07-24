from pathlib import Path
from zipfile import ZipFile

import pandas as pd

from recsyslib.data_loaders.base import DatasetInfo, Loader
from recsyslib.data_loaders.registry import _loader


@_loader("MovieLens100K")
class MovieLens100K(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://files.grouplens.org/datasets/movielens/ml-100k.zip",
            "50d2a982c66986937beb9ffb3aa76efe955bf3d5c6b761f4e3a7cd717c6a3229",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> pd.DataFrame:
        with ZipFile(f"{source_dir}/ml-100k.zip") as zipf:
            with zipf.open("ml-100k/u.data") as file:
                return pd.read_csv(
                    file,
                    sep="\t",
                    names=[
                        "user",
                        "item",
                        "rating",
                        "timestamp",
                    ],
                )
