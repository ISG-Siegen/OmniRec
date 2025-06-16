from .citeulike import CiteULike


class CiteULikeA(CiteULike):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "citeulike-a-master"
        return super(CiteULikeA, CiteULikeA).load_from_file(source_path, user_column_name, item_column_name,
                                                            rating_column_name, timestamp_column_name, version=version)
