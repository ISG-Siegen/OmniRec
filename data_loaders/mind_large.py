from .mind import MIND


class MINDLarge(MIND):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "large"
        return super(MINDLarge, MINDLarge).load_from_file(source_path, user_column_name, item_column_name,
                                                          rating_column_name, timestamp_column_name, version=version)
