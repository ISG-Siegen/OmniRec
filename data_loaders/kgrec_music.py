from .kgrec import KGRec


class KGRecMusic(KGRec):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "music/implicit_lf_dataset.csv"
        return super(KGRecMusic, KGRecMusic).load_from_file(source_path, user_column_name, item_column_name,
                                                            rating_column_name, timestamp_column_name, version=version)
