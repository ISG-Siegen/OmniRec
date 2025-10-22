from pathlib import Path

import pandas as pd
from pandas import DataFrame

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _loader


@_loader(
    [
        "GoogleLocal2021Alabama",
        "GoogleLocal2021Alaska",
        "GoogleLocal2021Arizona",
        "GoogleLocal2021Arkansas",
        "GoogleLocal2021California",
        "GoogleLocal2021Colorado",
        "GoogleLocal2021Connecticut",
        "GoogleLocal2021Delaware",
        "GoogleLocal2021DistrictofColumbia",
        "GoogleLocal2021Florida",
        "GoogleLocal2021Georgia",
        "GoogleLocal2021Hawaii",
        "GoogleLocal2021Idaho",
        "GoogleLocal2021Illinois",
        "GoogleLocal2021Indiana",
        "GoogleLocal2021Iowa",
        "GoogleLocal2021Kansas",
        "GoogleLocal2021Kentucky",
        "GoogleLocal2021Louisiana",
        "GoogleLocal2021Maine",
        "GoogleLocal2021Maryland",
        "GoogleLocal2021Massachusetts",
        "GoogleLocal2021Michigan",
        "GoogleLocal2021Minnesota",
        "GoogleLocal2021Mississippi",
        "GoogleLocal2021Missouri",
        "GoogleLocal2021Montana",
        "GoogleLocal2021Nebraska",
        "GoogleLocal2021Nevada",
        "GoogleLocal2021NewHampshire",
        "GoogleLocal2021NewJersey",
        "GoogleLocal2021NewMexico",
        "GoogleLocal2021NewYork",
        "GoogleLocal2021NorthCarolina",
        "GoogleLocal2021NorthDakota",
        "GoogleLocal2021Ohio",
        "GoogleLocal2021Oklahoma",
        "GoogleLocal2021Oregon",
        "GoogleLocal2021Pennsylvania",
        "GoogleLocal2021RhodeIsland",
        "GoogleLocal2021SouthCarolina",
        "GoogleLocal2021SouthDakota",
        "GoogleLocal2021Tennessee",
        "GoogleLocal2021Texas",
        "GoogleLocal2021Utah",
        "GoogleLocal2021Vermont",
        "GoogleLocal2021Virginia",
        "GoogleLocal2021Washington",
        "GoogleLocal2021WestVirginia",
        "GoogleLocal2021Wisconsin",
        "GoogleLocal2021Wyoming",
    ]
)
class GoogleLocal2021(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        if name == "GoogleLocal2021Alabama":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Alabama.csv.gz",
                "4d528f858f093c0c1ab18278e6209364a1b48e58e0a52fad14609f6372ebe29b",
            )
        elif name == "GoogleLocal2021Alaska":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Alaska.csv.gz",
                "8c61b14e6770d40d30a3838ec26a15511648c4359e33d6169f9d87eca7ffd0b5",
            )
        elif name == "GoogleLocal2021Arizona":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Arizona.csv.gz",
                "d39a079bbf024f5d80c7afd47999bc970469ca729169521dc5122e92bc678673",
            )
        elif name == "GoogleLocal2021Arkansas":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Arkansas.csv.gz",
                "2d6e48b5b76a1526e8f6fb574355febd86cc7356cede0f39f63508f15174b308",
            )
        elif name == "GoogleLocal2021California":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-California.csv.gz",
                "b7577525537c6b99ed2ab089ffd169211827ba70c20430661b419bc019995cf8",
            )
        elif name == "GoogleLocal2021Colorado":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Colorado.csv.gz",
                "09f8d2ac059b8f9e97878a38953a95f6329daa8a5a0e1373c5bf0b573417f010",
            )
        elif name == "GoogleLocal2021Connecticut":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Connecticut.csv.gz",
                "b67649a5d8a78581cc33bfc9cdb3f60f603bdfee55d14b7aa16cc02884c2e94f",
            )
        elif name == "GoogleLocal2021Delaware":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Delaware.csv.gz",
                "b29656f03cf078542bfccea5138378ebeb007ec80b4f1eea1c0b583286e5667e",
            )
        elif name == "GoogleLocal2021DistrictofColumbia":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-District_of_Columbia.csv.gz",
                "0b75a6fca2b522cbc6741c6d6e550bb5f737dd0b0f75ec264f28ff9ebe115890",
            )
        elif name == "GoogleLocal2021Florida":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Florida.csv.gz",
                "7549f633771111123310be207053d7fa567e64797f5bd0edb482d02cd71a3655",
            )
        elif name == "GoogleLocal2021Georgia":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Georgia.csv.gz",
                "46d98935ea3c98a9b86e2735795ed4b135c5e48af88d218e6643ee62238d922c",
            )
        elif name == "GoogleLocal2021Hawaii":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Hawaii.csv.gz",
                "be4d7dd2efaac5eb5c5f63410c8373ea54d1450f13e53c8a0170e9fa5d5f17c6",
            )
        elif name == "GoogleLocal2021Idaho":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Idaho.csv.gz",
                "9281799dc5e5a1660d2b214027f8200f6cc30ce78565f7d5ea07e18d1f3acb86",
            )
        elif name == "GoogleLocal2021Illinois":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Illinois.csv.gz",
                "720def94e2c6ad4bfc5c989fac61a820b50aab96edfd5a5cd344aedae278f863",
            )
        elif name == "GoogleLocal2021Indiana":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Indiana.csv.gz",
                "bbe02812a470cff5889d530cb949da784553e10a21f2f13e1210ff857e8e54e9",
            )
        elif name == "GoogleLocal2021Iowa":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Iowa.csv.gz",
                "78e68fa196ddcc16d91a0e812f5d4fbd0ff4ca40124b94e23af8bce8357bdde6",
            )
        elif name == "GoogleLocal2021Kansas":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Kansas.csv.gz",
                "e56c262ef0ab95b0122bfcee4b92aa74680b756441d223c58249f1afb8d9a09a",
            )
        elif name == "GoogleLocal2021Kentucky":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Kentucky.csv.gz",
                "92d148551f8b395165e87116118cbb95ae0130650a0553a229bdee0003ed42da",
            )
        elif name == "GoogleLocal2021Louisiana":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Louisiana.csv.gz",
                "ca9675ba6eb7dbbd56fd7822fdb75e73fdd22456561791fe158bf0fde4c33ca0",
            )
        elif name == "GoogleLocal2021Maine":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Maine.csv.gz",
                "a2300cd045fa752e9b3e85fb2f91d5218f80fc8358d3b8349e07318e250b5ab1",
            )
        elif name == "GoogleLocal2021Maryland":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Maryland.csv.gz",
                "cb62b0c4862ba2e71b92c4065870056b23b66fce5653a26f1159a165f78cc4eb",
            )
        elif name == "GoogleLocal2021Massachusetts":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Massachusetts.csv.gz",
                "30425608e95ce9a40796f9a96bb1fc014df0ae4cb1bf7546c7440ff509f5348a",
            )
        elif name == "GoogleLocal2021Michigan":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Michigan.csv.gz",
                "6a3394dd052aa7b242f370f32f96b65ea3032420ad2862d4a686bbd1137bf21c",
            )
        elif name == "GoogleLocal2021Minnesota":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Minnesota.csv.gz",
                "b98052125e7306b0caa9ba9b16d47d64c40f3244f53724107677f650b55a8969",
            )
        elif name == "GoogleLocal2021Mississippi":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Mississippi.csv.gz",
                "8d180f638f02817f67d463bd6f0b5874fe81d46f2f9f9caf8a5a06715d2c92d8",
            )
        elif name == "GoogleLocal2021Missouri":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Missouri.csv.gz",
                "e7e80be7bbc8da9ba26e3c56cad5787089782b22f35943534c94649455597c57",
            )
        elif name == "GoogleLocal2021Montana":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Montana.csv.gz",
                "ec9bb219fa0ca6971f0d92beba74099cd4e21f60043f731ab0fb9bc0adaa6afe",
            )
        elif name == "GoogleLocal2021Nebraska":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Nebraska.csv.gz",
                "5e94ce5026690d321680280db3586048a4c8fa789b52cc0ac9b1bc8c7779aef5",
            )
        elif name == "GoogleLocal2021Nevada":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Nevada.csv.gz",
                "59f8f23e707a4cab924bb82e588ffbe39a2b91037580aa1b6ec4d90445dad809",
            )
        elif name == "GoogleLocal2021NewHampshire":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-New_Hampshire.csv.gz",
                "7face3de04b1859448ec50646119483bd1e1c45d83c8fe92f07c8bd88de212a0",
            )
        elif name == "GoogleLocal2021NewJersey":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-New_Jersey.csv.gz",
                "000d0abc75fb91afa10ef9f681dfe76652da4a3a30a57e44c21f1a8c3088c261",
            )
        elif name == "GoogleLocal2021NewMexico":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-New_Mexico.csv.gz",
                "6437457c168cc2946a38a733ae703d6a37311732c2da368d26fd5d984b10aa32",
            )
        elif name == "GoogleLocal2021NewYork":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-New_York.csv.gz",
                "cdf9f81e8f2e3e05ab1a62ee9dde052bf3d1d9c916df6849bdf4250fa3b2eaff",
            )
        elif name == "GoogleLocal2021NorthCarolina":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-North_Carolina.csv.gz",
                "bd14702263b32f31cb8199fde7c9f8a0a99b89d378b8343306ae45ed7efc2869",
            )
        elif name == "GoogleLocal2021NorthDakota":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-North_Dakota.csv.gz",
                "5bef4edca2d4f5f3011137a098a87b362d6f13a066cfbb2ad378f93fc6444e2d",
            )
        elif name == "GoogleLocal2021Ohio":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Ohio.csv.gz",
                "79d33ba5155f7f21a04f68a7fa560e80acef5c74d042f72125e850ba25db360f",
            )
        elif name == "GoogleLocal2021Oklahoma":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Oklahoma.csv.gz",
                "58fe83f26a093405a94ab8bb6f06ba6a98c5c4b002acc2790eb30e6e975dacfd",
            )
        elif name == "GoogleLocal2021Oregon":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Oregon.csv.gz",
                "c986fb79ba11227011507b3aa3f3aa5e9e8ebe7b8132ea1da2075759023aa84b",
            )
        elif name == "GoogleLocal2021Pennsylvania":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Pennsylvania.csv.gz",
                "fe6c02754ee66a81473dcf5034ac0e5a178a08b62739b50f0d29041c0e00c801",
            )
        elif name == "GoogleLocal2021RhodeIsland":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Rhode_Island.csv.gz",
                "17eb09485ec69a627a9d6e11e68094b4c5a4f9fb44c9ada6134f024e7febe713",
            )
        elif name == "GoogleLocal2021SouthCarolina":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-South_Carolina.csv.gz",
                "7d5839df7dc6ee56fd168ff85cac6e38c578f10cb157e541151fb91edeb0c6a0",
            )
        elif name == "GoogleLocal2021SouthDakota":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-South_Dakota.csv.gz",
                "597aad9215dc51c9dff89c077e85e2bc596c3bd95848d279eb8b68a742ad8d9e",
            )
        elif name == "GoogleLocal2021Tennessee":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Tennessee.csv.gz",
                "c3e03824b822a46d65f18270c90d5c8c3ffe787a5a9ab3d47fb1e4c43fee2a78",
            )
        elif name == "GoogleLocal2021Texas":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Texas.csv.gz",
                "1513471ed729adcabb81cdb3e2a3d2d4673b920202f88c882fc05c4ca3bdb32e",
            )
        elif name == "GoogleLocal2021Utah":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Utah.csv.gz",
                "5c2547dc97dd6c6f49b1abbca43b12033eede8d845cfd8a9e95878622066106d",
            )
        elif name == "GoogleLocal2021Vermont":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Vermont.csv.gz",
                "8c8f6bba9a47302eac681feccd186c8d3404da4a2fba4896e149d30e9272d102",
            )
        elif name == "GoogleLocal2021Virginia":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Virginia.csv.gz",
                "d170d262b332f3af414250693abd4f7bf50fe9d90a6f8ba0557c495a5530768f",
            )
        elif name == "GoogleLocal2021Washington":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Washington.csv.gz",
                "1e3ed9a90c1172629909508a5671556cee3b65d6061d6d92eee00ecea70cc84c",
            )
        elif name == "GoogleLocal2021WestVirginia":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-West_Virginia.csv.gz",
                "5207904a1c14519658b791358fcc8c50ea5e0e7a61fb400a7f5fca5c70a5b99b",
            )
        elif name == "GoogleLocal2021Wisconsin":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Wisconsin.csv.gz",
                "1570cb61329671346e5090d75d0bda8ee6b906c1265ab39541e0002e7c95a6a1",
            )
        elif name == "GoogleLocal2021Wyoming":
            return DatasetInfo(
                "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Wyoming.csv.gz",
                "d62cf66742722e20f71bdf94edc27111d6d05122893aea41c4aaf1fcf3b468ae",
            )
        else:
            raise ValueError(
                f'Unknown dataset name "{name}" for GoogleLocal2021 dataloader!'
            )

    @staticmethod
    def load(source_dir: Path, name: str) -> DataFrame:
        rating_archive = next(Path.iterdir(Path(source_dir)))
        return pd.read_csv(
            rating_archive,
            compression="gzip",
            sep=",",
            header=0,
            names=["item", "user", "rating", "timestamp"],
        )[["user", "item", "rating", "timestamp"]]
