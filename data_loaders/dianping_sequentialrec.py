import tarfile
import numpy as np
import pandas as pd

from .loader import Loader


class DianpingSequentialRec(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with tarfile.open(f"{source_path}/Dianping_SequentialRec.tar.bz2", "r:bz2") as tar:
            with tar.extractfile("Dianping_SequentialRec/actions.txt") as file:
                data = pd.read_csv(file, header=None, sep=",",
                                   names=[user_column_name, item_column_name,
                                          rating_column_name, timestamp_column_name, "1"],
                                   usecols=[user_column_name, item_column_name,
                                            rating_column_name, timestamp_column_name])
                data.loc[data[rating_column_name] == "-", rating_column_name] = np.nan
                data = data.astype({rating_column_name: np.float64})
                return data
