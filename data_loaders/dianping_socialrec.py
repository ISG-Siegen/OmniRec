import tarfile
import pandas as pd

from .loader import Loader


class DianpingSocialRec(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with tarfile.open(f"{source_path}/Dianping_SocialRec_2015.tar.bz2", "r:bz2") as tar:
            with tar.extractfile("Dianping_SocialRec_2015/rating.txt") as file:
                return pd.read_csv(file, header=None, sep="|",
                                   names=[user_column_name, item_column_name, rating_column_name,
                                          timestamp_column_name])
