import zipfile

import pandas as pd

from .loader import Loader


class SpotifyPlaylists(Loader):
    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with zipfile.ZipFile(f"{source_path}/2594557.zip", 'r') as zipf_top:
            with zipfile.ZipFile(zipf_top.open(f"spotify_playlists.zip"), 'r') as zipf:
                return pd.read_csv(zipf.open("spotify_dataset.csv", 'r'), sep=",", header=0,
                                   usecols=[0, 2], names=[user_column_name, item_column_name])
