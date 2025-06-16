import zipfile
import pandas as pd

from .loader import Loader


class HetrecDelicious(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/hetrec2011-delicious-2k.zip", "r") as zipf:
            data = pd.read_csv(zipf.open("user_taggedbookmarks-timestamps.dat"), sep="\t", header=0,
                               usecols=["userID", "bookmarkID", "timestamp"])
            data.rename(columns={"userID": user_column_name, "bookmarkID": item_column_name,
                                 "timestamp": timestamp_column_name}, inplace=True)
            return data
