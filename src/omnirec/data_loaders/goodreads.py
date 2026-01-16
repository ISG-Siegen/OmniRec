import gzip
import json
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader

INFO_MAP = {
    "GoodreadsChildren": (
        "children",
        "d8ce59259e45262b3322bd87f5c2a13228cd8bb659332414a05660aed7cd7c71",
    ),
    "GoodreadsComicsAndGraphic": (
        "comics_graphic",
        "b55fbe66c2c802cefad5051808724d5074e342d6a4004309595a972702a62f4d",
    ),
    "GoodreadsFantasyAndParanormal": (
        "fantasy_paranormal",
        "ec6a2444c13aa05b056988ac2671c5d643883c9aca0d8f9e46e413fc5773fa4b",
    ),
    "GoodreadsHistoryAndBiography": (
        "history_biography",
        "c08c7ebe477807556d4f92b75ba146916f2ae49e3ed269e3966fd9ca4ce517ca",
    ),
    "GoodreadsMysteryThrillerAndCrime": (
        "mystery_thriller_crime",
        "9c3c179ce5e5612cf72dc7aa2e570b49ab655b42a44cb8e9ddd5697393c43c4f",
    ),
    "GoodreadsPoetry": (
        "poetry",
        "65fb9777f5e482695f0e4b71ef9884f6a7e5ab31c224dabc7ae0c2dcd60e49de",
    ),
    "GoodreadsRomance": (
        "romance",
        "3dde6e1dae8ebb7384f849e4378f5f294cbd6385abeac238aea2ce7e66e0faf0",
    ),
    "GoodreadsYoungAdult": (
        "young_adult",
        "6d03182383f10e1eec36ac0a972533806518e2a082089867e3deb941ed77d6c4",
    ),
}


def get_info(name: str):
    info = INFO_MAP.get(name)
    if info is None:
        raise ValueError(f'Unknown dataset name "{name}" for Goodreads dataloader!')

    return info


@_loader(list(INFO_MAP.keys()))
class Goodreads(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        version, checksum = get_info(name)

        return DatasetInfo(
            f"https://mcauleylab.ucsd.edu/public_datasets/gdrive/goodreads/byGenre/goodreads_interactions_{version}.json.gz",
            checksum,
        )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        version, checksum = get_info(name)

        with gzip.open(
            source_dir / f"goodreads_interactions_{version}.json.gz",
            "rb",
        ) as file:
            file_data = []
            for line in file.readlines():
                line = json.loads(line.decode("utf-8"))
                if (
                    "user_id" in line
                    and "book_id" in line
                    and "rating"
                    and "date_updated" in line
                ):
                    file_data.append(
                        [
                            line["user_id"],
                            line["book_id"],
                            line["rating"],
                            line["date_updated"],
                        ]
                    )
            return pd.DataFrame(
                file_data,
                columns=[
                    "user",
                    "item",
                    "rating",
                    "timestamp",
                ],
            )
