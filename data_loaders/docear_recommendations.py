import zipfile
import pandas as pd

from .loader import Loader


class DocearRecommendations(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/docear-datasets-recommendations.zip") as zipf:
            with zipf.open(f"recommendations/recommendations/recommendations.csv") as file:
                data = pd.read_csv(file, header=0, sep="\t", usecols=[3, 4, 30],
                                        names=[timestamp_column_name, item_column_name, user_column_name])[
                                [user_column_name, item_column_name, timestamp_column_name]]
                data = data[data[timestamp_column_name].notna()]
                return data
