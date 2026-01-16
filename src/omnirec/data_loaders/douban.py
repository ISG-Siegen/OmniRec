import tarfile
from pathlib import Path

import numpy as np
import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader(["DoubanBook", "DoubanMovie", "DoubanMusic"])
class Douban(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://www.dropbox.com/scl/fi/9zoykjl7km4wlrddscqrf/Douban.tar.gz?dl=1&e=2&rlkey=i6w593rb3m8p8u13znp9mq1t3",
            "8c2106750f457c8770d125718041f518ab088b6f8696c21c5e1764d85ff6a993",
            "Douban.tar.gz",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        if name == "DoubanBook":
            version = "book"
        elif name == "DoubanMovie":
            version = "movie"
        elif name == "DoubanMusic":
            version = "music"
        else:
            raise ValueError(f'Unknown dataset name "{name}" for Douban dataloader!')

        with tarfile.open(source_dir / "Douban.tar.gz") as tar:
            file = tar.extractfile(f"Douban/{version}/douban_{version}.tsv")
            assert file is not None

            data = pd.read_csv(
                file,
                header=0,
                sep="\t",
            )
            data.rename(
                columns={
                    "UserId": "user",
                    "ItemId": "item",
                    "Rating": "rating",
                    "Timestamp": "timestamp",
                },
                inplace=True,
            )
            data.loc[data["rating"] == -1, "rating"] = np.nan
            return data
