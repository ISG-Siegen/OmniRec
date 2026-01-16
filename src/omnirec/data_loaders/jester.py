import zipfile
from pathlib import Path

import pandas as pd
from pandas.core.api import DataFrame as DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader

VERSIONS = {}


@_loader(
    [
        "Jester1_1",
        "Jester1_2",
        "Jester1_3",
        "Jester2",
        "Jester2Plus",
        "Jester3",
        "Jester4",
    ]
)
class Jester(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        if name == "Jester1_1":
            return DatasetInfo(
                "https://web.archive.org/web/20250409222630/https://eigentaste.berkeley.edu/dataset/archive/jester_dataset_1_1.zip",
                "cb7841756ded125b15f3d95c9f8241224065e96354c132a46ae4214deeab7615",
            )
        elif name == "Jester1_2":
            return DatasetInfo(
                "https://web.archive.org/web/20250409222630/https://eigentaste.berkeley.edu/dataset/archive/jester_dataset_1_2.zip",
                "4d312fd824d8c8cb2c9c952a7b1fb7c00d1f5fd3ece370f7285aa701d371748b",
            )
        elif name == "Jester1_3":
            return DatasetInfo(
                "https://web.archive.org/web/20250409222630/https://eigentaste.berkeley.edu/dataset/archive/jester_dataset_1_3.zip",
                "7f548d3762d3506cf7cd37d8cb9e3adb67984a7da7aa2d2096d5e0b1b884758d",
            )
        elif name == "Jester2":
            return DatasetInfo(
                "https://web.archive.org/web/20250409222630/https://eigentaste.berkeley.edu/dataset/archive/jester_dataset_2.zip",
                "5c2b9fb8346fc132ac1be6a9264fef9a6d153da68f3201839ac25c19f9a59a09",
            )
        elif name == "Jester2Plus":
            return DatasetInfo(
                "https://web.archive.org/web/20250409222630/https://eigentaste.berkeley.edu/dataset/archive/jester_dataset_3.zip",
                "de360773d91253200a203afa99c38d3368bfcfcc02d28088f11d5ec1dacc9f6f",
            )
        elif name == "Jester3":
            return DatasetInfo(
                "https://web.archive.org/web/20250514140837/https://eigentaste.berkeley.edu/dataset/JesterDataset3.zip",
                "0987d0d892f833ce9f889addb18c1960cb086658362a77a27216327ffb91614f",
            )
        elif name == "Jester4":
            return DatasetInfo(
                "https://web.archive.org/web/20250514140837/https://eigentaste.berkeley.edu/dataset/JesterDataset4.zip",
                "98382f7f652daf67d7c6963afd7e007cea180b20af290c115fcb587387ea831b",
            )
        else:
            raise ValueError(f'Unknown dataset name "{name}" for Jester dataloader!')

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        if name == "Jester1_1":
            with zipfile.ZipFile(source_dir / "jester_dataset_1_1.zip", "r") as zipf:
                data = pd.read_excel(zipf.open("jester-data-1.xls"), header=None)
        elif name == "Jester1_2":
            with zipfile.ZipFile(source_dir / "jester_dataset_1_2.zip", "r") as zipf:
                data = pd.read_excel(zipf.open("jester-data-2.xls"), header=None)
        elif name == "Jester1_3":
            with zipfile.ZipFile(source_dir / "jester_dataset_1_3.zip", "r") as zipf:
                data = pd.read_excel(zipf.open("jester-data-3.xls"), header=None)
        elif name == "Jester2":
            with zipfile.ZipFile(source_dir / "jester_dataset_2.zip", "r") as zipf:
                df = pd.read_csv(
                    zipf.open("jester_ratings.dat"),
                    sep="\t\t",
                    engine="python",
                    names=["user", "item", "rating"],
                )
                return df
        elif name == "Jester2Plus":
            with zipfile.ZipFile(source_dir / "jester_dataset_3.zip", "r") as zipf:
                data = pd.read_excel(zipf.open("jesterfinal151cols.xls"), header=None)
        elif name == "Jester3":
            with zipfile.ZipFile(source_dir / "JesterDataset3.zip", "r") as zipf:
                data = pd.read_excel(zipf.open("FINAL jester 2006-15.xls"), header=None)
        elif name == "Jester4":
            with zipfile.ZipFile(source_dir / "JesterDataset4.zip", "r") as zipf:
                data = pd.read_excel(
                    zipf.open(
                        "[final] April 2015 to Nov 30 2019 - Transformed Jester Data - .xlsx"
                    ),
                    header=None,
                )
        else:
            raise ValueError(f'Unknown dataset name "{name}" for Jester dataloader!')

        data = data.iloc[:, 1:]
        data["user"] = [i for i in range(len(data))]
        data = data.melt(
            id_vars="user",
            var_name="item",
            value_name="rating",
        )
        data = data[data["rating"] != 99]
        data.dropna(subset=["rating"], inplace=True)

        return data
