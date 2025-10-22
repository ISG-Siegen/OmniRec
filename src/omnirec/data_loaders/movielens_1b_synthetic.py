import tarfile
from pathlib import Path

import numpy as np
import pandas as pd
from pandas.core.api import DataFrame as DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("MovieLens1BSynthetic")
class MovieLens1BSynthetic(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://files.grouplens.org/datasets/movielens/ml-20mx16x32.tar",
            "a8c3fd4788659da7dac1ad15c335877f5da8b49eed9478e93072fc3c352325d5",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        filenames = [i for i in range(0, 16)]
        categories = ["train", "test"]
        dfs = []
        with tarfile.open(source_dir / "ml-20mx16x32.tar", "r") as tar:
            for category in categories:
                for filename in filenames:
                    npz_file_name = f"ml-20mx16x32/{category}x16x32_{filename}.npz"
                    npz_file = tar.extractfile(npz_file_name)
                    if npz_file is None:
                        raise ValueError(f'Could not extract "{npz_file_name}"')
                    data = np.load(npz_file)["arr_0"]
                    dfs.append(pd.DataFrame(data, columns=["user", "item"]))

        df = pd.concat(dfs, axis=0)
        df["rating"] = 1
        return df
