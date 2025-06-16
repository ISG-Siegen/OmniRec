import tarfile
import pandas as pd

from .loader import Loader


class YahooMusic3(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with tarfile.open(f"{source_path}/dataset.tgz", "r") as tar:
            data_train = pd.read_csv(tar.extractfile("./ydata-ymusic-rating-study-v1_0-train.txt"), sep="\t",
                                     header=None, names=[user_column_name, item_column_name, rating_column_name])
            data_test = pd.read_csv(tar.extractfile("./ydata-ymusic-rating-study-v1_0-test.txt"), sep="\t",
                                    header=None, names=[user_column_name, item_column_name, rating_column_name])
            return pd.concat([data_train, data_test], axis=0, ignore_index=True)
