import json
import tarfile
import pandas as pd

from .loader import Loader


class AdressaOneWeek(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        data = []
        with tarfile.open(f"{source_path}/one_week.tar.gz", "r:gz") as tar:
            for file in ["20170101", "20170102", "20170103", "20170104", "20170105", "20170106", "20170107"]:
                day = tar.extractfile(f"one_week/{file}")
                file_data = []
                for line in day.readlines():
                    line_data = json.loads(line)
                    if "id" in line_data and "userId" in line_data:
                        file_data.append([line_data["userId"], line_data["id"], line_data["time"]])
                data.append(
                    pd.DataFrame(file_data, columns=[user_column_name, item_column_name, timestamp_column_name]))
            return pd.concat(data)
