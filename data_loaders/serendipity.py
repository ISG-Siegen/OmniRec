import zipfile

import pandas as pd

from .loader import Loader


class Serendipity(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/serendipity-sac2018.zip", 'r') as zipf:
            data_train = pd.read_csv(zipf.open('serendipity-sac2018/training.csv'), sep=',', header=0,
                                     usecols=[0, 1, 2, 3],
                                     names=[user_column_name, item_column_name, rating_column_name,
                                            timestamp_column_name])
            data_answers = pd.read_csv(zipf.open('serendipity-sac2018/answers.csv'), sep=',', header=0,
                                       usecols=[0, 1, 2, 3],
                                       names=[user_column_name, item_column_name, rating_column_name,
                                              timestamp_column_name])
            return pd.concat([data_train, data_answers], axis=0, ignore_index=True)