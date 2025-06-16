from .mind import MIND


class MINDSmall(MIND):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "small"
        return super(MINDSmall, MINDSmall).load_from_file(source_path, user_column_name, item_column_name,
                                                          rating_column_name, timestamp_column_name, version=version)
