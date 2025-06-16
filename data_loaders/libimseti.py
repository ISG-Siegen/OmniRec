from .konect import Konect


class Libimseti(Konect):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "libimseti"
        has_timestamp = False
        return super(Libimseti, Libimseti).load_from_file(source_path, user_column_name, item_column_name,
                                                          rating_column_name, timestamp_column_name, version=version,
                                                          has_timestamp=has_timestamp)
