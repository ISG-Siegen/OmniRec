import zipfile
import pandas as pd

from .loader import Loader


class Jester(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        if additional_parameters['version'] == "1":
            with zipfile.ZipFile(f"{source_path}/jester_dataset_1_1.zip", "r") as zipf:
                data_j1 = pd.read_excel(zipf.open("jester-data-1.xls"), header=None)
            with zipfile.ZipFile(f"{source_path}/jester_dataset_1_2.zip", "r") as zipf:
                data_j2 = pd.read_excel(zipf.open("jester-data-2.xls"), header=None)
            with zipfile.ZipFile(f"{source_path}/jester_dataset_1_3.zip", "r") as zipf:
                data_j3 = pd.read_excel(zipf.open("jester-data-3.xls"), header=None)

            data = pd.concat([data_j1, data_j2, data_j3], axis=0)
        elif additional_parameters['version'] == "2Plus":
            with zipfile.ZipFile(f"{source_path}/jester_dataset_3.zip", "r") as zipf:
                data = pd.read_excel(zipf.open("jesterfinal151cols.xls"), header=None)
        elif additional_parameters['version'] == "3":
            with zipfile.ZipFile(f"{source_path}/JesterDataset3.zip", "r") as zipf:
                data = pd.read_excel(zipf.open("FINAL jester 2006-15.xls"), header=None)
        elif additional_parameters['version'] == "4":
            with zipfile.ZipFile(f"{source_path}/JesterDataset4.zip", "r") as zipf:
                data = pd.read_excel(zipf.open("[final] April 2015 to Nov 30 2019 - Transformed Jester Data - .xlsx"),
                                     header=None)
        data = data.iloc[:, 1:]
        data[user_column_name] = [i for i in range(len(data))]
        data = data.melt(id_vars=user_column_name, var_name=item_column_name, value_name=rating_column_name)
        data = data[data[rating_column_name] != 99]
        data.dropna(subset=[rating_column_name], inplace=True)

        return data
