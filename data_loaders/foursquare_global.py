import zipfile
import pandas as pd

from .loader import Loader


class FoursquareGlobal(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        def _read_file(file_obj):
            return pd.read_csv(file_obj, sep="\t", header=None,
                               names=[user_column_name, item_column_name, timestamp_column_name, "1"],
                               usecols=[user_column_name, item_column_name, timestamp_column_name])

        if additional_parameters['version'] == "TIST2015":
            with zipfile.ZipFile(f"{source_path}/dataset_TIST2015.zip") as zipf:
                with zipf.open("dataset_TIST2015_Checkins.txt") as file:
                    return _read_file(file)
        elif additional_parameters['version'] == "WWW2019":
            with zipfile.ZipFile(f"{source_path}/dataset_WWW2019.zip") as zipf:
                with zipf.open("dataset_WWW2019/dataset_WWW_Checkins_anonymized.txt") as file:
                    return _read_file(file)
