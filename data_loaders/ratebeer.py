from .beer import Beer


class RateBeer(Beer):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "ratebeer"
        return super(RateBeer, RateBeer).load_from_file(source_path, user_column_name, item_column_name,
                                                        rating_column_name, timestamp_column_name,
                                                        version=version)
