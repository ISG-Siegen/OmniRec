import zipfile
import pandas as pd

from .loader import Loader


class MyketAndroid(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/myket-android-application-market-dataset-main.zip", 'r') as zipf:
            file = zipf.open(f"myket-android-application-market-dataset-main/myket.csv")
            return pd.read_csv(file, sep=',', header=0, usecols=[0, 1, 2],
                               names=[user_column_name, item_column_name, timestamp_column_name])
