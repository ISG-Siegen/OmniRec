import zipfile
import pandas as pd

from .loader import Loader


class TaobaoUserBehavior(Loader):
    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/UserBehavior.csv.zip", 'r') as zipf:
            data = pd.read_csv(zipf.open('UserBehavior.csv'), header=None, sep=",", usecols=[0, 1, 3, 4],
                               names=[user_column_name, item_column_name, rating_column_name, timestamp_column_name])
            return data[data[rating_column_name] == "pv"].drop(columns=[rating_column_name])[
                [user_column_name, item_column_name, timestamp_column_name]]
