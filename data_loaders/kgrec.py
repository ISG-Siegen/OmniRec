import zipfile
import pandas as pd

from .loader import Loader


class KGRec(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/KGRec-dataset.zip", "r") as zipf:
            return pd.read_csv(zipf.open(f"KGRec-dataset/KGRec-{additional_parameters['version']}"),
                               delim_whitespace=True, header=None, usecols=[0, 1],
                               names=[user_column_name, item_column_name])
