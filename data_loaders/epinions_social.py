import tarfile
import pandas as pd

from .loader import Loader


class EpinionsSocial(Loader):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        with tarfile.open(f"{source_path}/epinions_data.tar.gz", "r:gz") as tar:
            file = tar.extractfile("epinions_data/epinions.txt")
            final_dict = {user_column_name: [], item_column_name: [], rating_column_name: [], timestamp_column_name: []}
            lines = file.readlines()[1:]
            skip_line = -1
            for line_idx, line in enumerate(lines):
                line_data = line.decode("utf-8", "replace").split(" ")
                if line_idx == skip_line:
                    continue
                if len(line_data) < 5:
                    next_line_data = lines[line_idx + 1].decode("utf-8", "replace").split(" ")
                    next_line_data = next_line_data[1:]
                    line_data += next_line_data
                    skip_line = line_idx + 1
                final_dict[user_column_name].append(line_data[1])
                final_dict[item_column_name].append(line_data[0])
                final_dict[rating_column_name].append(line_data[4].strip("\n"))
                final_dict[timestamp_column_name].append(line_data[3])

            data = pd.DataFrame.from_dict(final_dict)
            data = data.astype({rating_column_name: "float64"})

            return data
