import argparse

from recsys_data_set import RecSysDataSet

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Convert raw to processed")
    parser.add_argument('--data_set_name', dest='data_set_name', type=str, required=True)
    parser.add_argument('--drop_duplicates', dest='drop_duplicates', type=bool, default=True)
    parser.add_argument('--normalize_identifiers', dest='normalize_identifiers', type=bool, default=True)

    args = parser.parse_args()

    data_set = RecSysDataSet(args.data_set_name)
    data_set.data_origin = "raw"
    data_set.log_function_time(data_set.process_data, force_process=False, drop_duplicates=args.drop_duplicates,
                               normalize_identifiers=args.normalize_identifiers)
    data_set.log_function_time(data_set.write_data, force_write=False)
    data_set.log_function_time(data_set.calculate_metadata, force_calculate=False)
    data_set.log_function_time(data_set.write_metadata, force_write=False)
    data_set.release_log(data_set.processed_data_log_path)
