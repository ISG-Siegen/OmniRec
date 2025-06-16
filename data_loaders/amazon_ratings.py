from .konect import Konect


class AmazonRatings(Konect):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "amazon-ratings"
        has_timestamp = True
        return super(AmazonRatings, AmazonRatings).load_from_file(source_path, user_column_name, item_column_name,
                                                                  rating_column_name, timestamp_column_name,
                                                                  version=version, has_timestamp=has_timestamp)
