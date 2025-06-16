from .douban import Douban


class DoubanMusic(Douban):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "music"
        return super(DoubanMusic, DoubanMusic).load_from_file(source_path, user_column_name, item_column_name,
                                                              rating_column_name, timestamp_column_name,
                                                              version=version)
