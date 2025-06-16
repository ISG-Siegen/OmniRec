import zipfile
import pandas as pd

from .loader import Loader


class Rekko(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/rekko_challenge_2019.zip", 'r') as zipf:
            return pd.read_csv(zipf.open('ratings.csv'), sep=',', header=0,
                               names=[user_column_name, item_column_name, rating_column_name, timestamp_column_name])
