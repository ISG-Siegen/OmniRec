import zipfile

import numpy as np
import pandas as pd

from .loader import Loader


class MIND(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        file_endings = []
        if additional_parameters['version'] == "large":
            file_endings = ["train", "dev", "test"]
        elif additional_parameters['version'] == "small":
            file_endings = ["train", "dev"]

        file_names = [f"MIND{additional_parameters['version']}_{file_ending}.zip" for file_ending in file_endings]

        dfs = []
        for file_name in file_names:
            with zipfile.ZipFile(f"{source_path}/{file_name}", 'r') as zipf:
                data = pd.read_csv(zipf.open(f"behaviors.tsv"), sep="\t", header=None,
                                   usecols=[1, 3, 4], names=[user_column_name, "history", "impressions"])

                def split_and_clear(x):
                    actual_item, is_clicked = x.split("-")
                    if is_clicked == "1":
                        return actual_item
                    else:
                        return np.nan

                history_data = data[[user_column_name, "history"]][data["history"].notna()]
                history_data["history"] = history_data["history"].apply(lambda x: x.split(" "))
                history_data = history_data.explode("history", ignore_index=True)
                history_data.rename(columns={"history": item_column_name}, inplace=True)

                if "test" not in file_name:
                    impression_data = data[[user_column_name, "impressions"]][data["impressions"].notna()]
                    impression_data["impressions"] = impression_data["impressions"].apply(lambda x: x.split(" "))
                    impression_data = impression_data.explode("impressions", ignore_index=True)
                    impression_data["impressions"] = impression_data["impressions"].apply(lambda x: split_and_clear(x))
                    impression_data = impression_data[impression_data["impressions"].notna()]
                    impression_data.rename(columns={"impressions": item_column_name}, inplace=True)
                    data = pd.concat([history_data, impression_data], axis=0, ignore_index=True)
                else:
                    data = history_data

                dfs.append(data)

        return pd.concat(dfs, axis=0)
