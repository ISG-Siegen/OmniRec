import gzip
import pandas as pd

from .loader import Loader


class Beer(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with gzip.open(f"{source_path}/{additional_parameters['version']}.json.gz", "r") as gz:
            file = gz.readlines()
            final_dict = {user_column_name: [], item_column_name: [], rating_column_name: [], timestamp_column_name: []}
            for line in file:
                dic = eval(line)
                if all(k in dic for k in
                       ("review/profileName", "beer/beerId", "review/overall", "review/time")):
                    final_dict[user_column_name].append(dic['review/profileName'])
                    final_dict[item_column_name].append(dic['beer/beerId'])
                    final_dict[rating_column_name].append(dic['review/overall'])
                    final_dict[timestamp_column_name].append(dic['review/time'])
            data = pd.DataFrame.from_dict(final_dict)

            if additional_parameters['version'] == "ratebeer":
                data[rating_column_name] = data[rating_column_name].apply(lambda x: x.split('/')[0])

            return data
