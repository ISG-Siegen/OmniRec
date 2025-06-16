import zipfile
import pandas as pd

from .loader import Loader


class AlibabaMobile(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/tianchi_mobile_recommend_train_user.zip", "r") as zipf:
            data = pd.read_csv(zipf.open("tianchi_mobile_recommend_train_user.csv"), sep=",", header=0,
                               usecols=["user_id", "item_id", "time"])
            data.rename(
                columns={"user_id": user_column_name, "item_id": item_column_name, "time": timestamp_column_name},
                inplace=True)
            return data
