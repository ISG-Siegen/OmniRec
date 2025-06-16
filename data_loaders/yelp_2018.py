from .yelp import Yelp


class Yelp2018(Yelp):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "2018"
        return super(Yelp2018, Yelp2018).load_from_file(source_path, user_column_name, item_column_name,
                                                        rating_column_name, timestamp_column_name, version=version)
