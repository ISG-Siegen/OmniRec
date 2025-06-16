from .foursquare import Foursquare


class FoursquareNYC2(Foursquare):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "NYC"
        return super(FoursquareNYC2, FoursquareNYC2).load_from_file(source_path, user_column_name,
                                                                    item_column_name, rating_column_name,
                                                                    timestamp_column_name, version=version)
