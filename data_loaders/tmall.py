import zipfile
import pandas as pd

from .loader import Loader


class Tmall(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/IJCAI16_data.zip") as zipf:
            return pd.read_csv(zipf.open("ijcai2016_taobao.csv"), header=0, sep=",", usecols=[0, 2, 5],
                               names=[user_column_name, item_column_name, timestamp_column_name])
