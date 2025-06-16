from .beer import Beer


class BeerAdvocate(Beer):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "beeradvocate"
        return super(BeerAdvocate, BeerAdvocate).load_from_file(source_path, user_column_name, item_column_name,
                                                                rating_column_name, timestamp_column_name,
                                                                version=version)
