import argparse

from recsys_data_set import RecSysDataSet

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Convert processed to atomic")
    parser.add_argument('--data_set_name', dest='data_set_name', type=str, required=True)
    parser.add_argument('--threshold', dest='threshold', type=float, required=False, default=0.0)
    parser.add_argument('--sample_size', dest='sample_size', type=int, required=False, default=10_000_000)
    parser.add_argument('--core', dest='core', type=int, required=False, default=5)
    parser.add_argument('--data_split_type', dest='data_split_type', type=str, required=False, default="user_cv")
    parser.add_argument('--num_folds', dest='num_folds', type=int, required=False, default=5)
    parser.add_argument('--valid_size', dest='valid_size', type=float, required=False, default=None)
    parser.add_argument('--test_size', dest='test_size', type=float, required=False, default=0.2)
    parser.add_argument('--random_state', dest='random_state', type=int, required=False, default=42)

    args = parser.parse_args()

    data_set = RecSysDataSet(args.data_set_name)
    data_set.data_origin = "processed"
    data_set.log_function_time(data_set.process_data, force_process=False)
    data_set.log_function_time(data_set.make_implicit, threshold=args.threshold)
    data_set.log_function_time(data_set.subsample, sample_size=args.sample_size, random_state=args.random_state)
    data_set.log_function_time(data_set.core_pruning, core=args.core)
    data_set.log_function_time(data_set.normalize_identifiers)
    data_set.log_function_time(data_set.write_data, force_write=False)
    data_set.data_split_type = args.data_split_type
    data_set.log_function_time(data_set.split_data, num_folds=args.num_folds, valid_size=args.valid_size,
                               test_size=args.test_size, random_state=args.random_state)
    data_set.log_function_time(data_set.write_data_splits, force_write=False)
    data_set.log_function_time(data_set.calculate_metadata, force_calculate=False)
    data_set.log_function_time(data_set.write_metadata, force_write=False)
    data_set.release_log(data_set.atomic_data_log_path)
