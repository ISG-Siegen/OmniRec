from .goodreads import Goodreads


class GoodreadsYoungAdult(Goodreads):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "young_adult"
        return super(GoodreadsYoungAdult, GoodreadsYoungAdult).load_from_file(source_path, user_column_name,
                                                                              item_column_name, rating_column_name,
                                                                              timestamp_column_name, version=version)
