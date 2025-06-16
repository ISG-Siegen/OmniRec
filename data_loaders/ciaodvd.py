import zipfile
import pandas as pd

from .loader import Loader


class CiaoDVD(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/CiaoDVD.zip") as zipf:
            with zipf.open("movie-ratings.txt") as file:
                return pd.read_csv(file, header=None, sep=',',
                                   names=[user_column_name, item_column_name, "1", "2",
                                          rating_column_name, timestamp_column_name],
                                   usecols=[user_column_name, item_column_name, rating_column_name,
                                            timestamp_column_name])
