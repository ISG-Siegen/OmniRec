import zipfile

import pandas as pd

from .loader import Loader


class Sketchfab(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/rec-a-sketch-master.zip", 'r') as zipf:
            return pd.read_csv(zipf.open(f"rec-a-sketch-master/data/model_likes_anon.psv"), sep="|", header=0,
                               usecols=[1, 2], names=[user_column_name, item_column_name])
