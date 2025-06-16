import zipfile
import pandas as pd

from .loader import Loader


class MovieLensLarge(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/ml-{additional_parameters['version']}.zip", 'r') as zipf:
            file = zipf.open(f"ml-{additional_parameters['version']}/ratings.csv")
            return pd.read_csv(file, sep=',', header=0,
                               names=[user_column_name, item_column_name, rating_column_name, timestamp_column_name])
