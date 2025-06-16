import zipfile
import pandas as pd

from .loader import Loader


class LearningFromSets(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/learning-from-sets-2019.zip", "r") as zipf:
            return pd.read_csv(zipf.open("learning-from-sets-2019/item_ratings.csv"), header=0, sep=",",
                               names=[user_column_name, item_column_name, rating_column_name, timestamp_column_name])
