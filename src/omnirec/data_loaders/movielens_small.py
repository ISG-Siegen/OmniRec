import zipfile
from pathlib import Path

import pandas as pd
from pandas.core.api import DataFrame as DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader

name_to_filenames = {
    "MovieLens1M": ("1m", "1m"),
    "MovieLens10M": ("10m", "10M100K"),
}


def name_err(name: str) -> ValueError:
    return ValueError(f'Unknown dataset name "{name}" for MovieLensSmall dataloader!')


@_loader(["MovieLens1M", "MovieLens10M"])
class MovieLensSmall(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        if name == "MovieLens1M":
            return DatasetInfo(
                "https://files.grouplens.org/datasets/movielens/ml-1m.zip",
                "a6898adb50b9ca05aa231689da44c217cb524e7ebd39d264c56e2832f2c54e20",
            )
        elif name == "MovieLens10M":
            return DatasetInfo(
                "https://files.grouplens.org/datasets/movielens/ml-10m.zip",
                "813c411ccb6122564edfe752e7f80c4dcc5aa25fa94c93622f6877a7ba252862",
            )
        else:
            raise name_err(name)

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        filenames = name_to_filenames.get(name)
        if filenames is None:
            raise name_err(name)
        with zipfile.ZipFile(source_dir / f"ml-{filenames[0]}.zip", "r") as zipf:
            file = zipf.open(f"ml-{filenames[1]}/ratings.dat")
            return pd.read_csv(
                file,
                sep="::",
                header=None,
                engine="python",
                names=[
                    "user",
                    "item",
                    "rating",
                    "timestamp",
                ],
            )
