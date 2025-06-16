import zipfile

import pandas as pd

from .loader import Loader


class IPinYou(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/archive.zip", "r") as zipf:
            dfs = []
            file_names_s1 = [f"training1st/imp.201303{i}.txt.bz2" for i in range(11, 18)]
            file_names_s2 = [f"training2nd/imp.20130{i}.txt.bz2" for i in range(606, 613)]
            file_names_s3 = [f"training3rd/imp.201310{i}.txt.bz2" for i in range(19, 28)]
            file_names = file_names_s1 + file_names_s2 + file_names_s3
            for file_name in file_names:
                dfs.append(pd.read_csv(zipf.open(f"ipinyou.contest.dataset/{file_name}"), sep="\t",
                                       header=None, compression="bz2", usecols=[1, 3, 18],
                                       names=[timestamp_column_name, user_column_name, item_column_name]))
            return pd.concat(dfs, axis=0)
