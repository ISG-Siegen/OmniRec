import zipfile

import pandas as pd

from .loader import Loader


class Frappe(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/Mobile_Frappe.zip") as zipf:
            with zipf.open("Mobile_Frappe/frappe/frappe.csv") as file:
                data = pd.read_csv(file, sep="\t", header=0, usecols=["user", "item"])
                data.rename(columns={"user": user_column_name, "item": item_column_name}, inplace=True)
                return data
