from pathlib import Path

import pandas as pd
from pandas.core.api import DataFrame as DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader(
    [
        "Amazon2014Books",
        "Amazon2014Electronics",
        "Amazon2014MoviesAndTv",
        "Amazon2014CdsAndVinyl",
        "Amazon2014ClothingShoesAndJewelry",
        "Amazon2014HomeAndKitchen",
        "Amazon2014KindleStore",
        "Amazon2014SportsAndOutdoors",
        "Amazon2014CellPhonesAndAccessories",
        "Amazon2014HealthAndPersonalCare",
        "Amazon2014ToysAndGames",
        "Amazon2014VideoGames",
        "Amazon2014ToolsAndHomeImprovement",
        "Amazon2014Beauty",
        "Amazon2014AppsForAndroid",
        "Amazon2014OfficeProducts",
        "Amazon2014PetSupplies",
        "Amazon2014Automotive",
        "Amazon2014GroceryAndGourmetFood",
        "Amazon2014PatioLawnAndGarden",
        "Amazon2014Baby",
        "Amazon2014DigitalMusic",
        "Amazon2014MusicalInstruments",
        "Amazon2014AmazonInstantVideo",
    ]
)
class Amazon(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        if name == "Amazon2014Books":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Books.csv",
                "87d923ddac2aacf40c1d0e0e056dbf4bf69c9c7d41852c6b434e781e759c0707",
            )
        elif name == "Amazon2014Electronics":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Electronics.csv",
                "a8e5b66b7f5371d1659ff88ae4acec91604125d6850f4f7e1c418120f2f9c16c",
            )
        elif name == "Amazon2014MoviesAndTv":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Movies_and_TV.csv",
                "05fd3bbb387bca99f16b7a64a26abb736429da416e3cc0cc7423483e9ec4c265",
            )
        elif name == "Amazon2014CdsAndVinyl":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_CDs_and_Vinyl.csv",
                "74b503152bc8f92f389a1f841ec00361f903772e5ebb2b664ce678c023dbbceb",
            )
        elif name == "Amazon2014ClothingShoesAndJewelry":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Clothing_Shoes_and_Jewelry.csv",
                "7bf571cb99abaebf380d2a231986e6df7b622ebd49b308e2506f1c0aab54b29a",
            )
        elif name == "Amazon2014HomeAndKitchen":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Home_and_Kitchen.csv",
                "b0dae06e0b147abbf31878b4d16075a77b6ca8b8a5005b1a0b153b9d3ed310b2",
            )
        elif name == "Amazon2014KindleStore":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Kindle_Store.csv",
                "616edbb9ee9b5e1f0212e0a75e226df3abb66548d833df3ea8a3c53942541200",
            )
        elif name == "Amazon2014SportsAndOutdoors":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Sports_and_Outdoors.csv",
                "a31a27e2f0cd85b50acd002378cf1a23a0b3f2659484defb3225a836118252d4",
            )
        elif name == "Amazon2014CellPhonesAndAccessories":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Cell_Phones_and_Accessories.csv",
                "3c944712ec98360c959df256c9e3dde0d40caa4a888b6d2013050a7ab502afaa",
            )
        elif name == "Amazon2014HealthAndPersonalCare":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Health_and_Personal_Care.csv",
                "387374ea5c9641a6e9dc09b93423414da4f8153b2975594e8b24c4bdd60b0462",
            )
        elif name == "Amazon2014ToysAndGames":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Toys_and_Games.csv",
                "e28a342ca89a79036a9a840c0385a3a3342a08d3d3450ea3eaf3d544cd65d3af",
            )
        elif name == "Amazon2014VideoGames":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Video_Games.csv",
                "f0ca171050c2e0f208d47f5267992476b21ab68a01439c21c8be1a4432982cfa",
            )
        elif name == "Amazon2014ToolsAndHomeImprovement":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Tools_and_Home_Improvement.csv",
                "ea650a9d79e69a78f011843104ecac2a3ed8059bf7405e5a19f3a25511c9d2c6",
            )
        elif name == "Amazon2014Beauty":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Beauty.csv",
                "17d5232b90444beecfe758ce1446e5300230491f3a88ac802992ca95fc4c150f",
            )
        elif name == "Amazon2014AppsForAndroid":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Apps_for_Android.csv",
                "ed8919d499a20949a60ea10c40c25d820783da7bead896f32213f98b1887d987",
            )
        elif name == "Amazon2014OfficeProducts":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Office_Products.csv",
                "4cd5f3d454e744b7017ad5918e995ec2893b577c2109dbaa6d65b375092f9630",
            )
        elif name == "Amazon2014PetSupplies":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Pet_Supplies.csv",
                "5f963b813439471b4b2ce10fa7e9293da5995e4ec61f29d54489996a857b3442",
            )
        elif name == "Amazon2014Automotive":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Automotive.csv",
                "d77d59c094d86b7c987edcbc8d99ae78c9061e6f89ba819e1a77a1951fe977cc",
            )
        elif name == "Amazon2014GroceryAndGourmetFood":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Grocery_and_Gourmet_Food.csv",
                "ae9b32803a9f0ddf98222e00871e7a8ff7709e792f2ba8048131ca214617e33c",
            )
        elif name == "Amazon2014PatioLawnAndGarden":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Patio_Lawn_and_Garden.csv",
                "8edc47c5fe860e97e34ab1f339835606e551b03bec13bc4f967693c1b04ad3c0",
            )
        elif name == "Amazon2014Baby":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Baby.csv",
                "a219f779b2694f660f1ee243f2af71d63c2c9828425e716569faace305e978d1",
            )
        elif name == "Amazon2014DigitalMusic":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Digital_Music.csv",
                "fdf164882460ff26fa2521e01f6a9cf8005ad252ddce308dd03519064f02d80e",
            )
        elif name == "Amazon2014MusicalInstruments":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Musical_Instruments.csv",
                "c541cf84fcc75d98cc595ebd856b0ebd351efce134671171c2de0d54b9573b9c",
            )
        elif name == "Amazon2014AmazonInstantVideo":
            return DatasetInfo(
                "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Amazon_Instant_Video.csv",
                "249e1061d30db8c1230e4f3edd0523be12c37e6a8e6b9872a312cf6c326f157b",
            )
        else:
            raise ValueError(f'Unknown dataset name "{name}" for Amazon dataloader!')

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        rating_file = next(Path.iterdir(Path(source_dir)))
        return pd.read_csv(
            rating_file,
            header=None,
            sep=",",
            names=[
                "user",
                "item",
                "rating",
                "timestamp",
            ],
        )
