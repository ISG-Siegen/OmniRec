import tarfile
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("DianpingSocialRec")
class DianpingSocialRec(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://lihui.info/file/Dianping_SocialRec_2015.tar.bz2",
            "adcb6bffff16136a99e390cafd0f549a7e7f3028351e19886e9e3696b0722275",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        with tarfile.open(
            source_dir / "Dianping_SocialRec_2015.tar.bz2", "r:bz2"
        ) as tar:
            file = tar.extractfile("Dianping_SocialRec_2015/rating.txt")
            assert file is not None
            return pd.read_csv(
                file,
                header=None,
                sep="|",
                names=[
                    "user",
                    "item",
                    "rating",
                    "timestamp",
                ],
            )
