from .movielens_small import MovieLensSmall


class MovieLens10M(MovieLensSmall):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "10m"
        return super(MovieLens10M, MovieLens10M).load_from_file(source_path, user_column_name, item_column_name,
                                                                rating_column_name, timestamp_column_name,
                                                                version=version)
