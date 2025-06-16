import tarfile
import pandas as pd

from .loader import Loader


class YahooMusic1(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with tarfile.open(f"{source_path}/dataset.tgz", "r") as tar:
            data = pd.read_csv(tar.extractfile("./ydata-ymusic-user-artist-ratings-v1_0.txt.gz"), sep="\t",
                               compression="gzip",
                               header=None, usecols=[0, 1, 2],
                               names=[user_column_name, item_column_name, rating_column_name])

            data.loc[data["rating"] == 255, ["rating"]] = 0
            return data
