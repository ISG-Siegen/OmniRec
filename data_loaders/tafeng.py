import zipfile
import pandas as pd

from .loader import Loader


class TaFeng(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/archive.zip", 'r') as zipf:
            return pd.read_csv(zipf.open('ta_feng_all_months_merged.csv'), header=0, sep=',', usecols=[0, 1, 5],
                               names=[timestamp_column_name, user_column_name, item_column_name])[
                [user_column_name, item_column_name, timestamp_column_name]]
