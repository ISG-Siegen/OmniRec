import zipfile
import pandas as pd

from .loader import Loader


class Diginetica(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/dataset-train-diginetica.zip") as zipf:
            with zipf.open("train-item-views.csv") as file:
                data = pd.read_csv(file, header=0, sep=";", usecols=["userId", "itemId", "eventdate"])
                data.rename(columns={"userId": user_column_name, "itemId": item_column_name,
                                     "eventdate": timestamp_column_name}, inplace=True)
                data = data[data[user_column_name].notna()]
                return data
