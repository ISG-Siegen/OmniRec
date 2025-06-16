import zipfile
import numpy as np
import pandas as pd

from .loader import Loader


class Anime(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/archive.zip") as zipf:
            with zipf.open("rating.csv") as file:
                data = pd.read_csv(file, header=0, names=[user_column_name, item_column_name, rating_column_name])
                data.loc[data[rating_column_name] == -1, rating_column_name] = np.nan
                return data
