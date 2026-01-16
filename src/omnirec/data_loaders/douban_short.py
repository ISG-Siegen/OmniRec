import zipfile
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("DoubanShort")
class DoubanShort(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://www.kaggle.com/api/v1/datasets/download/utmhikari/doubanmovieshortcomments",
            "ab9e933b6531851bcf2848f25bb142a782f55e20c30bba9c796f419b746bf6e6",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        with zipfile.ZipFile(source_dir / "doubanmovieshortcomments") as zipf:
            with zipf.open("DMSC.csv") as file:
                data = pd.read_csv(
                    file,
                    sep=",",
                    usecols=["Username", "Movie_Name_EN", "Star", "Date"],
                )
                data.rename(
                    columns={
                        "Username": "user",
                        "Movie_Name_EN": "item",
                        "Star": "rating",
                        "Date": "timestamp",
                    },
                    inplace=True,
                )
                return data
