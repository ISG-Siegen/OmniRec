import zipfile
import pandas as pd

from .loader import Loader


class LastFM1B(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/LFM-1b.zip", "r") as zipf:
            return pd.read_csv(zipf.open("LFM-1b_LEs.txt"), sep="\t", header=None, usecols=[0, 3, 4],
                               names=[user_column_name, item_column_name, timestamp_column_name])
