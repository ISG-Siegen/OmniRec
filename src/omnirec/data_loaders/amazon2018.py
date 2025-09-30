from pathlib import Path

import pandas as pd
from pandas.core.api import DataFrame as DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader(
    [
        "Amazon2018AmazonFashion",
        "Amazon2018AllBeauty",
        "Amazon2018Appliances",
        "Amazon2018ArtsCraftsAndSewing",
        "Amazon2018Automotive",
        "Amazon2018Books",
        "Amazon2018CdsAndVinyl",
        "Amazon2018CellPhonesAndAccessories",
        "Amazon2018ClothingShoesAndJewelry",
        "Amazon2018DigitalMusic",
        "Amazon2018Electronics",
        "Amazon2018GiftCards",
        "Amazon2018GroceryAndGourmetFood",
        "Amazon2018HomeAndKitchen",
        "Amazon2018IndustrialAndScientific",
        "Amazon2018KindleStore",
        "Amazon2018LuxuryBeauty",
        "Amazon2018MagazineSubscriptions",
        "Amazon2018MoviesAndTv",
        "Amazon2018MusicalInstruments",
        "Amazon2018OfficeProducts",
        "Amazon2018PatioLawnAndGarden",
        "Amazon2018PetSupplies",
        "Amazon2018PrimePantry",
        "Amazon2018Software",
        "Amazon2018SportsAndOutdoors",
        "Amazon2018ToolsAndHomeImprovement",
        "Amazon2018ToysAndGames",
        "Amazon2018VideoGames",
    ]
)
class Amazon2018(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        if name == "Amazon2018AmazonFashion":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/AMAZON_FASHION.csv",
                "c72e84207601cd00840a91b9b4433c60b8be800a27aa86991f5cb57f29b99825",
            )
        elif name == "Amazon2018AllBeauty":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/All_Beauty.csv",
                "b3d9260771f9fe489a61180b9ff407e15e10f481a287848f69bc4709b669246f",
            )
        elif name == "Amazon2018Appliances":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Appliances.csv",
                "35af90b093508f4a811d259b71b94d45b2f67b0daf3d702203d29ff6b16b1e28",
            )
        elif name == "Amazon2018ArtsCraftsAndSewing":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Arts_Crafts_and_Sewing.csv",
                "ab42ec44840c130b8bcb1993bad37021b5ff98f3aae55a120c2a0d0624be3be5",
            )
        elif name == "Amazon2018Automotive":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Automotive.csv",
                "3cb4182e6623f1ac4511cf02a46c5ba11b761fa6d7feead7922199603f9d35df",
            )
        elif name == "Amazon2018Books":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Books.csv",
                "2ff13d9763d38118851d8f8a4ab530f958e08ad48aa764c2d9bbe16ec227a3b8",
            )
        elif name == "Amazon2018CdsAndVinyl":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/CDs_and_Vinyl.csv",
                "daedcfb79310479728f11cc1e66d49ec6dccdec124222391bf6f4f69ca5092db",
            )
        elif name == "Amazon2018CellPhonesAndAccessories":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Cell_Phones_and_Accessories.csv",
                "c05835e7a7f7a1b0bab4fe4f2dbabecb102fde22de579758d10d36973d8b6a14",
            )
        elif name == "Amazon2018ClothingShoesAndJewelry":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Clothing_Shoes_and_Jewelry.csv",
                "8b78d8a965e2351468deeebe99edb6118561711be4d5b6294e24e25f910c4d3d",
            )
        elif name == "Amazon2018DigitalMusic":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Digital_Music.csv",
                "a73f1504ed58fdc3533a6817b4c89fc4f722eb46dc18f94a4566a4b171439c9c",
            )
        elif name == "Amazon2018Electronics":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Electronics.csv",
                "1ce756643c0abed1b0d8a0738e67fc2510f3086d2bd52567942e18582dd01791",
            )
        elif name == "Amazon2018GiftCards":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Gift_Cards.csv",
                "e360486b46b7eef5f2ed3ecc0a486f15097b7600fbee4079632418496802704a",
            )
        elif name == "Amazon2018GroceryAndGourmetFood":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Grocery_and_Gourmet_Food.csv",
                "9652d130382a3f1fcbfffffcaf3b8474e2649be034fbea8b0281b78424b65d40",
            )
        elif name == "Amazon2018HomeAndKitchen":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Home_and_Kitchen.csv",
                "618e6c4493bcdd147a2bf3015bc0835dfedbc03570fba7d89335d9cd360069eb",
            )
        elif name == "Amazon2018IndustrialAndScientific":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Industrial_and_Scientific.csv",
                "29e194947309c1a0e81f0f9646fd6f63959949dbd807ea327e07074f35376a30",
            )
        elif name == "Amazon2018KindleStore":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Kindle_Store.csv",
                "f2fac32f72f51857f164c2c1671db141f06b2649608ebf1af2efba02a2fb219b",
            )
        elif name == "Amazon2018LuxuryBeauty":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Luxury_Beauty.csv",
                "5e1ab08a0147412d6a15ab4b8259df7fbc1fe09c747ba5c46486081ee4d68d24",
            )
        elif name == "Amazon2018MagazineSubscriptions":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Magazine_Subscriptions.csv",
                "40287d71ee0c49030ee222888fb21a95941c2c31344e15bdd2e58e0f63831c2d",
            )
        elif name == "Amazon2018MoviesAndTv":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Movies_and_TV.csv",
                "c7a6ca7769a34fd0d335e1cd25e359c18a8fcd474515f8b62986297e35b5fc4f",
            )
        elif name == "Amazon2018MusicalInstruments":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Musical_Instruments.csv",
                "8933b17434e4984bcce8cf4ec43d847e0af6aa6d46add28bbb37b80e06da1b06",
            )
        elif name == "Amazon2018OfficeProducts":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Office_Products.csv",
                "2e24f3df092efc71fa4dea41162c7c1ab2d46bc53c4cace63794a3a66dc6d82f",
            )
        elif name == "Amazon2018PatioLawnAndGarden":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Patio_Lawn_and_Garden.csv",
                "103438afc6ddb6a9416b94804bf86251b7d3b15bdf6cc50e90d6787008f08e31",
            )
        elif name == "Amazon2018PetSupplies":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Pet_Supplies.csv",
                "dac12cc077131bdf1c951cc0cc2016d6381e6b52eb65a3cb98456ce82a3c6bd9",
            )
        elif name == "Amazon2018PrimePantry":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Prime_Pantry.csv",
                "ed55b1f239c4ec3402fdd15a603a4b84210177678c36c01db59487a8fddf685c",
            )
        elif name == "Amazon2018Software":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Software.csv",
                "86d2ec7712b4c979bf7e7e984d39989b610c9f0e4ba4fc02c6aac7dcd9a15583",
            )
        elif name == "Amazon2018SportsAndOutdoors":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Sports_and_Outdoors.csv",
                "da8d746f1602d5ff01d4056c8f55b228996a30d40069b658d71388b0bf3df5d6",
            )
        elif name == "Amazon2018ToolsAndHomeImprovement":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Tools_and_Home_Improvement.csv",
                "1406d988afa38c62aeba1e6b33dada18a570fa6d8dd59cbc6e5229f8ecae0db0",
            )
        elif name == "Amazon2018ToysAndGames":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Toys_and_Games.csv",
                "cfdf96d55b3d923c913f3b139e7fabdc20360989db38527ef5947982aa246d45",
            )
        elif name == "Amazon2018VideoGames":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Video_Games.csv",
                "c3fec1cce4ee67f0d51f8b53a7e294d8bbe6f75ca1d8732256e900b3c46606d8",
            )
        else:
            raise ValueError(
                f'Unknown dataset name "{name}" for Amazon2018 dataloader!'
            )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        rating_file = next(Path.iterdir(Path(source_dir)))
        return pd.read_csv(
            rating_file,
            header=None,
            sep=",",
            names=[
                "item",
                "user",
                "rating",
                "timestamp",
            ],
        )
