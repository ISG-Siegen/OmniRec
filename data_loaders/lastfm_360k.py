import tarfile
import pandas as pd

from .loader import Loader


class LastFM360K(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with tarfile.open(f"{source_path}/lastfm-dataset-360K.tar.gz", "r:gz") as tarf:
            return pd.read_csv(tarf.extractfile("lastfm-dataset-360K/usersha1-artmbid-artname-plays.tsv"),
                               sep="\t", header=None, usecols=[0, 1],
                               names=[user_column_name, item_column_name])
