import gzip
import json
import pandas as pd

from .loader import Loader


class Goodreads(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with gzip.open(f"{source_path}/goodreads_interactions_{additional_parameters['version']}.json.gz",
                       "rb") as file:
            file_data = []
            for line in file.readlines():
                line = json.loads(line.decode("utf-8"))
                if "user_id" in line and "book_id" in line and "rating" and "date_updated" in line:
                    file_data.append([line["user_id"], line["book_id"], line["rating"], line["date_updated"]])
            return pd.DataFrame(file_data,
                                columns=[user_column_name, item_column_name, rating_column_name, timestamp_column_name])
