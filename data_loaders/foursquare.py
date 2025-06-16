import zipfile
import pandas as pd

from .loader import Loader


class Foursquare(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/dataset_tsmc2014.zip") as zipf:
            with zipf.open(f"dataset_tsmc2014/dataset_TSMC2014_{additional_parameters['version']}.txt") as file:
                return pd.read_csv(file, sep="\t", header=None, encoding="latin-1",
                                   names=[user_column_name, item_column_name, "1", "2", "3", "4", "5",
                                          timestamp_column_name],
                                   usecols=[user_column_name, item_column_name, timestamp_column_name])
