from .foursquare_global import FoursquareGlobal


class FoursquareGlobal1(FoursquareGlobal):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "TIST2015"
        return super(FoursquareGlobal1, FoursquareGlobal1).load_from_file(source_path, user_column_name,
                                                                          item_column_name, rating_column_name,
                                                                          timestamp_column_name, version=version)
