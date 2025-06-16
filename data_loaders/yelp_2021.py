from .yelp import Yelp


class Yelp2021(Yelp):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "2019-2022"
        return super(Yelp2021, Yelp2021).load_from_file(source_path, user_column_name, item_column_name,
                                                        rating_column_name, timestamp_column_name, version=version)
