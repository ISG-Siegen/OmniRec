import pandas as pd

from .loader import Loader


class Behance(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        return pd.read_csv(f"{source_path}/Behance_appreciate_1M.gz", compression="gzip", header=None, sep=" ",
                           names=[user_column_name, item_column_name, timestamp_column_name])
