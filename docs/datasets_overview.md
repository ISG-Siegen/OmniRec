TODO: Expand dataset overview
# Dataset Overview

The framework includes many built-in datasets. Use the exact name with the `use_dataloader` function to load a dataset. Here is the comprehensive list with all dataset names:

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
| MovieLens100K               | Movies              | Explicit   | GroupLens      |
| HetrecLastFM                | Music               | Implicit   | HetRec         |


## Listing Available Datasets

To see all registered datasets:

```python
from omnirec.data_loaders.registry import list_datasets

available_datasets = list_datasets()
print("Available datasets:", available_datasets)
```