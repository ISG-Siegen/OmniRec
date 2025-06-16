from .googlelocal2021 import GoogleLocal2021


class GoogleLocal2021DistrictOfColumbia(GoogleLocal2021):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        return super(GoogleLocal2021DistrictOfColumbia,
                     GoogleLocal2021DistrictOfColumbia).load_from_file(source_path, user_column_name, item_column_name,
                                                                       rating_column_name, timestamp_column_name)
