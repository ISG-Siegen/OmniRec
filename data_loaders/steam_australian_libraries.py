import gzip
import pandas as pd

from .loader import Loader


class SteamAustralianLibraries(Loader):
    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with gzip.open(f"{source_path}/australian_users_items.json.gz", 'rb') as file:
            data = []
            lines = file.readlines()
            for line in lines:
                line = eval(line.decode("utf-8"))
                user = line["steam_id"]
                for item in line["items"]:
                    item_id = item["item_id"]
                    data.append([user, item_id])
            return pd.DataFrame(data, columns=[user_column_name, item_column_name])
