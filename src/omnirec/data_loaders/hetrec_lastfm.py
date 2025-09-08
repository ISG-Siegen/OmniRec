import zipfile
from pathlib import Path

import pandas as pd

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("HetrecLastFM")
class HetrecLastFM(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://files.grouplens.org/datasets/hetrec2011/hetrec2011-lastfm-2k.zip",
            "6738f48195667ff03caaab4d32ca9a3133d8cc026b7c3cdaf6ce1010e913c59c",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> pd.DataFrame:
        with zipfile.ZipFile(source_dir / "hetrec2011-lastfm-2k.zip", "r") as zipf:
            data = pd.read_csv(
                zipf.open("user_taggedartists-timestamps.dat"),
                sep="\t",
                header=0,
                usecols=["userID", "artistID", "timestamp"],
            )
            data.rename(
                columns={
                    "userID": "user",
                    "artistID": "item",
                },
                inplace=True,
            )
            data["rating"] = 1
            return data
