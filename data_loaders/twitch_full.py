from .twitch import Twitch


class TwitchFull(Twitch):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "full_a"
        return super(TwitchFull, TwitchFull).load_from_file(source_path, user_column_name, item_column_name,
                                                            rating_column_name, timestamp_column_name, version=version)
