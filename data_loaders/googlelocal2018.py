import gzip
import pandas as pd

from .loader import Loader


class GoogleLocal2018(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with gzip.open(f"{source_path}/reviews.clean.json.gz", "rb") as file:
            file_data = []
            for line in file.readlines():
                line = eval(line.decode("utf-8"))
                if "gPlusUserId" in line and "gPlusPlaceId" in line and "rating" and "unixReviewTime" in line:
                    file_data.append(
                        [line["gPlusUserId"], line["gPlusPlaceId"], line["rating"], line["unixReviewTime"]])
            return pd.DataFrame(file_data,
                                columns=[user_column_name, item_column_name, rating_column_name, timestamp_column_name])
