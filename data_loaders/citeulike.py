import zipfile
import pandas as pd

from .loader import Loader


class CiteULike(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/{additional_parameters['version']}.zip") as zipf:
            with zipf.open(f"{additional_parameters['version']}/users.dat") as file:
                u_i_pairs = []
                for user, line in enumerate(file.readlines()):
                    line = line.decode("utf-8")
                    item_cnt = line.strip("\n").split(" ")[0]
                    items = line.strip("\n").split(" ")[1:]
                    assert len(items) == int(item_cnt)
                    for item in items:
                        assert item.isdecimal()
                        u_i_pairs.append((user, int(item)))
                return pd.DataFrame(u_i_pairs, columns=["user", "item"])
