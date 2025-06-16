import tarfile

import pandas as pd

from .loader import Loader


class ThirtyMusic(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with tarfile.open(f"{source_path}/ThirtyMusic.tar.gz", "r:gz") as tar:
            events = tar.extractfile("relations/events.idomaar")
            lines = events.readlines()
            data = []
            for line in lines:
                line = line.decode("utf-8").split("\t")
                event, timestamp, user_item = line[0], line[2], line[4]
                if event == "event.play":
                    user_item = eval(user_item)
                    subjects = user_item["subjects"][0]
                    objects = user_item["objects"][0]
                    if subjects["type"] == "user" and objects["type"] == "track":
                        user, item = subjects["id"], objects["id"]
                        data.append([user, item, timestamp])
            return pd.DataFrame(data, columns=[user_column_name, item_column_name, timestamp_column_name])
