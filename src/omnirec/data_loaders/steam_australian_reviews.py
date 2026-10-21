import gzip
from ast import literal_eval
from pathlib import Path

import pandas as pd

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("SteamAustralianReviews")
class SteamAustralianReviews(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://mcauleylab.ucsd.edu/public_datasets/data/steam/australian_user_reviews.json.gz",
            "a934bf74d8579bb25bc7bf24e652a87e2ccc91064e429a4cb4af5809178687a8",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> pd.DataFrame:
        with gzip.open(source_dir / "australian_user_reviews.json.gz", "rt") as file:
            data = []
            lines = file.readlines()
            for line in lines:
                line = literal_eval(line)
                user = line["user_id"]
                for review in line["reviews"]:
                    if review["recommend"]:
                        item_id = review["item_id"]
                        timestamp = review["posted"]
                        data.append([user, item_id, timestamp])

            df = pd.DataFrame(
                data,
                columns=["user", "item", "timestamp"],
            )
            return df
