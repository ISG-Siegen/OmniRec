import zipfile
import pandas as pd

from .loader import Loader


class TVAudience(Loader):
    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/tv-audience-dataset.zip") as zipf:
            return pd.read_csv(zipf.open("tv-audience-dataset/tv-audience-dataset.csv"), header=None, sep=",",
                               usecols=[5, 6], names=[user_column_name, item_column_name])
