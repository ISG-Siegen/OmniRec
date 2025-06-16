import pandas as pd

from .loader import Loader


class ModClothClothingFit(Loader):
    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        data = pd.read_json(f"{source_path}/modcloth_final_data.json.gz", compression="gzip", lines=True)[
            ["user_id", "item_id", "quality"]]
        data.rename(columns={"user_id": user_column_name, "item_id": item_column_name, "quality": rating_column_name},
                    inplace=True)
        return data
