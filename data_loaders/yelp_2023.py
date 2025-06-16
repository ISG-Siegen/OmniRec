from .yelp import Yelp


class Yelp2023(Yelp):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "2023"
        return super(Yelp2023, Yelp2023).load_from_file(source_path, user_column_name, item_column_name,
                                                        rating_column_name, timestamp_column_name, version=version)
