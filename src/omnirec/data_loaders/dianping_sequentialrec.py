import tarfile
from pathlib import Path

import numpy as np
import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("DianpingSequentialRec")
class DianpingSequentialRec(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://lihui.info/file/Dianping_SequentialRec.tar.bz2",
            "d6c72dfcf89cab73cd8413ff226b051d3170169c8e6db5216827e5b779e7dc48",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        with tarfile.open(
            source_dir / "Dianping_SequentialRec.tar.bz2", "r:bz2"
        ) as tar:
            file = tar.extractfile("Dianping_SequentialRec/actions.txt")
            assert file is not None

            data = pd.read_csv(
                file,
                header=None,
                sep=",",
                names=[
                    "user",
                    "item",
                    "rating",
                    "timestamp",
                    "1",
                ],
                usecols=[
                    "user",
                    "item",
                    "rating",
                    "timestamp",
                ],
            )
            data.loc[data["rating"] == "-", "rating"] = np.nan
            data = data.astype({"rating": np.float64})
            return data
