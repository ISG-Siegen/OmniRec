from enum import StrEnum, auto


class DataSet(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> str:
        return name  # keep exact case for using auto

    Amazon2014Books = auto()
    Amazon2014Electronics = auto()
    Amazon2014MoviesAndTv = auto()
    Amazon2014CdsAndVinyl = auto()
    Amazon2014ClothingShoesAndJewelry = auto()
    Amazon2014HomeAndKitchen = auto()
    Amazon2014KindleStore = auto()
    Amazon2014SportsAndOutdoors = auto()
    Amazon2014CellPhonesAndAccessories = auto()
    Amazon2014HealthAndPersonalCare = auto()
    Amazon2014ToysAndGames = auto()
    Amazon2014VideoGames = auto()
    Amazon2014ToolsAndHomeImprovement = auto()
    Amazon2014Beauty = auto()
    Amazon2014AppsForAndroid = auto()
    Amazon2014OfficeProducts = auto()
    Amazon2014PetSupplies = auto()
    Amazon2014Automotive = auto()
    Amazon2014GroceryAndGourmetFood = auto()
    Amazon2014PatioLawnAndGarden = auto()
    Amazon2014Baby = auto()
    Amazon2014DigitalMusic = auto()
    Amazon2014MusicalInstruments = auto()
    Amazon2014AmazonInstantVideo = auto()
    HetrecLastFM = auto()
    MovieLens100K = auto()
