import json
import tarfile
import zipfile
from pathlib import Path

import pandas as pd
from pandas.core.api import DataFrame as DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


def file_missing_err(name: str):
    return ValueError(f'Cannot find file "{name}" in archive!')


pre_23_name_to_link_and_checksum = {
    "Yelp2018": (
        "https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset/versions/1",
        "7c5157bb92c92b03a2323df6cda7c4d80b8b6bbcd1a455cc8562ee746e1db4a7",
    ),
    "Yelp2019": (
        "https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset/versions/9",
        "ed66da89ebf6141f678632cadb694308581b7d32cd8b9e9dda03520dc25d80a7",
    ),
    "Yelp2020": (
        "https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset/versions/2",
        "ad0e83d9f273b1dcbff254eb38d66fc5794f4c9e4900a031beeb64227428cf7f",
    ),
    "Yelp2021": (
        "https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset/versions/3",
        "a92fa71dd985d278a3c88c7ffe2a4d3be964a9eec3ba53b1720d17a569804af4",
    ),
    "Yelp2022": (
        "https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset/",
        "a07689ac11ea09b8cb04993ce4593f7157696088e707d8352c754dde279bfd5a",
    ),
}


def name_err(name: str):
    return ValueError(f'Unknown dataset name "{name}" for Yelp dataloader!')


@_loader(
    [
        "Yelp2018",
        "Yelp2019",
        "Yelp2020",
        "Yelp2021",
        "Yelp2022",
        "Yelp2023",
    ]
)
class Yelp(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        if name == "Yelp2023":
            return DatasetInfo(
                "https://business.yelp.com/external-assets/files/Yelp-JSON.zip",
                "7196433b8a43dd1cbbc3054c5ee85447a56d5fdee8652f8dc7aa5aad579ad7cd",
            )
        elif name in ("Yelp2018", "Yelp2019", "Yelp2020", "Yelp2021", "Yelp2022"):
            link_checksum = pre_23_name_to_link_and_checksum.get(name)
            if link_checksum is None:
                raise name_err(name)

            return DatasetInfo(
                link_checksum[0],
                link_checksum[1],
                download_file_name="archive.zip",
                license_or_registration=True,
            )

        else:
            raise name_err(name)

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        if name == "Yelp2018":
            with zipfile.ZipFile(source_dir / "archive.zip", "r") as zipf:
                with tarfile.open(fileobj=zipf.open("dataset.tgz"), mode="r:gz") as tar:
                    file_name = "yelp_academic_dataset_review.json"
                    file = tar.extractfile(file_name)
                    if file is None:
                        raise file_missing_err(file_name)
                    lines = file.readlines()
        elif name in ("Yelp2019", "Yelp2020", "Yelp2021", "Yelp2022"):
            with zipfile.ZipFile(source_dir / "archive.zip", "r") as zipf:
                file = zipf.open("yelp_academic_dataset_review.json")
                lines = file.readlines()
        elif name == "Yelp2023":
            with tarfile.open(source_dir / "yelp_dataset.tar", mode="r") as tar:
                file_name = "yelp_academic_dataset_review.json"
                file = tar.extractfile(file_name)
                if file is None:
                    raise file_missing_err(file_name)
                lines = file.readlines()
        else:
            raise name_err(name)

        final_dict = {
            "user": [],
            "item": [],
            "rating": [],
            "timestamp": [],
        }
        for line in lines:
            line = line.decode("utf-8")
            dic = json.loads(line)
            if all(k in dic for k in ("user_id", "business_id", "stars", "date")):
                final_dict["user"].append(dic["user_id"])
                final_dict["item"].append(dic["business_id"])
                final_dict["rating"].append(dic["stars"])
                final_dict["timestamp"].append(dic["date"])
        return pd.DataFrame.from_dict(final_dict)
