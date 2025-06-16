import zipfile

import pandas as pd

from .loader import Loader


class Globo(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        data = []
        with zipfile.ZipFile(f"{source_path}/archive.zip") as zipf:
            filenames = [f"clicks_hour_{str(i).zfill(3)}.csv" for i in range(385)]
            for filename in filenames:
                with zipf.open(f"clicks/clicks/{filename}") as file:
                    hour = pd.read_csv(file, sep=",", header=0,
                                       usecols=["user_id", "click_article_id", "click_timestamp"])
                    hour.rename(columns={"user_id": user_column_name, "click_article_id": item_column_name,
                                         "click_timestamp": timestamp_column_name}, inplace=True)
                    if hour.shape[0] == 0:
                        continue
                    else:
                        data.append(hour)
            return pd.concat(data)
