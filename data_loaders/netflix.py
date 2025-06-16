import zipfile
import pandas as pd

from .loader import Loader


class Netflix(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/archive.zip", 'r') as zipf:
            filenames = ["combined_data_1.txt", "combined_data_2.txt", "combined_data_3.txt", "combined_data_4.txt"]
            dfs = []
            for filename in filenames:
                this_data = []
                with zipf.open(filename) as file:
                    for num, line in enumerate(file):
                        line = line.decode("utf-8").strip()
                        if line.endswith(':'):
                            current_item = line[:-1]
                        else:
                            user, rating, timestamp = line.split(',')
                            this_data.append([user, current_item, rating, timestamp])
                    dfs.append(pd.DataFrame(this_data, columns=[user_column_name, item_column_name, rating_column_name,
                                                                timestamp_column_name]))
            return pd.concat(dfs, axis=0)
