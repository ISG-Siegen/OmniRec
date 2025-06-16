import zipfile
import pandas as pd

from .loader import Loader


class CosmeticsShop(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        data = []
        with zipfile.ZipFile(f"{source_path}/archive.zip") as zipf:
            for file in ["2019-Dec.csv", "2019-Nov.csv", "2019-Oct.csv", "2020-Feb.csv", "2020-Jan.csv"]:
                with zipf.open(file) as month:
                    df = pd.read_csv(month, usecols=["user_id", "product_id", "event_type"], header=0, sep=",")
                    df.rename(columns={"user_id": user_column_name, "product_id": item_column_name}, inplace=True)
                    df = df[df["event_type"] == "view"][["user", "item"]].copy()
                    data.append(df)
            return pd.concat(data)
