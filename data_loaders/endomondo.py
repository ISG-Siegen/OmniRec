import gzip
import pandas as pd

from .loader import Loader


class EndoMondo(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with gzip.open(f"{source_path}/endomondoHR.json.gz", "r") as gz:
            file = gz.readlines()
            final_dict = {user_column_name: [], item_column_name: [], timestamp_column_name: []}
            for line in file:
                dic = eval(line)
                if all(k in dic for k in ("userId", "sport", "timestamp")):
                    final_dict[user_column_name].append(dic['userId'])
                    final_dict[item_column_name].append(dic['sport'])
                    final_dict[timestamp_column_name].append(sum(dic['timestamp']) / len(dic['timestamp']))
            return pd.DataFrame.from_dict(final_dict)
