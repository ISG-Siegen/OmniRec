import pandas as pd

from .loader import Loader


class EachMovie(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        return pd.read_csv(f"{source_path}/eachmovie_triple.gz", compression="gzip", delim_whitespace=True,
                           header=None, names=[user_column_name, item_column_name, rating_column_name])
