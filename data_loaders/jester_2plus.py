from .jester import Jester


class Jester2Plus(Jester):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "2Plus"
        return super(Jester2Plus, Jester2Plus).load_from_file(source_path, user_column_name, item_column_name,
                                                              rating_column_name, timestamp_column_name,
                                                              version=version)
