from .foursquare_global import FoursquareGlobal


class FoursquareGlobal2(FoursquareGlobal):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "WWW2019"
        return super(FoursquareGlobal2, FoursquareGlobal2).load_from_file(source_path, user_column_name,
                                                                          item_column_name, rating_column_name,
                                                                          timestamp_column_name, version=version)
