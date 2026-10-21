import zipfile
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("Frappe")
class Frappe(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://www.baltrunas.info/_files/archives/be17b7_474755a5e9684a749a012516d04fb456.zip?dn=Mobile_Frappe.zip",
            "4adc616de57170f282397f6e6e30215f97fa7ad1b7f40bd12ef5dceaaf3e9b4e",
            "Mobile_Frappe.zip",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        with zipfile.ZipFile(source_dir / "Mobile_Frappe.zip") as zipf:
            with zipf.open("Mobile_Frappe/frappe/frappe.csv") as file:
                data = pd.read_csv(file, sep="\t", header=0, usecols=["user", "item"])
                return data
