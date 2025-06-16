import zipfile

import pandas as pd

from .loader import Loader


class DoubanShort(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/archive.zip") as zipf:
            with zipf.open("DMSC.csv") as file:
                data = pd.read_csv(file, header=0, sep=",", usecols=['Username', 'Movie_Name_EN', 'Star', 'Date'])
                data.rename(columns={'Username': user_column_name, 'Movie_Name_EN': item_column_name,
                                     'Star': rating_column_name, 'Date': timestamp_column_name}, inplace=True)
                return data
