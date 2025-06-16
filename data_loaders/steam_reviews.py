import gzip
import pandas as pd

from .loader import Loader


class SteamReviews(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with gzip.open(f"{source_path}/steam_reviews.json.gz", 'rb') as file:
            data = []
            lines = file.readlines()
            for line in lines:
                line = eval(line.decode("utf-8"))
                user = line["username"]
                item = line["product_id"]
                timestamp = line["date"]
                data.append([user, item, timestamp])
            return pd.DataFrame(data, columns=[user_column_name, item_column_name, timestamp_column_name])
