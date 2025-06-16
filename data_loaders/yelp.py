import tarfile
import zipfile

import pandas as pd

from .loader import Loader


class Yelp(Loader):
    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        if additional_parameters["version"] == "2018":
            with zipfile.ZipFile(f"{source_path}/archive.zip", 'r') as zipf:
                with tarfile.open(fileobj=zipf.open('dataset.tgz'), mode='r:gz') as tar:
                    file = tar.extractfile('yelp_academic_dataset_review.json')
                    lines = file.readlines()
        elif additional_parameters["version"] == "2019-2022":
            with zipfile.ZipFile(f"{source_path}/archive.zip", 'r') as zipf:
                file = zipf.open('yelp_academic_dataset_review.json')
                lines = file.readlines()
        elif additional_parameters["version"] == "2023":
            with tarfile.open(f"{source_path}/yelp_dataset.tar", mode='r') as tar:
                file = tar.extractfile('yelp_academic_dataset_review.json')
                lines = file.readlines()

        final_dict = {user_column_name: [], item_column_name: [], rating_column_name: [],
                      timestamp_column_name: []}
        for line in lines:
            line = line.decode('utf-8')
            dic = eval(line)
            if all(k in dic for k in ("user_id", "business_id", "stars", "date")):
                final_dict[user_column_name].append(dic['user_id'])
                final_dict[item_column_name].append(dic['business_id'])
                final_dict[rating_column_name].append(dic['stars'])
                final_dict[timestamp_column_name].append(dic['date'])
        return pd.DataFrame.from_dict(final_dict)
