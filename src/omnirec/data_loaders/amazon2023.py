from pathlib import Path

import pandas as pd
from pandas.core.api import DataFrame as DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader(
    [
        "Amazon2023AllBeauty",
        "Amazon2023AmazonFashion",
        "Amazon2023Appliances",
        "Amazon2023ArtsCraftsAndSewing",
        "Amazon2023Automotive",
        "Amazon2023BabyProducts",
        "Amazon2023BeautyAndPersonalCare",
        "Amazon2023Books",
        "Amazon2023CdsAndVinyl",
        "Amazon2023CellPhonesAndAccessories",
        "Amazon2023ClothingShoesAndJewelry",
        "Amazon2023DigitalMusic",
        "Amazon2023Electronics",
        "Amazon2023GiftCards",
        "Amazon2023GroceryAndGourmetFood",
        "Amazon2023HandmadeProducts",
        "Amazon2023HealthAndHousehold",
        "Amazon2023HealthAndPersonalCare",
        "Amazon2023HomeAndKitchen",
        "Amazon2023IndustrialAndScientific",
        "Amazon2023KindleStore",
        "Amazon2023MagazineSubscriptions",
        "Amazon2023MoviesAndTv",
        "Amazon2023MusicalInstruments",
        "Amazon2023OfficeProducts",
        "Amazon2023PatioLawnAndGarden",
        "Amazon2023PetSupplies",
        "Amazon2023Software",
        "Amazon2023SportsAndOutdoors",
        "Amazon2023SubscriptionBoxes",
        "Amazon2023ToolsAndHomeImprovement",
        "Amazon2023ToysAndGames",
        "Amazon2023VideoGames",
        "Amazon2023Unknown",
    ]
)
class Amazon2023(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        if name == "Amazon2023AllBeauty":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/All_Beauty.csv.gz",
                "54b894e68ad965aa73cdb80d8695c1ed37679c46f38b6f97b21ab0fb585aab24",
            )
        elif name == "Amazon2023AmazonFashion":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Amazon_Fashion.csv.gz",
                "7d08f3ad3ec331eb95cabf5a85c8e65f82f958429a17131e6d391f54532c0310",
            )
        elif name == "Amazon2023Appliances":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Appliances.csv.gz",
                "0096701a2521a5fc71c5cfca11e953b0eb48a94a1b6ee4be65cb680c1fd56976",
            )
        elif name == "Amazon2023ArtsCraftsAndSewing":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Arts_Crafts_and_Sewing.csv.gz",
                "05ca786b3f99269ba659d71891b55d23e37bd74ab6cec0b53214ccb656308bb3",
            )
        elif name == "Amazon2023Automotive":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Automotive.csv.gz",
                "9dda260d1d2cb91d0f967d0b4bfa0a09fda2904432023234569e45a6a30c48d3",
            )
        elif name == "Amazon2023BabyProducts":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Baby_Products.csv.gz",
                "e2a8d0498afed767ee2615db7fac549559d82490b1a73c7241b84b5e9e8c279e",
            )
        elif name == "Amazon2023BeautyAndPersonalCare":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Beauty_and_Personal_Care.csv.gz",
                "dd89a914e8c71d811c49a7e8fbdfc251c08bffb461b9544275e94018cb17f741",
            )
        elif name == "Amazon2023Books":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Books.csv.gz",
                "752e144c1d3804619711a6b21bd68a5505825064723bfcd5008ac26067abe04b",
            )
        elif name == "Amazon2023CdsAndVinyl":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/CDs_and_Vinyl.csv.gz",
                "1bade4e428efcffb549b6b7cb1f62a8cde9644e19a981a210b11a4c9c1561e75",
            )
        elif name == "Amazon2023CellPhonesAndAccessories":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Cell_Phones_and_Accessories.csv.gz",
                "1f6df616b0ae463c039f68c7082daec52d2c713b33adb57b85db3430a8e2373a",
            )
        elif name == "Amazon2023ClothingShoesAndJewelry":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Clothing_Shoes_and_Jewelry.csv.gz",
                "ee93396e811c03d077290b78e323228c58814a034e3e98d0339e5314d7f7a9a7",
            )
        elif name == "Amazon2023DigitalMusic":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Digital_Music.csv.gz",
                "dbd5ddd5398d0eb9cfe224c9cc60470ccfd9c55e76fc82653dd3f44f6796c2a1",
            )
        elif name == "Amazon2023Electronics":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Electronics.csv.gz",
                "2ac3508c5d0ee55ed9fdc833629f751e0f0120b9a8cb30867c8c14b87911c170",
            )
        elif name == "Amazon2023GiftCards":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Gift_Cards.csv.gz",
                "abfd9636afc5cdc1f46082ac1f9661b7c617cbd9c8a75652ad6a567173a14807",
            )
        elif name == "Amazon2023GroceryAndGourmetFood":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Grocery_and_Gourmet_Food.csv.gz",
                "4cb2da7f57dfe210eecf348ee16514d11460022f0ce4ed141aa66e3eb5410135",
            )
        elif name == "Amazon2023HandmadeProducts":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Handmade_Products.csv.gz",
                "b024e3e4cb1b1f4c9cfbb44a506ea42f8b8430ee8caf0dfa69fef52b69ece408",
            )
        elif name == "Amazon2023HealthAndHousehold":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Health_and_Household.csv.gz",
                "0a8982f9915bd18ea61caf4341db95c3fe1478abee907e6a61fec838374d2dca",
            )
        elif name == "Amazon2023HealthAndPersonalCare":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Health_and_Personal_Care.csv.gz",
                "5516d99b9747abff99003a7e1518833c2d64b10196201b6e6e90673bee15964d",
            )
        elif name == "Amazon2023HomeAndKitchen":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Home_and_Kitchen.csv.gz",
                "9be4e2dc8b3dc513c02521644b2ae55f722b2941767e539dcfe518f6bdd4f70b",
            )
        elif name == "Amazon2023IndustrialAndScientific":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Industrial_and_Scientific.csv.gz",
                "97aea590deb258f634caea04b63f038dceb5990bbc92cac87ce2a985f0f91595",
            )
        elif name == "Amazon2023KindleStore":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Kindle_Store.csv.gz",
                "ff546c451edfb403d10099912b816b11600e689a599621167d4847331fdc0a0d",
            )
        elif name == "Amazon2023MagazineSubscriptions":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Magazine_Subscriptions.csv.gz",
                "4892619d97f810331c2a278176b2be616de10403be59e48efbe65c5c1e7904d2",
            )
        elif name == "Amazon2023MoviesAndTv":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Movies_and_TV.csv.gz",
                "aa927ae5a4fc5262bfa6152ce522349f828760035242fd7e02b1dc139e867156",
            )
        elif name == "Amazon2023MusicalInstruments":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Musical_Instruments.csv.gz",
                "042648a89f479aaa2af4664dcb49966dbaf07bd5ebab6957799f5fb4c5efa2e0",
            )
        elif name == "Amazon2023OfficeProducts":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Office_Products.csv.gz",
                "f91b5cfb6ed5ff52afe3e2f3ecc7918cbd8745b3241a8fc61011c3a41f23920b",
            )
        elif name == "Amazon2023PatioLawnAndGarden":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Patio_Lawn_and_Garden.csv.gz",
                "a1ea496e71e488c6b12823d479ed6375384b82f6794b38e66d12a5dcd20c392d",
            )
        elif name == "Amazon2023PetSupplies":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Pet_Supplies.csv.gz",
                "cfc55406a1fbb507e4adfa18472e60a5de52fab3dd76f97fea25d30da1288003",
            )
        elif name == "Amazon2023Software":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Software.csv.gz",
                "11687bdbedc0bfd9bf86368465dcab40f2450d1ea8eabd3c830ba8b339edd9c0",
            )
        elif name == "Amazon2023SportsAndOutdoors":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Sports_and_Outdoors.csv.gz",
                "110617511c7303ca34d157b7d62fd20a02e412c3639b4c6e307a951fadf0414c",
            )
        elif name == "Amazon2023SubscriptionBoxes":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Subscription_Boxes.csv.gz",
                "fb867ee253db3987ab3ceaf371da506df794b08c98cf9a99e9718d9e4e818188",
            )
        elif name == "Amazon2023ToolsAndHomeImprovement":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Tools_and_Home_Improvement.csv.gz",
                "5845ac062a2c165d540badac13f00a8cb8cdaa30deb670a9b41db19d92c6bd1d",
            )
        elif name == "Amazon2023ToysAndGames":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Toys_and_Games.csv.gz",
                "170fc8a18797c6091cf1b07bb3d97c13c94bfa030cf76c430bb8cac0dfb47a9f",
            )
        elif name == "Amazon2023VideoGames":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Video_Games.csv.gz",
                "30692f9806e33a7b5d8b599b73d7ca33dbfefb0abdfc1578052a101f2e64b3cd",
            )
        elif name == "Amazon2023Unknown":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Unknown.csv.gz",
                "864c1dfa8b215a9a09fe0d17c7abc15f2da97078bc9acc7911783f2447016e10",
            )
        else:
            raise ValueError(
                f'Unknown dataset name "{name}" for Amazon2023 dataloader!'
            )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        gz_file = next(Path.iterdir(Path(source_dir)))
        df = pd.read_csv(
            gz_file,
            sep=",",
        )
        df.rename(columns={"user_id": "user", "parent_asin": "item"}, inplace=True)
        return df
