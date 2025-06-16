import zipfile
import numpy as np
import pandas as pd

from .loader import Loader


class FoodComRecipes(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/archive.zip") as zipf:
            with zipf.open("RAW_interactions.csv") as file:
                final_dict = {user_column_name: [], item_column_name: [], rating_column_name: [],
                              timestamp_column_name: []}
                lines = file.readlines()[1:]
                for line in lines:
                    decoded_line = line.decode("utf-8", "replace")
                    line_data = decoded_line.split(",")
                    if len(line_data) >= 4 and line_data[0].isdigit() and line_data[1].isdigit():
                        final_dict[user_column_name].append(line_data[0])
                        final_dict[item_column_name].append(line_data[1])
                        final_dict[rating_column_name].append(line_data[3])
                        final_dict[timestamp_column_name].append(line_data[2])
                data = pd.DataFrame.from_dict(final_dict)
                data.loc[data[rating_column_name] == 0, rating_column_name] = np.nan
                data = data.astype({rating_column_name: 'int64'})
                return data
