import zipfile
import pandas as pd

from .loader import Loader


class Reddit(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/archive.zip", "r") as zipf:
            return pd.read_csv(zipf.open("44_million_reddit_votes/44_million_votes.txt"), sep="\t",
                               header=0, usecols=[0, 2, 3],
                               names=[item_column_name, timestamp_column_name, user_column_name])
