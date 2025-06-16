from .goodreads import Goodreads


class GoodreadsFantasyAndParanormal(Goodreads):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "fantasy_paranormal"
        return super(GoodreadsFantasyAndParanormal, GoodreadsFantasyAndParanormal).load_from_file(source_path,
                                                                                                  user_column_name,
                                                                                                  item_column_name,
                                                                                                  rating_column_name,
                                                                                                  timestamp_column_name,
                                                                                                  version=version)
