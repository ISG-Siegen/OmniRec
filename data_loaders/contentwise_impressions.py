import zipfile
import pandas as pd

from .loader import Loader


class ContentWiseImpressions(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/ContentWiseImpressionsData.zip") as zipf:
            compressed_file = zipf.open(
                "ContentWiseImpressions/data/ContentWiseImpressions/CW10M-CSV/interactions.csv.gz")
            return pd.read_csv(compressed_file, compression="gzip", header=0, sep=",",
                               names=[timestamp_column_name, user_column_name,
                                      item_column_name, "1", "2", "3", "4", "5", "6", "7", "8"],
                               usecols=[user_column_name, item_column_name,
                                        timestamp_column_name])[[user_column_name, item_column_name,
                                                                 timestamp_column_name]]
