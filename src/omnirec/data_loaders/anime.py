import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("Anime")
class Anime(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://www.kaggle.com/datasets/CooperUnion/anime-recommendations-database",
            "49595ab309d1d773ae66464379dc23d813466199816ae6b24e38bc73b8f2cd12",
            download_file_name="archive.zip",
            license_or_registration=True,
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        with zipfile.ZipFile(source_dir / "archive.zip") as zipf:
            with zipf.open("rating.csv") as file:
                data = pd.read_csv(file, header=0, names=["user", "item", "rating"])
                data.loc[data["rating"] == -1, "rating"] = np.nan
                return data
