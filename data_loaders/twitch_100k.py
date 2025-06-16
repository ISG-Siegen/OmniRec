import pandas as pd

from .twitch import Twitch


class Twitch100K(Twitch):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "100k_a"
        return super(Twitch100K, Twitch100K).load_from_file(source_path, user_column_name, item_column_name,
                                                            rating_column_name, timestamp_column_name, version=version)
