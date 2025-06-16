from .konect import Konect


class WikiLens(Konect):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "wikilens-ratings"
        has_timestamp = True
        return super(WikiLens, WikiLens).load_from_file(source_path, user_column_name, item_column_name,
                                                        rating_column_name, timestamp_column_name, version=version,
                                                        has_timestamp=has_timestamp)
