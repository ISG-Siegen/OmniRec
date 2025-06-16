import zipfile

import pandas as pd

from .loader import Loader


class InstaCart(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/archive.zip", "r") as zipf:
            prior_order = pd.read_csv(zipf.open("order_products__prior.csv"), sep=",", header=0,
                                      usecols=["order_id", "product_id"])
            train_order = pd.read_csv(zipf.open("order_products__train.csv"), sep=",", header=0,
                                      usecols=["order_id", "product_id"])
            full_order = pd.concat([prior_order, train_order])
            orders = pd.read_csv(zipf.open("orders.csv"), sep=",", header=0, usecols=["order_id", "user_id"])

            data = pd.merge(full_order, orders, on="order_id")

            data.rename(columns={"user_id": user_column_name, "product_id": item_column_name}, inplace=True)

            return data[[user_column_name, item_column_name]]
