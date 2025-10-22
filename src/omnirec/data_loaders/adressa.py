import json
import tarfile
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader("AdressaOneWeek")
class Adressa(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            "https://reclab.idi.ntnu.no/dataset/one_week.tar.gz",
            "a68a1af8322e7fabada7a8b8a118ba0564beab7eb0433e80b3dec13cf5158e03",
            verify_tls=False,
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        data = []
        with tarfile.open(source_dir / "one_week.tar.gz", "r:gz") as tar:
            for file in [
                "20170101",
                "20170102",
                "20170103",
                "20170104",
                "20170105",
                "20170106",
                "20170107",
            ]:
                day = tar.extractfile(f"one_week/{file}")
                if day is None:
                    continue
                file_data = []
                for line in day.readlines():
                    line_data = json.loads(line)
                    if "id" in line_data and "userId" in line_data:
                        file_data.append(
                            [line_data["userId"], line_data["id"], line_data["time"]]
                        )
                data.append(
                    DataFrame(
                        file_data,
                        columns=[
                            "user",
                            "item",
                            "timestamp",
                        ],
                    )
                )
            df = pd.concat(data)
            df["rating"] = 1
            return df
