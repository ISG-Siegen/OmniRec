import tarfile
import pandas as pd

from .loader import Loader


class YahooMusic2(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):

        def read_file(file):
            return pd.read_csv(file, sep="\t", header=None, usecols=[0, 1, 2],
                               names=[user_column_name, item_column_name, rating_column_name])

        dfs = []
        with tarfile.open(f"{source_path}/dataset-1.tgz", "r") as tar:
            rating_files_1 = [f"test_{i}.txt" for i in range(0, 10)] + [f"train_{i}.txt" for i in range(0, 5)]

            for rating_file in rating_files_1:
                dfs.append(read_file(tar.extractfile(f"ydata-ymusic-user-song-ratings-meta-v1_0/{rating_file}")))

        with tarfile.open(f"{source_path}/dataset-2.tgz", "r") as tar:
            rating_files_2 = [f"train_{i}.txt" for i in range(5, 10)]
            for rating_file in rating_files_2:
                dfs.append(read_file(tar.extractfile(f"ydata-ymusic-user-song-ratings-meta-v1_0/{rating_file}")))

        return pd.concat(dfs, axis=0, ignore_index=True)
