import gzip
from ast import literal_eval
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("GoogleLocal2018")
class GoogleLocal2018(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://mcauleylab.ucsd.edu/public_datasets/data/googlelocal/reviews.clean.json.gz",
            "c1e9e29f746d3165bf048bad94f7db824f186c1f5a4c515fd163e9112d217081",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        with gzip.open(source_dir / "reviews.clean.json.gz", "rt") as file:
            file_data = []
            for line in file.readlines():
                line = literal_eval(line)
                if (
                    "gPlusUserId" in line
                    and "gPlusPlaceId" in line
                    and "rating"
                    and "unixReviewTime" in line
                ):
                    file_data.append(
                        [
                            line["gPlusUserId"],
                            line["gPlusPlaceId"],
                            line["rating"],
                            line["unixReviewTime"],
                        ]
                    )
            return pd.DataFrame(
                file_data,
                columns=[
                    "user",
                    "item",
                    "rating",
                    "timestamp",
                ],
            )
