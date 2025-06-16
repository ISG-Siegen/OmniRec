import pandas as pd

from .loader import Loader


class Twitch(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        if additional_parameters["version"] == "100k_a":
            data = pd.read_csv(f"{source_path}/{additional_parameters['version']}.csv", sep=",", header=None,
                               usecols=[0, 1, 3, 4],
                               names=[user_column_name, item_column_name, "stream_start", "stream_stop"])
        elif additional_parameters["version"] == "full_a":
            data = pd.read_csv(f"{source_path}/{additional_parameters['version']}.csv.gz", compression="gzip", sep=",",
                               header=None, usecols=[0, 1, 3, 4],
                               names=[user_column_name, item_column_name, "stream_start", "stream_stop"])

        data[timestamp_column_name] = 0
        data[timestamp_column_name] = data.apply(lambda x: (x["stream_stop"] - x["stream_start"]) / 2, axis=1)
        data.drop(columns=["stream_start", "stream_stop"], inplace=True)
        return data
