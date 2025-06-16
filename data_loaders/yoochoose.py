import zipfile
import pandas as pd

from .loader import Loader


class Yoochoose(Loader):
    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/archive.zip", 'r') as zipf:
            data_train = pd.read_csv(zipf.open(f"yoochoose-clicks.dat"), header=None, sep=",", usecols=[0, 1, 2],
                                     names=[user_column_name, timestamp_column_name, item_column_name])
            data_test = pd.read_csv(zipf.open(f"yoochoose-test.dat"), header=None, sep=",", usecols=[0, 1, 2],
                                    names=[user_column_name, timestamp_column_name, item_column_name])
            return pd.concat([data_train, data_test], axis=0, ignore_index=True)
