import zipfile
from pathlib import Path

import pandas as pd

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("SteamRecommendations")
class SteamRecommendations(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://www.kaggle.com/api/v1/datasets/download/antonkozyriev/game-recommendations-on-steam",
            "7620a48dbff9fdb53e08c06640fae6060189f458784df646835eff4f69c7995a",
            "archive.zip",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> pd.DataFrame:
        with zipfile.ZipFile(source_dir / "archive.zip", "r") as zipf:
            data = pd.read_csv(
                zipf.open("recommendations.csv"),
                sep=",",
                header=0,
                usecols=[0, 3, 4, 6],
                names=[
                    "item",
                    "timestamp",
                    "rating",
                    "user",
                ],
            )
            data = data[data["rating"]]
            return data
