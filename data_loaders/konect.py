import tarfile
import pandas as pd

from .loader import Loader


class Konect(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with tarfile.open(f"{source_path}/download.tsv.{additional_parameters['version']}.tar.bz2", 'r:bz2') as tar:
            names = [user_column_name, item_column_name, rating_column_name]
            if additional_parameters['has_timestamp']:
                names.append(timestamp_column_name)
            data = pd.read_csv(
                tar.extractfile(f"{additional_parameters['version']}/out.{additional_parameters['version']}"), header=0,
                delim_whitespace=True, names=names, low_memory=False)
            if data.iloc[0, :][user_column_name] == "%":
                data = data.iloc[1:, :]
            if data[rating_column_name].unique().size == 1:
                data.drop(columns=[rating_column_name], inplace=True)
            return data
