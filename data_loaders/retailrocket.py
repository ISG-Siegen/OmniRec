import zipfile
import pandas as pd

from .loader import Loader


class Retailrocket(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/archive.zip", "r") as zipf:
            data = pd.read_csv(zipf.open("events.csv"), header=0, sep=",", usecols=["visitorid", "itemid", "event"])
            data = data[data["event"] == "view"]
            data.rename(columns={"visitorid": user_column_name, "itemid": item_column_name}, inplace=True)
            return data.drop(columns=["event"])
