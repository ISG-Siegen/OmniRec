import zipfile
import pandas as pd

from .loader import Loader


class EchoNest(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/train_triplets.txt.zip") as zipf:
            with zipf.open("train_triplets.txt") as file:
                return pd.read_csv(file, header=None, sep="\t", names=[user_column_name, item_column_name, "1"],
                                   usecols=[user_column_name, item_column_name])
