import zipfile
import pandas as pd

from .loader import Loader


class NowplayingRS(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/nowplayingrs.zip", "r") as zipf:
            return pd.read_csv(zipf.open(f"user_track_hashtag_timestamp.csv"), header=0, sep=",",
                               usecols=[0, 1, 3], names=[user_column_name, item_column_name, timestamp_column_name])
