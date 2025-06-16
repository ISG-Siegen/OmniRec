from .goodreads import Goodreads


class GoodreadsChildren(Goodreads):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "children"
        return super(GoodreadsChildren, GoodreadsChildren).load_from_file(source_path, user_column_name,
                                                                          item_column_name, rating_column_name,
                                                                          timestamp_column_name, version=version)
