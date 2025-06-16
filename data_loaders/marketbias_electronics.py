from .marketbias import MarketBias


class MarketBiasElectronics(MarketBias):
    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        version = "electronics"
        return super(MarketBiasElectronics, MarketBiasElectronics).load_from_file(source_path, user_column_name,
                                                                                  item_column_name, rating_column_name,
                                                                                  timestamp_column_name,
                                                                                  version=version)
