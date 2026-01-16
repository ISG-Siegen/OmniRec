import zipfile
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader(["CiteULikeA", "CiteULikeT"])
class CiteULike(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        if name == "CiteULikeA":
            return DatasetInfo(
                "https://github.com/js05212/citeulike-a/archive/refs/heads/master.zip",
                "d47993abf270e0366536c94a9c31c512082b124ad6039b3779b519aa8ab4e96e",
            )
        elif name == "CiteULikeT":
            return DatasetInfo(
                "https://github.com/js05212/citeulike-t/archive/refs/heads/master.zip",
                "bc3bc287f13805e992b811db05c1f731f67167f6fdecab58f050433613727aab",
            )
        else:
            raise ValueError(f'Unknown dataset name "{name}" for CiteULike dataloader!')

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        if name == "CiteULikeA":
            repo_name = "citeulike-a"
        elif name == "CiteULikeT":
            repo_name = "citeulike-t"
        else:
            raise ValueError(f'Unknown dataset name "{name}" for CiteULike dataloader!')

        with zipfile.ZipFile(source_dir / "master.zip") as zipf:
            with zipf.open(f"{repo_name}-master/users.dat") as file:
                u_i_pairs = []
                for user, line in enumerate(file.readlines()):
                    line = line.decode("utf-8")
                    item_cnt = line.strip("\n").split(" ")[0]
                    items = line.strip("\n").split(" ")[1:]
                    assert len(items) == int(item_cnt)
                    for item in items:
                        assert item.isdecimal()
                        u_i_pairs.append((user, int(item)))
                df = pd.DataFrame(u_i_pairs, columns=["user", "item"])
                df["rating"] = 1
                return df
