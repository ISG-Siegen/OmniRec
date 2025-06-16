import pandas as pd

from .loader import Loader


class EpinionsExtended(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        return pd.read_csv(f"{source_path}/epinions-extended.txt", header=None, sep='\t',
                           names=[item_column_name, user_column_name, rating_column_name, "1", timestamp_column_name,
                                  "2", "3", "4"])[[user_column_name, item_column_name,
                                                   rating_column_name, timestamp_column_name]]
