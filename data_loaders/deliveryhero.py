import zipfile
import pandas as pd

from .loader import Loader


class DeliveryHero(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/data_{additional_parameters['version']}.zip") as zipf:
            with zipf.open(
                    f"data_{additional_parameters['version']}/orders_{additional_parameters['version']}.txt") as file:
                df = pd.read_csv(file, header=0, sep=",",
                                 usecols=["customer_id", "product_id", "order_time", "order_day"])

                def convert_time_to_milliseconds(x):
                    if len(x.split(":")) == 3:
                        hours, minutes, seconds = x.split(":")
                        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
                    else:
                        return -1

                def convert_days_to_milliseconds(x):
                    if len(x.split(" ")) == 2:
                        days, _ = x.split(" ")
                        return int(days) * 24 * 3600
                    else:
                        return -1

                df["order_time"] = df["order_time"].apply(lambda x: convert_time_to_milliseconds(x))
                df["order_day"] = df["order_day"].apply(lambda x: convert_days_to_milliseconds(x))

                df[timestamp_column_name] = df["order_time"] + df["order_day"]

                df.rename(columns={"customer_id": user_column_name, "product_id": item_column_name}, inplace=True)

                return df[[user_column_name, item_column_name, timestamp_column_name]]
