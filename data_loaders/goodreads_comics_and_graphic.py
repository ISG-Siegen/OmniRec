from .goodreads import Goodreads


class GoodreadsComicsAndGraphic(Goodreads):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "comics_graphic"
        return super(GoodreadsComicsAndGraphic, GoodreadsComicsAndGraphic).load_from_file(source_path, user_column_name,
                                                                                          item_column_name,
                                                                                          rating_column_name,
                                                                                          timestamp_column_name,
                                                                                          version=version)
