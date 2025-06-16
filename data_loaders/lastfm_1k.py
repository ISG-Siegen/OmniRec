import tarfile
import pandas as pd

from .loader import Loader


class LastFM1K(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with tarfile.open(f"{source_path}/lastfm-dataset-1K.tar.gz", "r:gz") as tar:
            return pd.read_csv(tar.extractfile("lastfm-dataset-1K/userid-timestamp-artid-artname-traid-traname.tsv"),
                               sep="\t", header=None, usecols=[0, 1, 4],
                               names=[user_column_name, timestamp_column_name, item_column_name])
