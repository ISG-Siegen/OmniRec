from .deliveryhero import DeliveryHero


class DeliveryHeroTW(DeliveryHero):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "tw"
        return super(DeliveryHeroTW, DeliveryHeroTW).load_from_file(source_path, user_column_name, item_column_name,
                                                                    rating_column_name, timestamp_column_name,
                                                                    version=version)
