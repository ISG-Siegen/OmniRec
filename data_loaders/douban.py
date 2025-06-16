import numpy as np
import pandas as pd

from .loader import Loader


class Douban(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        data = pd.read_csv(f"{source_path}/douban_{additional_parameters['version']}.tsv", header=0, sep='\t')
        data.rename(columns={'UserId': user_column_name, 'ItemId': item_column_name, 'Rating': rating_column_name,
                             'Timestamp': timestamp_column_name}, inplace=True)
        data.loc[data[rating_column_name] == -1, rating_column_name] = np.nan
        return data
