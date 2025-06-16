import zipfile
import pandas as pd

from .loader import Loader


class RARDII(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/dataverse_files.zip") as zipf:
            with zipf.open(f"rating_matrix_full-1.csv") as file:
                data = pd.read_csv(file, header=0, sep="\t", usecols=[1, 2, 4],
                                   names=[user_column_name, item_column_name, rating_column_name])
                data = data[data[rating_column_name] != 0]
                data.drop(columns=[rating_column_name], inplace=True)
                return data