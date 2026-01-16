import gzip
from ast import literal_eval
from pathlib import Path

import pandas as pd

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("SteamReviews")
class SteamReviews(Loader):
    @staticmethod
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://cseweb.ucsd.edu/~wckang/steam_reviews.json.gz",
            "40c6343deedf488689987749c5f8435233da48c163fbaa2a7766c215d584bc61",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> pd.DataFrame:
        with gzip.open(source_dir / "steam_reviews.json.gz", "rb") as file:
            data = []
            lines = file.readlines()
            for line in lines:
                line = literal_eval(line.decode("utf-8"))
                user = line["username"]
                item = line["product_id"]
                timestamp = line["date"]
                data.append([user, item, timestamp])
            df = pd.DataFrame(
                data,
                columns=["user", "item", "timestamp"],
            )
            df["rating"] = 1
            return df
