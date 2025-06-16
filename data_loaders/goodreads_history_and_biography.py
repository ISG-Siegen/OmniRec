from .goodreads import Goodreads


class GoodreadsHistoryAndBiography(Goodreads):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "history_biography"
        return super(GoodreadsHistoryAndBiography, GoodreadsHistoryAndBiography).load_from_file(source_path,
                                                                                                user_column_name,
                                                                                                item_column_name,
                                                                                                rating_column_name,
                                                                                                timestamp_column_name,
                                                                                                version=version)
