import zipfile
from pathlib import Path

import pandas as pd
from pandas.core.api import DataFrame as DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader

name_to_filename = {
    "MovieLens20M": "20m",
    "MovieLens25M": "25m",
    "MovieLensLatest": "latest",
    "MovieLensLatestSmall": "latest-small",
}


def name_err(name: str) -> ValueError:
    return ValueError(f'Unknown dataset name "{name}" for MovieLensLarge dataloader!')


@_loader(
    [
        "MovieLens20M",
        "MovieLens25M",
        "MovieLensLatest",
        "MovieLensLatestSmall",
    ]
)
class MovieLensLarge(Loader):
    @staticmethod
    def raise_name_err(name: str):
        raise

    @staticmethod
    def info(name: str) -> DatasetInfo:
        if name == "MovieLens20M":
            return DatasetInfo(
                "https://files.grouplens.org/datasets/movielens/ml-20m.zip",
                "96f243c338a8665f6bcc89c53edf6ee39162a846940de6b7c8c48aeada765ff3",
            )
        elif name == "MovieLens25M":
            return DatasetInfo(
                "https://files.grouplens.org/datasets/movielens/ml-25m.zip",
                "8b21cfb7eb1706b4ec0aac894368d90acf26ebdfb6aced3ebd4ad5bd1eb9c6aa",
            )
        elif name == "MovieLensLatest":
            return DatasetInfo(
                "https://files.grouplens.org/datasets/movielens/ml-latest.zip",
                "66a9e518c747d76b241d9a859b001a2619d3ed1672ceef599eb50daf73a7b4a3",
            )
        elif name == "MovieLensLatestSmall":
            return DatasetInfo(
                "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip",
                "696d65a3dfceac7c45750ad32df2c259311949efec81f0f144fdfb91ebc9e436",
            )
        else:
            raise name_err(name)

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        filename = name_to_filename.get(name)
        if filename is None:
            raise name_err(name)
        with zipfile.ZipFile(source_dir / f"ml-{filename}.zip", "r") as zipf:
            file = zipf.open(f"ml-{filename}/ratings.csv")
            return pd.read_csv(
                file,
                sep=",",
                header=0,
                names=[
                    "user",
                    "item",
                    "rating",
                    "timestamp",
                ],
            )
