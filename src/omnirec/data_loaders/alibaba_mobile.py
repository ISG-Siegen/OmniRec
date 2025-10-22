import zipfile
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("AlibabaMobile")
class AlibabaMobile(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://tianchi.aliyun.com/dataset/46",
            "84156725849ff62e758323657adefa9d3f9c7fba7a6d847b04f77724be7c2992",
            download_file_name="tianchi_mobile_recommend_train_user.zip",
            license_or_registration=True,
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        with zipfile.ZipFile(
            source_dir / "tianchi_mobile_recommend_train_user.zip", "r"
        ) as zipf:
            data = pd.read_csv(
                zipf.open("tianchi_mobile_recommend_train_user.csv"),
                sep=",",
                header=0,
                usecols=["user_id", "item_id", "time"],
            )
            data.rename(
                columns={
                    "user_id": "user",
                    "item_id": "item",
                    "time": "timestamp",
                },
                inplace=True,
            )
            data["rating"] = 1
            return data
