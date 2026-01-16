import zipfile
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("BookCrossing")
class BookCrossing(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://www.kaggle.com/api/v1/datasets/download/somnambwl/bookcrossing-dataset",
            "fc6d72288c8f3c20841175114ee1d3359a6b1dc1e6c65361284e1fb700a41bf7",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        with zipfile.ZipFile(source_dir / "bookcrossing-dataset") as zipf:
            with zipf.open("Ratings.csv") as file:
                df = pd.read_csv(file, sep=";")
                df.rename(
                    columns={"User-ID": "user", "ISBN": "item", "Rating": "rating"},
                    inplace=True,
                )
                return df
