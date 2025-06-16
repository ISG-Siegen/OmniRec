import zipfile

import pandas as pd

from .loader import Loader


class InCarMusic(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/Music_InCarMusic.zip", "r") as zipf:
            return pd.read_excel(zipf.open("Music_InCarMusic/Data_InCarMusic.xlsx"), usecols=[0, 1, 2],
                                 names=[user_column_name, item_column_name, rating_column_name])
