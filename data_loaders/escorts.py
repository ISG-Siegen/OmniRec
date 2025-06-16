import pandas as pd

from .loader import Loader


class Escorts(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        return pd.read_csv(f"{source_path}/pcbi.1001109.s001.csv", skiprows=24, header=None, sep=";",
                           usecols=[0, 1, 2, 3],
                           names=[item_column_name, user_column_name, timestamp_column_name, rating_column_name])[
            [user_column_name, item_column_name, rating_column_name, timestamp_column_name]]
