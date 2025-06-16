import zipfile
import pandas as pd

from .loader import Loader


class DocearMindMaps(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/docear-datasets-mindmaps.zip") as zipf:
            data = []
            for num in [str(i).zfill(2) for i in range(17)]:
                with zipf.open(f"mindmaps/mindmaps/mindmaps-papers_{num}.csv") as file:
                    data.append(pd.read_csv(file, header=0, sep="\t", usecols=[1, 3, 5],
                                            names=[timestamp_column_name, item_column_name, user_column_name])[
                                    [user_column_name, item_column_name, timestamp_column_name]])
            return pd.concat(data, ignore_index=True)
