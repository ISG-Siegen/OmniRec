import argparse

from recsys_data_set import RecSysDataSet

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Clear all processed data sets")
    parser.add_argument('--data_origin', dest='data_origin', type=str, required=True)
    parser.add_argument('--safety_flag', dest='safety_flag', type=bool, required=False, default=False)

    args = parser.parse_args()


    for data_set_name in RecSysDataSet.available_data_sets:
        data_set = RecSysDataSet(data_set_name)
        data_set.data_origin = args.data_origin
        data_set.clear_data(safety_flag=args.safety_flag)
