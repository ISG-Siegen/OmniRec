from .konect import Konect


class YahooSongs(Konect):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "yahoo-song"
        has_timestamp = True
        return super(YahooSongs, YahooSongs).load_from_file(source_path, user_column_name, item_column_name,
                                                            rating_column_name, timestamp_column_name, version=version,
                                                            has_timestamp=has_timestamp)
