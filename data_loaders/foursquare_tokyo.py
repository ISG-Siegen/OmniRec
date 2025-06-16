from .foursquare import Foursquare


class FoursquareTokyo(Foursquare):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "TKY"
        return super(FoursquareTokyo, FoursquareTokyo).load_from_file(source_path, user_column_name,
                                                                      item_column_name, rating_column_name,
                                                                      timestamp_column_name, version=version)
