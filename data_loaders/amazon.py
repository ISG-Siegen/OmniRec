from pathlib import Path
import pandas as pd

from .loader import Loader


class Amazon(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        rating_file = next(Path.iterdir(Path(source_path)))
        return pd.read_csv(rating_file, header=None, sep=",",
                           names=[user_column_name, item_column_name, rating_column_name, timestamp_column_name])
