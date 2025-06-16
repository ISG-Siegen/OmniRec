from .movielens_large import MovieLensLarge


class MovieLens25M(MovieLensLarge):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "25m"
        return super(MovieLens25M, MovieLens25M).load_from_file(source_path, user_column_name, item_column_name,
                                                                rating_column_name, timestamp_column_name,
                                                                version=version)
