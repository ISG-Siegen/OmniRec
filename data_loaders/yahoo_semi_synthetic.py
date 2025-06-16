import zipfile
import pandas as pd

from .loader import Loader


class YahooSemiSynthetic(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/yahoo.zip", 'r') as zipf:
            dfs = []
            file_names = [f"yahoo0{i}-0{j}" for i in [1, 5, 9] for j in [1, 5, 9]]
            for file_name in file_names:
                dfs.append(pd.read_csv(zipf.open(f"{file_name}"), delim_whitespace=True, header=None, usecols=[0, 1, 2],
                                       names=[user_column_name, item_column_name, rating_column_name]))
            return pd.concat(dfs, axis=0, ignore_index=True)
