import argparse

from available_algorithms import recbole_algorithm_names, lenskit_algorithm_names, recpack_algorithm_names, \
    elliot_algorithm_names

from run_utils import measure_and_log_function_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Execution Master")
    parser.add_argument('--mode', dest='mode', type=str, required=True)
    parser.add_argument('--data_set_name', dest='data_set_name', type=str, required=True)
    parser.add_argument('--algorithm_name', dest='algorithm_name', type=str, required=True)
    parser.add_argument('--algorithm_config', dest='algorithm_config', type=int, required=True)
    parser.add_argument('--fold', dest='fold', type=int, required=True)
    args = parser.parse_args()

    if args.algorithm_name in recbole_algorithm_names:
        if args.mode == "fit":
            from run_recbole import recbole_fit

            measure_and_log_function_time(recbole_fit, **vars(args))
        elif args.mode == "predict":
            from run_recbole import recbole_predict

            measure_and_log_function_time(recbole_predict, **vars(args))
        elif args.mode == "evaluate":
            from run_recbole import recbole_evaluate

            measure_and_log_function_time(recbole_evaluate, **vars(args))
        else:
            print(f"Mode {args.mode} not found.")
    elif args.algorithm_name in lenskit_algorithm_names:
        if args.mode == "fit":
            from run_lenskit import lenskit_fit

            measure_and_log_function_time(lenskit_fit, **vars(args))
        elif args.mode == "predict":
            from run_lenskit import lenskit_predict

            measure_and_log_function_time(lenskit_predict, **vars(args))
        elif args.mode == "evaluate":
            from run_lenskit import lenskit_evaluate

            measure_and_log_function_time(lenskit_evaluate, **vars(args))
        else:
            print(f"Mode {args.mode} not found.")
    elif args.algorithm_name in recpack_algorithm_names:
        if args.mode == "fit":
            from run_recpack import recpack_fit

            measure_and_log_function_time(recpack_fit, **vars(args))
        elif args.mode == "predict":
            from run_recpack import recpack_predict

            measure_and_log_function_time(recpack_predict, **vars(args))
        elif args.mode == "evaluate":
            from run_recpack import recpack_evaluate

            measure_and_log_function_time(recpack_evaluate, **vars(args))
        else:
            print(f"Mode {args.mode} not found.")
    elif args.algorithm_name in elliot_algorithm_names:
        if args.mode == "fit":
            from run_elliot import elliot_fit

            measure_and_log_function_time(elliot_fit, **vars(args))
        elif args.mode == "predict":
            from run_elliot import elliot_predict

            measure_and_log_function_time(elliot_predict, **vars(args))
        elif args.mode == "evaluate":
            from run_elliot import elliot_evaluate

            measure_and_log_function_time(elliot_evaluate, **vars(args))
        else:
            print(f"Mode {args.mode} not found.")
    else:
        print(f"Algorithm {args.algorithm_name} not found.")
