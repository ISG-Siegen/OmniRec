import pandas as pd
import py7zr

from .loader import Loader


class AlibabaIFashion(Loader):
    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        data = []
        with py7zr.SevenZipFile(f"{source_path}/user_data.txt.7z") as sevenzip_file:
            with sevenzip_file.read(["user_data.txt"])["user_data.txt"] as file:
                for line in file.readlines():
                    user, items, _ = line.decode("utf-8").split(",")
                    for item in items.split(";"):
                        data.append([user, item])
                return pd.DataFrame(data, columns=[user_column_name, item_column_name])
