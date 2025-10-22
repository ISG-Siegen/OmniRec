import ast
import gzip
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader(["BeerAdvocate", "RateBeer"])
class Beer(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        if name == "BeerAdvocate":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/beer/beeradvocate.json.gz",
                "1e62c122f3645e46bffa6fd00d5d8b46ee4f61dc01fc8a60b0c35be16c2315a8",
            )
        elif name == "RateBeer":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/beer/ratebeer.json.gz",
                "f3b2569d23a831017f2d199ace85bb49d8c088e2ebff55d91f49a2a4d44efd74",
            )
        else:
            raise ValueError(f'Unknown dataset name "{name}" for Beer dataloader!')

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        with gzip.open(source_dir / f"{name.lower()}.json.gz", "r") as gz:
            file = gz.readlines()
            final_dict = {
                "user": [],
                "item": [],
                "rating": [],
                "timestamp": [],
            }
            for line in file:
                dic = ast.literal_eval(line.decode())
                if all(
                    k in dic
                    for k in (
                        "review/profileName",
                        "beer/beerId",
                        "review/overall",
                        "review/time",
                    )
                ):
                    final_dict["user"].append(dic["review/profileName"])
                    final_dict["item"].append(dic["beer/beerId"])
                    final_dict["rating"].append(dic["review/overall"])
                    final_dict["timestamp"].append(dic["review/time"])
            data = pd.DataFrame.from_dict(final_dict)

            if name == "RateBeer":
                data["rating"] = data["rating"].apply(lambda x: x.split("/")[0])

            return data
