import zipfile
import pandas as pd

from .loader import Loader


class Digg(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/digg_votes.zip", 'r') as zipf:
            return pd.read_csv(zipf.open("digg_votes1.csv", pwd=b"digg2009_user"), sep=",", header=None,
                               names=[timestamp_column_name, user_column_name, item_column_name])[
                [user_column_name, item_column_name, timestamp_column_name]]
