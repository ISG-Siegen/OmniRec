import tarfile
import pandas as pd

from .loader import Loader


class Librarything(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with tarfile.open(f"{source_path}/lthing_data.tar.gz", "r:gz") as tar:
            final_dict = {user_column_name: [], item_column_name: [], rating_column_name: [], timestamp_column_name: []}
            lines = tar.extractfile("lthing_data/reviews.txt").readlines()
            for line in lines[1:]:
                dic = eval(line.decode().split("')] = ")[1])
                if all(k in dic for k in ("user", "work", "stars", "unixtime")):
                    final_dict[user_column_name].append(dic['user'])
                    final_dict[item_column_name].append(dic['work'])
                    final_dict[rating_column_name].append(dic['stars'])
                    final_dict[timestamp_column_name].append(dic['unixtime'])
            return pd.DataFrame.from_dict(final_dict)
