import zipfile
import pandas as pd

from .loader import Loader


class FoursquareNYC1(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/dataset_ubicomp2013.zip") as zipf:
            with zipf.open("dataset_ubicomp2013/dataset_ubicomp2013_checkins.txt") as file:
                return pd.read_csv(file, sep="\t", header=None, names=[user_column_name, item_column_name])
