from pathlib import Path

from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("AlibabaIFashion")
class AlibabaIFashion(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://drive.usercontent.google.com/download?id=1G_1SV9H7fQMPPJOBmZpCnCkgifSsb9Ar&export=download&confirm=t&at=AKSUxGOyOatQ30CpcaRXJkpBTnB3%3A1760701852361",
            "e4f1d8203b9ea52fea86aa8ca850ff273a77f2255cf6c2050b8a38a271be8237",
            "user_data.txt.7z",
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        data = []
        raise NotImplementedError(
            "7 zip in python is a pain. We will implement this later"
        )

        # with py7zr.SevenZipFile(source_dir / "user_data.txt.7z", "r") as sevenzip_file:
        #     with TemporaryDirectory() as tmp_dir:
        #         print(tmp_dir)
        #         sevenzip_file.extractall(tmp_dir)
        # df = DataFrame(data, columns=["user", "item"])
        # df["rating"] = 1
        # return df
