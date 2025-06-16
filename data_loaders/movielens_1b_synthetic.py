import tarfile
import numpy as np
import pandas as pd

from .loader import Loader


class MovieLens1BSynthetic(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        filenames = [i for i in range(0, 16)]
        categories = ["train", "test"]
        dfs = []
        with tarfile.open(f"{source_path}/ml-20mx16x32.tar", 'r') as tar:
            for category in categories:
                for filename in filenames:
                    data = np.load(tar.extractfile(f"ml-20mx16x32/{category}x16x32_{filename}.npz"))["arr_0"]
                    dfs.append(pd.DataFrame(data, columns=[user_column_name, item_column_name]))
            return pd.concat(dfs, axis=0)
