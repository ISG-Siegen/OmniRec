import pandas as pd

from .loader import Loader


class RentTheRunway(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        data = pd.read_json(f"{source_path}/renttherunway_final_data.json.gz", lines=True, compression='gzip')[
            ["user_id", "item_id", "rating", "review_date"]]
        data.rename(columns={'user_id': user_column_name, 'item_id': item_column_name, 'rating': rating_column_name,
                             'review_date': timestamp_column_name}, inplace=True)
        return data
