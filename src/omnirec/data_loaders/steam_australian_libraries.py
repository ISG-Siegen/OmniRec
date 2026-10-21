import gzip
from ast import literal_eval
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("SteamAustralianLibraries")
class SteamAustralianLibraries(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://mcauleylab.ucsd.edu/public_datasets/data/steam/australian_users_items.json.gz",
            "0b329f79ddf450aba0aad923c8cb6d1affac0c98efaf70242d22fd10987a8d99",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> pd.DataFrame:
        with gzip.open(source_dir / "australian_users_items.json.gz", "rt") as file:
            data = []
            lines = file.readlines()
            for line in tqdm(lines):
                line = literal_eval(line)
                user = line["steam_id"]
                for item in line["items"]:
                    item_id = item["item_id"]
                    data.append([user, item_id])
            df = pd.DataFrame(data, columns=["user", "item"])
            return df
