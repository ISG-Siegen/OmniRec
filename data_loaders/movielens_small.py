import zipfile
import pandas as pd

from .loader import Loader


class MovieLensSmall(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        if additional_parameters["version"] == "1m":
            with zipfile.ZipFile(f"{source_path}/ml-1m.zip", 'r') as zipf:
                file = zipf.open('ml-1m/ratings.dat')
        elif additional_parameters["version"] == "10m":
            with zipfile.ZipFile(f"{source_path}/ml-10m.zip", 'r') as zipf:
                file = zipf.open('ml-10M100K/ratings.dat')

        return pd.read_csv(file, sep='::', header=None, engine='python',
                           names=[user_column_name, item_column_name, rating_column_name, timestamp_column_name])
