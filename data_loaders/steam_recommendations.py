import zipfile
import pandas as pd

from .loader import Loader


class SteamRecommendations(Loader):
    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/archive.zip", 'r') as zipf:
            data = pd.read_csv(zipf.open(f"recommendations.csv"), sep=",", header=0, usecols=[0, 3, 4, 6],
                               names=[item_column_name, timestamp_column_name, rating_column_name, user_column_name])
            return data[data[rating_column_name]].drop(columns=[rating_column_name])[
                [user_column_name, item_column_name, timestamp_column_name]]
