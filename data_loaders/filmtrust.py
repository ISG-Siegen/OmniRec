import zipfile
import pandas as pd

from .loader import Loader


class FilmTrust(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/filmtrust.zip", "r") as zipf:
            with zipf.open("ratings.txt") as file:
                return pd.read_csv(file, header=None, delim_whitespace=True,
                                   names=[user_column_name, item_column_name, rating_column_name])
