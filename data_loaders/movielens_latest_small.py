from .movielens_large import MovieLensLarge


class MovieLensLatestSmall(MovieLensLarge):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "latest-small"
        return super(MovieLensLatestSmall, MovieLensLatestSmall).load_from_file(source_path, user_column_name,
                                                                                item_column_name,
                                                                                rating_column_name,
                                                                                timestamp_column_name,
                                                                                version=version)
