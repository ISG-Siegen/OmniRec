import zipfile
import pandas as pd

from .loader import Loader


class MovieLens100K(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/ml-100k.zip") as zipf:
            with zipf.open("ml-100k/u.data") as file:
                return pd.read_csv(file, sep="\t", names=[user_column_name, item_column_name, rating_column_name,
                                                          timestamp_column_name])
