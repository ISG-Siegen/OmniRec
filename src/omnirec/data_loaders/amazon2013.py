import gzip
from pathlib import Path

import pandas as pd
from pandas.core.api import DataFrame as DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader

REQUIRED_FIELDS = {"productId", "userId", "score", "time"}


@_loader(
    [
        "Amazon2013AmazonInstantVideo",
        "Amazon2013Arts",
        "Amazon2013Automotive",
        "Amazon2013Baby",
        "Amazon2013Beauty",
        "Amazon2013Books",
        "Amazon2013CellPhonesAndAccessories",
        "Amazon2013ClothingAndAccessories",
        "Amazon2013Electronics",
        "Amazon2013GourmetFoods",
        "Amazon2013Health",
        "Amazon2013HomeAndKitchen",
        "Amazon2013IndustrialAndScientific",
        "Amazon2013Jewelry",
        "Amazon2013KindleStore",
        "Amazon2013MoviesAndTV",
        "Amazon2013MusicalInstruments",
        "Amazon2013Music",
        "Amazon2013OfficeProducts",
        "Amazon2013Patio",
        "Amazon2013PetSupplies",
        "Amazon2013Shoes",
        "Amazon2013Software",
        "Amazon2013SportsAndOutdoors",
        "Amazon2013ToolsAndHomeImprovement",
        "Amazon2013ToysAndGames",
        "Amazon2013VideoGames",
        "Amazon2013Watches",
    ]
)
class Amazon2013(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        if name == "Amazon2013AmazonInstantVideo":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Amazon_Instant_Video.txt.gz",
                "6f866b68147cf191a46ae8caf27fb317027da7621a80d09a90465264b82a10dd",
            )
        elif name == "Amazon2013Arts":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Arts.txt.gz",
                "772ce4e39b6127b7753794e44415148f02b5834c831c1ce5b8a5804228c38b52",
            )
        elif name == "Amazon2013Automotive":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Automotive.txt.gz",
                "3b46a17dfff27a566bdf59a33e68decf811b537151cb51393246a4fadfb1204f",
            )
        elif name == "Amazon2013Baby":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Baby.txt.gz",
                "902b4ec82cdc4d30198e5d94469f9fe588a14d96e05fe2633d72cb0674b5339f",
            )
        elif name == "Amazon2013Beauty":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Beauty.txt.gz",
                "8bc0101695d4a995c50f72b3712e07246f6a506ca958cc2647229a347220c33a",
            )
        elif name == "Amazon2013Books":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Books.txt.gz",
                "2b89e46f650ad88396300b9e697311ee2b7ddf26216f9ebcf0538bd3c5a5adff",
            )
        elif name == "Amazon2013CellPhonesAndAccessories":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Cell_Phones_&_Accessories.txt.gz",
                "caa4efbd589fb0896cc065ab9363b349735699f69625d1dafd62006741953120",
            )
        elif name == "Amazon2013ClothingAndAccessories":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Clothing_&_Accessories.txt.gz",
                "b511639f6bf950caf01b956f8faf6bfd52fa6640c719b5c446526d25780d1216",
            )
        elif name == "Amazon2013Electronics":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Electronics.txt.gz",
                "9029cee5e6f7209ceee7e4d52910397023c59d599430eb84b05fa1a6b822e3f4",
            )
        elif name == "Amazon2013GourmetFoods":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Gourmet_Foods.txt.gz",
                "2d4ef8fe1a934c5a9fc93e2fe19f3c2f69edef7b9c0a5c1b063bf1b694368fe1",
            )
        elif name == "Amazon2013Health":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Health.txt.gz",
                "07f7c6bfd092ab255ee9f4f07243f37538cc6d3cc84c3e1ad929e4cf3e639910",
            )
        elif name == "Amazon2013HomeAndKitchen":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Home_&_Kitchen.txt.gz",
                "4ef2026ed5422b3a80ec1c9ab49c905f7de34be704b30a08edaa3e6883840987",
            )
        elif name == "Amazon2013IndustrialAndScientific":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Industrial_&_Scientific.txt.gz",
                "828fd717f6e36a2da755fc3e18b447edce70d45997f1b2d34ffbcda91f94fd9e",
            )
        elif name == "Amazon2013Jewelry":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Jewelry.txt.gz",
                "e4cfb936df65b16156f3e6a3fe7cef57d474aa992cfed87905d73ad889656070",
            )
        elif name == "Amazon2013KindleStore":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Kindle_Store.txt.gz",
                "b5e3224e83cb99927b8d0edb7b16e67d7f8e5936f06feeb876ee514b6b0c0f7d",
            )
        elif name == "Amazon2013MoviesAndTV":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Movies_&_TV.txt.gz",
                "f93e43d1fafda9d64c424ac5cf6957e96a447dbee263afebe5ec5d144e41e350",
            )
        elif name == "Amazon2013MusicalInstruments":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Musical_Instruments.txt.gz",
                "f20578a5edb810d7d96020db35372f4e73a4fe4b2ded811addca673bbfd8569c",
            )
        elif name == "Amazon2013Music":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Music.txt.gz",
                "55470b89ba94e28fe557571e3a17c31c017628465057987c1f433ae5fb2f0815",
            )
        elif name == "Amazon2013OfficeProducts":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Office_Products.txt.gz",
                "f22630453b18bbc771c88e4738e827419ba9c320c7583363977bad8f954cc2e2",
            )
        elif name == "Amazon2013Patio":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Patio.txt.gz",
                "e60ac93d94258918401286e39e614c1c502c061e42dcee7f906bc174673aa9b9",
            )
        elif name == "Amazon2013PetSupplies":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Pet_Supplies.txt.gz",
                "3262ac63fa8e099469e3d9ad572bdb11b8fd4f33cb611f6463157a760679f78d",
            )
        elif name == "Amazon2013Shoes":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Shoes.txt.gz",
                "63a20ac3e452f31b7e35ba54bfe5e5bdb9ab7aeb18018edda25b9473db4ed545",
            )
        elif name == "Amazon2013Software":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Software.txt.gz",
                "53348ef0fdc787a8aa0996115bcc259ebee1905a6911cd434ff402ae667baedd",
            )
        elif name == "Amazon2013SportsAndOutdoors":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Sports_&_Outdoors.txt.gz",
                "4f545797da3af6f019f9c5fb1285b349f5c5861fbc3140bc1520fa8900068f5e",
            )
        elif name == "Amazon2013ToolsAndHomeImprovement":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Tools_&_Home_Improvement.txt.gz",
                "d949b3d21be87094469bc1cb30678e100569341d612d07e2ce3b8ee8990d7fb7",
            )
        elif name == "Amazon2013ToysAndGames":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Toys_&_Games.txt.gz",
                "7ae7bead718c16685a1ea763adbcf78f2cc6ba404b35ca3aed55dc3bf19167a8",
            )
        elif name == "Amazon2013VideoGames":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Video_Games.txt.gz",
                "90d4624dfd0cef4715322d82ae8d0d6bc30622433b0cd235ac38fd405a757697",
            )
        elif name == "Amazon2013Watches":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/Watches.txt.gz",
                "515108f52734df3ce8e9d40d771d4200394f8d72ead034fe1a9a8f08456ff5d5",
            )
        else:
            raise ValueError(
                f'Unknown dataset name "{name}" for Amazon2013 dataloader!'
            )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        rating_file = next(Path.iterdir(Path(source_dir)))
        df = pd.DataFrame(Amazon2013._parse_reviews(rating_file))
        return df

    @staticmethod
    def _parse_reviews(path: Path):
        with gzip.open(path, "rt", encoding="utf-8") as f:
            current = {}
            for line in f:
                line = line.strip()

                if line.startswith("product/productId:"):
                    current["productId"] = line.split(": ", 1)[1]
                elif line.startswith("review/userId:"):
                    current["userId"] = line.split(": ", 1)[1]
                elif line.startswith("review/score:"):
                    current["score"] = float(line.split(": ", 1)[1])
                elif line.startswith("review/time:"):
                    current["time"] = int(line.split(": ", 1)[1])
                elif line == "":
                    if REQUIRED_FIELDS.issubset(current):
                        yield {
                            "item": current.get("productId"),
                            "user": current.get("userId"),
                            "rating": current.get("score"),
                            "timestamp": current.get("time"),
                        }
                    current = {}

            if current:
                yield current
