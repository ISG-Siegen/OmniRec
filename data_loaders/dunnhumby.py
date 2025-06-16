import zipfile

import pandas as pd

from .loader import Loader


class Dunnhumby(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/archive.zip", "r") as zipf:
            data = pd.read_csv(zipf.open("transaction_data.csv"), sep=",", header=0,
                               usecols=["household_key", "PRODUCT_ID", "DAY", "TRANS_TIME"])

            data["DAY"] = data["DAY"] * 24 * 3600

            def convert_time_to_milliseconds(x):
                x = str(x)
                if 0 < len(x) < 3:
                    hours = "0"
                    minutes = x
                elif len(x) == 3:
                    hours = x[0]
                    minutes = x[1:]
                elif len(x) == 4:
                    hours = x[:2]
                    minutes = x[2:]
                else:
                    return -1

                return int(hours) * 3600 + int(minutes) * 60

            data["TRANS_TIME"] = data["TRANS_TIME"].apply(lambda x: convert_time_to_milliseconds(x))

            data[timestamp_column_name] = data["DAY"] + data["TRANS_TIME"]

            data.rename(columns={"household_key": user_column_name, "PRODUCT_ID": item_column_name}, inplace=True)

            return data[[user_column_name, item_column_name, timestamp_column_name]]
