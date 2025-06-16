from .jester import Jester


class Jester3(Jester):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "3"
        return super(Jester3, Jester3).load_from_file(source_path, user_column_name, item_column_name,
                                                      rating_column_name, timestamp_column_name, version=version)
