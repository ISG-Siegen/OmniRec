import gzip
import pandas as pd

from .loader import Loader


class SteamAustralianReviews(Loader):
    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with gzip.open(f"{source_path}/australian_user_reviews.json.gz", 'rb') as file:
            data = []
            lines = file.readlines()
            for line in lines:
                line = eval(line.decode("utf-8"))
                user = line["user_id"]
                for review in line["reviews"]:
                    if review["recommend"]:
                        item_id = review["item_id"]
                        timestamp = review["posted"]
                        data.append([user, item_id, timestamp])
            return pd.DataFrame(data, columns=[user_column_name, item_column_name, timestamp_column_name])
