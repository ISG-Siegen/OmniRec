from .kgrec import KGRec


class KGRecSound(KGRec):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "sound/downloads_fs_dataset.txt"
        return super(KGRecSound, KGRecSound).load_from_file(source_path, user_column_name, item_column_name,
                                                            rating_column_name, timestamp_column_name, version=version)
