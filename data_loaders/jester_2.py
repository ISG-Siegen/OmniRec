import zipfile
import pandas as pd

from .loader import Loader


class Jester2(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/jester_dataset_2.zip", "r") as zipf:
            data = pd.read_csv(zipf.open("jester_ratings.dat"), delim_whitespace=True, header=None,
                               names=[user_column_name, item_column_name, rating_column_name])
            data.dropna(subset=[rating_column_name], inplace=True)

            return data
