import tarfile
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader

VERSION_INFO = {
    "AmazonMP3": ("wang-amazon", True),
    "AmazonRatings": ("amazon-ratings", True),
    "Libimseti": ("libimseti", False),
    "StackOverflow": ("stackexchange-stackoverflow", True),
    "TripAdvisor": ("wang-tripadvisor", True),
    "WikiLens": ("wikilens-ratings", True),
    "YahooSongs": ("yahoo-song", True),
}


@_loader(list(VERSION_INFO.keys()))
class Konect(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        if name == "AmazonMP3":
            return DatasetInfo(
                "http://konect.cc/files/download.tsv.wang-amazon.tar.bz2",
                "4299c063fbbc9ad3327e403dc032ad7bcb87293c854894f7fa77ce85336f4e03",
            )
        elif name == "AmazonRatings":
            return DatasetInfo(
                "http://konect.cc/files/download.tsv.amazon-ratings.tar.bz2",
                "e0c739d04c554aa06f132f19575fc8c1e75894afd12662f34e0b10543c25849e",
            )
        elif name == "Libimseti":
            return DatasetInfo(
                "http://konect.cc/files/download.tsv.libimseti.tar.bz2",
                "2236164dc1c72d81e952d6435a550aaaaebada65c8679e6a0be6d456ebcc4bf5",
            )
        elif name == "StackOverflow":
            return DatasetInfo(
                "http://konect.cc/files/download.tsv.stackexchange-stackoverflow.tar.bz2",
                "5dbb6e97d17d8ab534e1e7464e319e7801075e1c0164d96334013074833f4c01",
            )
        elif name == "TripAdvisor":
            return DatasetInfo(
                "http://konect.cc/files/download.tsv.wang-tripadvisor.tar.bz2",
                "a762c7ee7e6bacf409daa57ee5f696d7bde88c4eaa05bfbd3c1722a576b616b9",
            )
        elif name == "WikiLens":
            return DatasetInfo(
                "http://konect.cc/files/download.tsv.wikilens-ratings.tar.bz2",
                "bbfdafa86435d8ff58cc0ddd5adbc3c75a1a6bc86b97e169e020948fe1e5fe52",
            )
        elif name == "YahooSongs":
            return DatasetInfo(
                "http://konect.cc/files/download.tsv.yahoo-song.tar.bz2",
                "772e0852f1312fff86b89979a0d1165aab66ae985274524d74e4ddc3d1a4993a",
            )
        else:
            raise ValueError(f"Invalid dataset name for Konect loader: {name}")

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        info = VERSION_INFO.get(name)
        assert info is not None
        version = info[0]
        has_timestamp = info[1]

        with tarfile.open(
            source_dir / f"download.tsv.{version}.tar.bz2",
            "r:bz2",
        ) as tar:
            names = ["user", "item", "rating"]
            if has_timestamp:
                names.append("timestamp")
            member = f"{version}/out.{version}"
            io_bytes = tar.extractfile(member)
            assert io_bytes is not None
            data = pd.read_csv(
                io_bytes,
                header=0,
                sep="\\s+",
                names=names,
                low_memory=False,
            )
            if data.iloc[0, :]["user"] == "%":
                data = data.iloc[1:, :]
            if data["rating"].unique().size == 1:
                data.drop(columns=["rating"], inplace=True)
            return data
