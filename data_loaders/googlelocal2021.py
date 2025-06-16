from pathlib import Path

import pandas as pd

from .loader import Loader


class GoogleLocal2021(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        rating_archive = next(Path.iterdir(Path(source_path)))
        return pd.read_csv(rating_archive, compression="gzip", sep=",", header=0,
                           names=[item_column_name, user_column_name, rating_column_name, timestamp_column_name])[
            [user_column_name, item_column_name, rating_column_name, timestamp_column_name]]
