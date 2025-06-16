from .goodreads import Goodreads


class GoodreadsPoetry(Goodreads):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "poetry"
        return super(GoodreadsPoetry, GoodreadsPoetry).load_from_file(source_path, user_column_name, item_column_name,
                                                                      rating_column_name, timestamp_column_name,
                                                                      version=version)
