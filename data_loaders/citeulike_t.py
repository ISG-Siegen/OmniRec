from .citeulike import CiteULike


class CiteULikeT(CiteULike):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "citeulike-t-master"
        return super(CiteULikeT, CiteULikeT).load_from_file(source_path, user_column_name, item_column_name,
                                                            rating_column_name, timestamp_column_name, version=version)
