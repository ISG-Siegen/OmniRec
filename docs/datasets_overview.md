TODO: Expand dataset overview
# Dataset Overview

The framework includes many built-in datasets. Use the exact name with the [`use_dataloader`](API_references.md#omnirec.recsys_data_set.RecSysDataSet.use_dataloader) function to load a dataset. Here is the comprehensive list with all dataset names:

| Name                        | Type/Domain         | Feedback   | Source         |
|-----------------------------|---------------------|------------|----------------|
| Amazon2014Books             | Books               | Explicit   | Amazon/SNAP    |
| Amazon2014Electronics       | Electronics         | Explicit   | Amazon/SNAP    |
| Amazon2014MoviesAndTv       | Movies & TV         | Explicit   | Amazon/SNAP    |
| Amazon2014CdsAndVinyl       | Music               | Explicit   | Amazon/SNAP    |
| Amazon2014ClothingShoesAndJewelry | Fashion      | Explicit   | Amazon/SNAP    |
| Amazon2014HomeAndKitchen    | Home & Kitchen      | Explicit   | Amazon/SNAP    |
| Amazon2014KindleStore       | eBooks              | Explicit   | Amazon/SNAP    |
| Amazon2014SportsAndOutdoors | Sports              | Explicit   | Amazon/SNAP    |
| Amazon2014CellPhonesAndAccessories | Phones      | Explicit   | Amazon/SNAP    |
| Amazon2014HealthAndPersonalCare | Health          | Explicit   | Amazon/SNAP    |
| Amazon2014ToysAndGames      | Toys & Games        | Explicit   | Amazon/SNAP    |
| Amazon2014VideoGames        | Video Games         | Explicit   | Amazon/SNAP    |
| Amazon2014ToolsAndHomeImprovement | Tools        | Explicit   | Amazon/SNAP    |
| Amazon2014Beauty            | Beauty              | Explicit   | Amazon/SNAP    |
| Amazon2014AppsForAndroid    | Android Apps        | Explicit   | Amazon/SNAP    |
| Amazon2014OfficeProducts    | Office              | Explicit   | Amazon/SNAP    |
| Amazon2014PetSupplies       | Pets                | Explicit   | Amazon/SNAP    |
| Amazon2014Automotive        | Automotive          | Explicit   | Amazon/SNAP    |
| Amazon2014GroceryAndGourmetFood | Grocery        | Explicit   | Amazon/SNAP    |
| Amazon2014PatioLawnAndGarden | Garden            | Explicit   | Amazon/SNAP    |
| Amazon2014Baby              | Baby                | Explicit   | Amazon/SNAP    |
| Amazon2014DigitalMusic      | Digital Music       | Explicit   | Amazon/SNAP    |
| Amazon2014MusicalInstruments| Instruments         | Explicit   | Amazon/SNAP    |
| Amazon2014AmazonInstantVideo| Video Streaming     | Explicit   | Amazon/SNAP    |
| Amazon2018AmazonFashion    | Fashion             | Explicit   | Amazon         |
| Amazon2018AllBeauty        | Beauty              | Explicit   | Amazon         |
| Amazon2018Appliances       | Home Appliances     | Explicit   | Amazon         |
| Amazon2018ArtsCraftsAndSewing | Arts & Crafts    | Explicit   | Amazon         |
| Amazon2018Automotive       | Automotive          | Explicit   | Amazon         |
| Amazon2018Books            | Books               | Explicit   | Amazon         |
| Amazon2018CdsAndVinyl      | Music               | Explicit   | Amazon         |
| Amazon2018CellPhonesAndAccessories | Phones       | Explicit   | Amazon         |
| Amazon2018ClothingShoesAndJewelry | Fashion      | Explicit   | Amazon         |
| Amazon2018DigitalMusic     | Digital Music       | Explicit   | Amazon         |
| Amazon2018Electronics      | Electronics         | Explicit   | Amazon         |
| Amazon2018GiftCards        | Gift Cards          | Explicit   | Amazon         |
| Amazon2018GroceryAndGourmetFood | Grocery        | Explicit   | Amazon         |
| Amazon2018HomeAndKitchen   | Home & Kitchen      | Explicit   | Amazon         |
| Amazon2018IndustrialAndScientific | Industrial    | Explicit   | Amazon         |
| Amazon2018KindleStore      | eBooks              | Explicit   | Amazon         |
| Amazon2018LuxuryBeauty     | Luxury Beauty       | Explicit   | Amazon         |
| Amazon2018MagazineSubscriptions | Magazines      | Explicit   | Amazon         |
| Amazon2018MoviesAndTv      | Movies & TV         | Explicit   | Amazon         |
| Amazon2018MusicalInstruments | Instruments       | Explicit   | Amazon         |
| Amazon2018OfficeProducts   | Office              | Explicit   | Amazon         |
| Amazon2018PatioLawnAndGarden | Garden           | Explicit   | Amazon         |
| Amazon2018PetSupplies      | Pets                | Explicit   | Amazon         |
| Amazon2018PrimePantry      | Prime Pantry        | Explicit   | Amazon         |
| Amazon2018Software         | Software            | Explicit   | Amazon         |
| Amazon2018SportsAndOutdoors | Sports             | Explicit   | Amazon         |
| Amazon2018ToolsAndHomeImprovement | Tools        | Explicit   | Amazon         |
| Amazon2018ToysAndGames     | Toys & Games        | Explicit   | Amazon         |
| Amazon2018VideoGames       | Video Games         | Explicit   | Amazon         |
| Amazon2023AllBeauty | Beauty | Explicit | Amazon |
| Amazon2023AmazonFashion | Fashion | Explicit | Amazon |
| Amazon2023Appliances | Home Appliances | Explicit | Amazon |
| Amazon2023ArtsCraftsAndSewing | Arts & Crafts | Explicit | Amazon |
| Amazon2023Automotive | Automotive | Explicit | Amazon |
| Amazon2023BabyProducts | Baby | Explicit | Amazon |
| Amazon2023BeautyAndPersonalCare | Beauty & Personal Care | Explicit | Amazon |
| Amazon2023Books | Books | Explicit | Amazon |
| Amazon2023CdsAndVinyl | Music | Explicit | Amazon |
| Amazon2023CellPhonesAndAccessories | Phones | Explicit | Amazon |
| Amazon2023ClothingShoesAndJewelry | Fashion | Explicit | Amazon |
| Amazon2023DigitalMusic | Digital Music | Explicit | Amazon |
| Amazon2023Electronics | Electronics | Explicit | Amazon |
| Amazon2023GiftCards | Gift Cards | Explicit | Amazon |
| Amazon2023GroceryAndGourmetFood | Grocery | Explicit | Amazon |
| Amazon2023HandmadeProducts | Handmade | Explicit | Amazon |
| Amazon2023HealthAndHousehold | Health & Household | Explicit | Amazon |
| Amazon2023HealthAndPersonalCare | Health & Personal Care | Explicit | Amazon |
| Amazon2023HomeAndKitchen | Home & Kitchen | Explicit | Amazon |
| Amazon2023IndustrialAndScientific | Industrial | Explicit | Amazon |
| Amazon2023KindleStore | eBooks | Explicit | Amazon |
| Amazon2023MagazineSubscriptions | Magazines | Explicit | Amazon |
| Amazon2023MoviesAndTv | Movies & TV | Explicit | Amazon |
| Amazon2023MusicalInstruments | Instruments | Explicit | Amazon |
| Amazon2023OfficeProducts | Office | Explicit | Amazon |
| Amazon2023PatioLawnAndGarden | Garden | Explicit | Amazon |
| Amazon2023PetSupplies | Pets | Explicit | Amazon |
| Amazon2023Software | Software | Explicit | Amazon |
| Amazon2023SportsAndOutdoors | Sports | Explicit | Amazon |
| Amazon2023SubscriptionBoxes | Subscription Boxes | Explicit | Amazon |
| Amazon2023ToolsAndHomeImprovement | Tools | Explicit | Amazon |
| Amazon2023ToysAndGames | Toys & Games | Explicit | Amazon |
| Amazon2023VideoGames | Video Games | Explicit | Amazon |
| Amazon2023Unknown | Unknown | Explicit | Amazon |
| MovieLens100K | Movies | Explicit | GroupLens |
| HetrecLastFM | Music | Implicit | HetRec |


## Listing Available Datasets

To see all registered datasets use [`list_datasets()`](API_references.md#omnirec.data_loaders.registry.list_datasets):

```python
from omnirec.data_loaders.registry import list_datasets

available_datasets = list_datasets()
print("Available datasets:", available_datasets)
```