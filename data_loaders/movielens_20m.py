from .movielens_large import MovieLensLarge


class MovieLens20M(MovieLensLarge):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "20m"
        return super(MovieLens20M, MovieLens20M).load_from_file(source_path, user_column_name, item_column_name,
                                                                rating_column_name, timestamp_column_name,
                                                                version=version)
