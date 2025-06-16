import zipfile
import pandas as pd

from .loader import Loader


class MarketBias(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/marketBias-master.zip", "r") as zipf:
            return pd.read_csv(zipf.open(f"marketBias-master/data/df_{additional_parameters['version']}.csv"), sep=",",
                               header=0, usecols=[0, 1, 2, 3],
                               names=[user_column_name, item_column_name, rating_column_name, timestamp_column_name])
