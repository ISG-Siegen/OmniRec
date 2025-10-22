TODO: Expand dataset overview
# Dataset Overview

The framework includes many built-in datasets. Use the exact name with the [`use_dataloader`](API_references.md#omnirec.recsys_data_set.RecSysDataSet.use_dataloader) function to load a dataset. Here is the comprehensive list with all dataset names:

| Dataset Name | Number of Users | Number of Items | Number of Ratings | Feedback Type |
|:---|---:|---:|---:|:---|
| **AdressaOneWeek** | 640.503 | 20.428 | 2.817.881 | implicit |
| **AlibabaIFashion** | 3.569.112 | 4.463.302 | 191.394.393 | implicit |
| **AlibabaMobile** | 10.000 | 2.876.947 | 4.686.904 | implicit |
| **Amazon2014Books** | 8.026.324 | 2.330.066 | 22.507.155 | explicit |
| **Amazon2014Electronics** | 4.201.696 | 476.002 | 7.824.482 | explicit |
| **Amazon2014MoviesAndTv** | 2.088.620 | 200.941 | 4.607.047 | explicit |
| **Amazon2014CdsAndVinyl** | 1.578.597 | 486.360 | 3.749.004 | explicit |
| **Amazon2014ClothingShoesAndJewelry** | 3.117.268 | 1.136.004 | 5.748.920 | explicit |
| **Amazon2014HomeAndKitchen** | 2.511.610 | 410.243 | 4.253.926 | explicit |
| **Amazon2014KindleStore** | 1.406.890 | 430.530 | 3.205.467 | explicit |
| **Amazon2014SportsAndOutdoors** | 1.990.521 | 478.898 | 3.268.695 | explicit |
| **Amazon2014CellPhonesAndAccessories** | 2.261.045 | 319.678 | 3.447.249 | explicit |
| **Amazon2014HealthAndPersonalCare** | 1.851.132 | 252.331 | 2.982.326 | explicit |
| **Amazon2014ToysAndGames** | 1.342.911 | 327.698 | 2.252.771 | explicit |
| **Amazon2014VideoGames** | 826.767 | 50.210 | 1.324.753 | explicit |
| **Amazon2014ToolsAndHomeImprovement** | 1.212.468 | 260.659 | 1.926.047 | explicit |
| **Amazon2014Beauty** | 1.210.271 | 249.274 | 2.023.070 | explicit |
| **Amazon2014AppsForAndroid** | 1.323.884 | 61.275 | 2.638.172 | explicit |
| **Amazon2014OfficeProducts** | 909.314 | 130.006 | 1.243.186 | explicit |
| **Amazon2014PetSupplies** | 740.985 | 103.288 | 1.235.316 | explicit |
| **Amazon2014Automotive** | 851.418 | 320.112 | 1.373.768 | explicit |
| **Amazon2014GroceryAndGourmetFood** | 768.438 | 166.049 | 1.297.156 | explicit |
| **Amazon2014PatioLawnAndGarden** | 714.791 | 105.984 | 993.490 | explicit |
| **Amazon2014Baby** | 531.890 | 64.426 | 915.446 | explicit |
| **Amazon2014DigitalMusic** | 478.235 | 266.414 | 836.006 | explicit |
| **Amazon2014MusicalInstruments** | 339.231 | 83.046 | 500.176 | explicit |
| **Amazon2014AmazonInstantVideo** | 426.922 | 23.965 | 583.933 | explicit |
| **Amazon2018AmazonFashion** | 186.189 | 749.233 | 875.121 | explicit |
| **Amazon2018AllBeauty** | 32.586 | 324.038 | 361.605 | explicit |
| **Amazon2018Appliances** | 30.252 | 515.650 | 590.844 | explicit |
| **Amazon2018ArtsCraftsAndSewing** | 302.809 | 1.579.230 | 2.733.842 | explicit |
| **Amazon2018Automotive** | 925.387 | 3.873.247 | 7.815.540 | explicit |
| **Amazon2018Books** | 2.930.451 | 15.362.619 | 51.062.224 | explicit |
| **Amazon2018CdsAndVinyl** | 434.060 | 1.944.316 | 4.458.901 | explicit |
| **Amazon2018CellPhonesAndAccessories** | 589.534 | 6.211.701 | 10.034.040 | explicit |
| **Amazon2018ClothingShoesAndJewelry** | 2.681.297 | 12.483.678 | 31.663.536 | explicit |
| **Amazon2018DigitalMusic** | 456.992 | 840.372 | 1.516.551 | explicit |
| **Amazon2018Electronics** | 756.489 | 9.838.676 | 20.553.480 | explicit |
| **Amazon2018GiftCards** | 1.548 | 128.877 | 147.136 | explicit |
| **Amazon2018GroceryAndGourmetFood** | 283.507 | 2.695.974 | 4.889.624 | explicit |
| **Amazon2018HomeAndKitchen** | 1.286.050 | 9.767.606 | 21.386.322 | explicit |
| **Amazon2018IndustrialAndScientific** | 165.764 | 1.246.131 | 1.711.995 | explicit |
| **Amazon2018KindleStore** | 493.849 | 2.409.262 | 5.704.334 | explicit |
| **Amazon2018LuxuryBeauty** | 12.120 | 416.174 | 535.310 | explicit |
| **Amazon2018MagazineSubscriptions** | 2.428 | 72.098 | 88.318 | explicit |
| **Amazon2018MoviesAndTv** | 182.032 | 3.826.085 | 8.506.849 | explicit |
| **Amazon2018MusicalInstruments** | 112.222 | 903.330 | 1.470.564 | explicit |
| **Amazon2018OfficeProducts** | 306.800 | 3.404.914 | 5.387.582 | explicit |
| **Amazon2018PatioLawnAndGarden** | 276.563 | 3.097.405 | 5.053.304 | explicit |
| **Amazon2018PetSupplies** | 198.402 | 3.085.591 | 6.254.167 | explicit |
| **Amazon2018PrimePantry** | 10.814 | 247.659 | 447.399 | explicit |
| **Amazon2018Software** | 21.663 | 375.147 | 450.578 | explicit |
| **Amazon2018SportsAndOutdoors** | 957.764 | 6.703.391 | 12.601.954 | explicit |
| **Amazon2018ToolsAndHomeImprovement** | 559.775 | 4.704.014 | 8.730.382 | explicit |
| **Amazon2018ToysAndGames** | 624.792 | 4.204.994 | 7.998.969 | explicit |
| **Amazon2018VideoGames** | 71.982 | 1.540.618 | 2.489.395 | explicit |
| **Amazon2023AllBeauty** | 632.000 | 112.600 | 701.500 | explicit |
| **Amazon2023AmazonFashion** | 2.000.000 | 825.900 | 2.500.000 | explicit |
| **Amazon2023Appliances** | 1.800.000 | 94.300 | 2.100.000 | explicit |
| **Amazon2023ArtsCraftsAndSewing** | 4.600.000 | 801.300 | 9.000.000 | explicit |
| **Amazon2023Automotive** | 8.000.000 | 2.000.000 | 20.000.000 | explicit |
| **Amazon2023BabyProducts** | 3.400.000 | 217.700 | 6.000.000 | explicit |
| **Amazon2023BeautyAndPersonalCare** | 11.300.000 | 1.000.000 | 23.900.000 | explicit |
| **Amazon2023Books** | 10.300.000 | 4.400.000 | 29.500.000 | explicit |
| **Amazon2023CdsAndVinyl** | 1.800.000 | 701.700 | 4.800.000 | explicit |
| **Amazon2023CellPhonesAndAccessories** | 11.600.000 | 1.300.000 | 20.800.000 | explicit |
| **Amazon2023ClothingShoesAndJewelry** | 22.600.000 | 7.200.000 | 66.000.000 | explicit |
| **Amazon2023DigitalMusic** | 101.000 | 70.500 | 130.400 | explicit |
| **Amazon2023Electronics** | 18.300.000 | 1.600.000 | 43.900.000 | explicit |
| **Amazon2023GiftCards** | 132.700 | 1.100 | 152.400 | explicit |
| **Amazon2023GroceryAndGourmetFood** | 7.000.000 | 603.200 | 14.300.000 | explicit |
| **Amazon2023HandmadeProducts** | 586.600 | 164.700 | 664.200 | explicit |
| **Amazon2023HealthAndHousehold** | 12.500.000 | 797.400 | 25.600.000 | explicit |
| **Amazon2023HealthAndPersonalCare** | 461.700 | 60.300 | 494.100 | explicit |
| **Amazon2023HomeAndKitchen** | 23.200.000 | 3.700.000 | 67.400.000 | explicit |
| **Amazon2023IndustrialAndScientific** | 3.400.000 | 427.500 | 5.200.000 | explicit |
| **Amazon2023KindleStore** | 5.600.000 | 1.600.000 | 25.600.000 | explicit |
| **Amazon2023MagazineSubscriptions** | 60.100 | 3.400 | 71.500 | explicit |
| **Amazon2023MoviesAndTv** | 6.500.000 | 747.800 | 17.300.000 | explicit |
| **Amazon2023MusicalInstruments** | 1.800.000 | 213.600 | 3.000.000 | explicit |
| **Amazon2023OfficeProducts** | 7.600.000 | 710.400 | 12.800.000 | explicit |
| **Amazon2023PatioLawnAndGarden** | 8.600.000 | 851.700 | 16.500.000 | explicit |
| **Amazon2023PetSupplies** | 7.800.000 | 492.700 | 16.800.000 | explicit |
| **Amazon2023Software** | 2.600.000 | 89.200 | 4.900.000 | explicit |
| **Amazon2023SportsAndOutdoors** | 10.300.000 | 1.600.000 | 19.600.000 | explicit |
| **Amazon2023SubscriptionBoxes** | 15.200 | 641 | 16.200 | explicit |
| **Amazon2023ToolsAndHomeImprovement** | 12.200.000 | 1.500.000 | 27.000.000 | explicit |
| **Amazon2023ToysAndGames** | 8.100.000 | 890.700 | 16.300.000 | explicit |
| **Amazon2023VideoGames** | 2.800.000 | 137.200 | 4.600.000 | explicit |
| **Amazon2023Unknown** | 23.100.000 | 13.200.000 | 63.800.000 | explicit |
| **Anime** | 73.515 | 11.200 | 7.813.730 | explicit |
| **BeerAdvocate** | 33.388 | 66.055 | 1.571.808 | explicit |
| **RateBeer** | 29.265 | 110.369 | 2.855.232 | explicit |
| **Behance** | 63.497 | 178.788 | 1.000.000 | implicit |
| **GoogleLocal2021Alabama** | 2.077.087 | 74.600 | 8.803.325 | explicit |
| **GoogleLocal2021Alaska** | 278.695 | 12.689 | 1.032.752 | explicit |
| **GoogleLocal2021Arizona** | 4.020.106 | 108.062 | 18.006.480 | explicit |
| **GoogleLocal2021Arkansas** | 1.217.718 | 47.076 | 5.013.709 | explicit |
| **GoogleLocal2021California** | 14.098.915 | 513.131 | 69.285.890 | explicit |
| **GoogleLocal2021Colorado** | 3.656.977 | 106.244 | 15.345.822 | explicit |
| **GoogleLocal2021Connecticut** | 1.419.448 | 48.936 | 5.089.012 | explicit |
| **GoogleLocal2021Delaware** | 566.738 | 14.620 | 1.855.170 | explicit |
| **GoogleLocal2021DistrictofColumbia** | 753.560 | 11.003 | 1.847.295 | explicit |
| **GoogleLocal2021Florida** | 13.832.724 | 376.192 | 60.543.660 | explicit |
| **GoogleLocal2021Georgia** | 5.620.482 | 165.395 | 23.570.208 | explicit |
| **GoogleLocal2021Hawaii** | 833.776 | 21.421 | 3.037.301 | explicit |
| **GoogleLocal2021Idaho** | 968.801 | 32.983 | 3.820.976 | explicit |
| **GoogleLocal2021Illinois** | 5.373.130 | 178.203 | 22.685.631 | explicit |
| **GoogleLocal2021Indiana** | 2.848.489 | 99.900 | 12.639.193 | explicit |
| **GoogleLocal2021Iowa** | 1.159.889 | 47.445 | 4.741.915 | explicit |
| **GoogleLocal2021Kansas** | 1.359.825 | 46.036 | 5.446.105 | explicit |
| **GoogleLocal2021Kentucky** | 1.873.160 | 62.862 | 7.507.829 | explicit |
| **GoogleLocal2021Louisiana** | 1.898.236 | 62.962 | 7.382.344 | explicit |
| **GoogleLocal2021Maine** | 575.257 | 24.666 | 2.169.983 | explicit |
| **GoogleLocal2021Maryland** | 2.858.778 | 77.680 | 10.513.574 | explicit |
| **GoogleLocal2021Massachusetts** | 2.639.379 | 91.894 | 10.260.857 | explicit |
| **GoogleLocal2021Michigan** | 4.008.458 | 158.116 | 20.409.484 | explicit |
| **GoogleLocal2021Minnesota** | 2.074.583 | 80.586 | 9.353.809 | explicit |
| **GoogleLocal2021Mississippi** | 1.056.414 | 36.932 | 3.788.144 | explicit |
| **GoogleLocal2021Missouri** | 2.982.323 | 98.939 | 13.167.690 | explicit |
| **GoogleLocal2021Montana** | 526.275 | 21.533 | 1.887.673 | explicit |
| **GoogleLocal2021Nebraska** | 798.181 | 29.877 | 3.219.434 | explicit |
| **GoogleLocal2021Nevada** | 2.565.244 | 48.009 | 8.683.291 | explicit |
| **GoogleLocal2021NewHampshire** | 748.007 | 24.624 | 2.602.125 | explicit |
| **GoogleLocal2021NewJersey** | 4.213.428 | 126.572 | 15.464.057 | explicit |
| **GoogleLocal2021NewMexico** | 1.136.149 | 34.512 | 4.600.323 | explicit |
| **GoogleLocal2021NewYork** | 8.086.412 | 270.717 | 32.891.500 | explicit |
| **GoogleLocal2021NorthCarolina** | 5.025.701 | 165.402 | 21.876.632 | explicit |
| **GoogleLocal2021NorthDakota** | 293.523 | 11.937 | 1.085.906 | explicit |
| **GoogleLocal2021Ohio** | 4.590.857 | 172.886 | 22.662.738 | explicit |
| **GoogleLocal2021Oklahoma** | 1.865.711 | 67.704 | 8.334.288 | explicit |
| **GoogleLocal2021Oregon** | 2.764.082 | 93.006 | 10.808.294 | explicit |
| **GoogleLocal2021Pennsylvania** | 4.957.916 | 189.836 | 21.574.012 | explicit |
| **GoogleLocal2021RhodeIsland** | 502.479 | 15.849 | 1.747.192 | explicit |
| **GoogleLocal2021SouthCarolina** | 2.964.113 | 84.539 | 11.749.061 | explicit |
| **GoogleLocal2021SouthDakota** | 412.911 | 14.167 | 1.420.224 | explicit |
| **GoogleLocal2021Tennessee** | 3.802.147 | 110.829 | 15.638.980 | explicit |
| **GoogleLocal2021Texas** | 13.545.569 | 444.948 | 65.178.288 | explicit |
| **GoogleLocal2021Utah** | 2.210.420 | 58.538 | 8.886.755 | explicit |
| **GoogleLocal2021Vermont** | 288.211 | 11.242 | 832.926 | explicit |
| **GoogleLocal2021Virginia** | 4.047.833 | 119.031 | 15.627.147 | explicit |
| **GoogleLocal2021Washington** | 3.360.838 | 120.641 | 16.249.980 | explicit |
| **GoogleLocal2021WestVirginia** | 631.093 | 23.359 | 2.163.197 | explicit |
| **GoogleLocal2021Wisconsin** | 2.257.895 | 91.522 | 10.071.305 | explicit |
| **GoogleLocal2021Wyoming** | 392.550 | 12.016 | 1.112.674 | explicit |
| **Gowalla** | 107.092 | 1.280.969 | 3.981.334 | implicit |
| **HetrecLastFM** | 1.892 | 12.523 | 71.064 | implicit |
| **MovieLens100K** | 943 | 1.682 | 100.000 | explicit |
| **MovieLens1BSynthetic** | 2.197.225 | 855.723 | 1.226.159.268 | implicit |
| **MovieLens20M** | 138.493 | 26.744 | 20.000.263 | explicit |
| **MovieLens25M** | 162.541 | 59.047 | 25.000.095 | explicit |
| **MovieLensLatest** | 330.975 | 83.239 | 33.832.162 | explicit |
| **MovieLensLatestSmall** | 610 | 9.724 | 100.836 | explicit |
| **MovieLens1M** | 6.040 | 3.706 | 1.000.209 | explicit |
| **MovieLens10M** | 69.878 | 10.677 | 10.000.054 | explicit |
| **Yelp2018** | 1.326.101 | 174.567 | 5.261.667 | explicit |
| **Yelp2019** | 1.637.138 | 192.606 | 6.461.396 | explicit |
| **Yelp2020** | 1.968.703 | 209.393 | 7.735.091 | explicit |
| **Yelp2021** | 2.189.457 | 160.585 | 8.345.614 | explicit |
| **Yelp2022** | 1.987.929 | 150.346 | 6.745.760 | explicit |
| **Yelp2023** | 1.987.929 | 150.346 | 6.745.760 | explicit |


## Listing Available Datasets

To see all registered datasets use [`list_datasets()`](API_references.md#omnirec.data_loaders.registry.list_datasets):

```python
from omnirec.data_loaders.registry import list_datasets

available_datasets = list_datasets()
print("Available datasets:", available_datasets)
```