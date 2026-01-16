import zipfile
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader(["DeliveryHeroSE", "DeliveryHeroSG", "DeliveryHeroTW"])
class DeliveryHero(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        if name == "DeliveryHeroSE":
            return DatasetInfo(
                "https://drive.usercontent.google.com/download?id=11OsafYu26ISaUfGEXzFSwNyKDJxKCy8e&export=download&confirm=t",
                "2a3947bd29a892a634882b0ec45e4d47a09e68dfdc74fca353b53467eeb43da4",
                "data_se.zip",
            )
        elif name == "DeliveryHeroSG":
            return DatasetInfo(
                "https://drive.usercontent.google.com/download?id=1v-FfCbLtv02EpNpopDx25EQnHZeT1nL2&export=download&confirm=t",
                "55a94a5c7eeba9610776b864aae7d653426afdb8aae93e5fa5050cbdc1c25d32",
                "data_sg.zip",
            )
        elif name == "DeliveryHeroTW":
            return DatasetInfo(
                "https://drive.usercontent.google.com/download?id=1Td7sTeJ7xcP8DLcY4bOQ_JqWUdqT93Ox&export=download&confirm=t",
                "83e8c0f5bfb4c27f14e3dd13964cc72117975397d7bee2522336301eaed781ec",
                "data_tw.zip",
            )
        else:
            raise ValueError(f'Unknown dataset name "{name}" for CiteULike dataloader!')

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        version = name[-2:].lower()

        with zipfile.ZipFile(source_dir / f"data_{version}.zip") as zipf:
            with zipf.open(f"data_{version}/orders_{version}.txt") as file:
                df = pd.read_csv(
                    file,
                    header=0,
                    sep=",",
                    usecols=["customer_id", "product_id", "order_time", "order_day"],
                )

                def convert_time_to_milliseconds(x):
                    if len(x.split(":")) == 3:
                        hours, minutes, seconds = x.split(":")
                        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
                    else:
                        return -1

                def convert_days_to_milliseconds(x):
                    if len(x.split(" ")) == 2:
                        days, _ = x.split(" ")
                        return int(days) * 24 * 3600
                    else:
                        return -1

                df["order_time"] = df["order_time"].apply(
                    lambda x: convert_time_to_milliseconds(x)
                )
                df["order_day"] = df["order_day"].apply(
                    lambda x: convert_days_to_milliseconds(x)
                )
                df["timestamp"] = df["order_time"] + df["order_day"]

                df.rename(
                    columns={
                        "customer_id": "user",
                        "product_id": "item",
                    },
                    inplace=True,
                )
                df["rating"] = 1

                return df[["user", "item", "rating", "timestamp"]]
