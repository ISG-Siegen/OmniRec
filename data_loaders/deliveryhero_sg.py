from .deliveryhero import DeliveryHero


class DeliveryHeroSG(DeliveryHero):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "sg"
        return super(DeliveryHeroSG, DeliveryHeroSG).load_from_file(source_path, user_column_name, item_column_name,
                                                                    rating_column_name, timestamp_column_name,
                                                                    version=version)
