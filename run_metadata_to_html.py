import argparse
from pathlib import Path

import pandas as pd
import numpy as np

from recsys_data_set import RecSysDataSet

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Metadata to HTML")
    parser.add_argument('--data_origin', dest='data_origin', type=str, required=True)
    parser.add_argument('--pretty_table', dest='pretty_table', type=bool, required=False, default=False)

    args = parser.parse_args()

    meta_data_dfs = []
    for data_set_index, data_set_name in enumerate(RecSysDataSet.available_data_sets):
        data_set = RecSysDataSet(data_set_name)
        data_set.data_origin = args.data_origin
        data_set.load_metadata(force_load=True)
        meta_data_df = pd.DataFrame(data_set.meta_data, index=[data_set_index])
        meta_data_df.insert(0, "data_set_name", data_set_name)
        meta_data_dfs.append(meta_data_df)

    meta_data_table = pd.concat(meta_data_dfs)

    '''
    # remove data sets with less than 2000 interactions
    meta_data_table = meta_data_table[meta_data_table["num_interactions"] >= 2000]
    meta_data_table.sort_values(by="num_interactions", inplace=True)
    list_of_data_sets = np.array2string(meta_data_table["data_set_name"].values, separator=",", max_line_width=np.iinfo(np.int32).max)
    '''

    Path("./docs").mkdir(parents=True, exist_ok=True)

    if args.pretty_table:
        from pretty_html_table import build_table
        # create html with static table
        html_table = build_table(meta_data_table, 'blue_light')
        with open("./docs/data_statistics_static.html", 'w', newline='\n') as f:
            f.write(html_table)
    else:
        meta_data_table.to_html("./docs/data_statistics_static.html")

    # create html with interactive table
    table_html = meta_data_table.to_html()
    interactive_table = (f'<script src="https://code.jquery.com/jquery-3.7.1.min.js" '
                         f'integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=" '
                         f'crossorigin="anonymous"></script> '
                         f'<link rel="stylesheet" '
                         f'href="https://cdn.datatables.net/1.13.7/css/jquery.dataTables.css" /> '
                         f'<script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.js">'
                         f'</script>' +
                         table_html +
                         '<script> let table = new DataTable(".dataframe"); </script>')
    with open("./docs/data_statistics_interactive.html", 'w', newline='\n') as f:
        f.write(interactive_table)

    # create markdown with static table
    markdown_table = meta_data_table.to_markdown()
    with open("./docs/data_statistics_static.md", 'w', newline='\n') as f:
        f.write(markdown_table)
