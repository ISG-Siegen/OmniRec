from .goodreads import Goodreads


class GoodreadsMysteryThrillerAndCrime(Goodreads):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "mystery_thriller_crime"
        return super(GoodreadsMysteryThrillerAndCrime,
                     GoodreadsMysteryThrillerAndCrime).load_from_file(source_path,
                                                                      user_column_name,
                                                                      item_column_name,
                                                                      rating_column_name,
                                                                      timestamp_column_name,
                                                                      version=version)
