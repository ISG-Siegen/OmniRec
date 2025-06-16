from pathlib import Path

import pandas as pd


def write_results():
    results = []

    base_folder = Path("./data_sets/")
    for data_set_folder in base_folder.iterdir():
        if data_set_folder.is_dir():
            data_set_name = data_set_folder.name
            print(f"Data set: {data_set_name}")
            for checkpoint_folder in data_set_folder.iterdir():
                if "checkpoint" in checkpoint_folder.name:
                    model_name = checkpoint_folder.name.split("_")[1]
                    print(f"Model: {model_name}")
                    for config_folder in checkpoint_folder.iterdir():
                        if "config" in config_folder.name:
                            config_index = int(config_folder.name.split("_")[1])
                            print(f"Config: {config_index}")
                            for fold_folder in config_folder.iterdir():
                                if "fold" in fold_folder.name:
                                    fold_index = fold_folder.name.split("_")[1]
                                    print(f"Fold: {fold_index}")
                                    fit_log_file = fold_folder / "fit_log.json"
                                    predict_log_file = fold_folder / "predict_log.json"
                                    evaluate_log_file = fold_folder / "evaluate_log.json"

                                    def log_exists(log_file, type_file):
                                        if log_file.exists():
                                            print(f"{type_file} log exists for {data_set_name} {model_name} "
                                                  f"{config_index} {fold_index}")
                                            return True
                                        else:
                                            print(f"{type_file} log missing for {data_set_name} {model_name} "
                                                  f"{config_index} {fold_index}")
                                            return False

                                    fit_log_exists = log_exists(fit_log_file, "Fit")
                                    predict_log_exists = log_exists(predict_log_file, "Predict")
                                    evaluate_log_exists = log_exists(evaluate_log_file, "Evaluate")

                                    results.append({"data_set_name": data_set_name, "model": model_name,
                                                    "config": config_index, "fold": fold_index, "fit": fit_log_exists,
                                                    "predict": predict_log_exists, "evaluate": evaluate_log_exists})

    results_df = pd.DataFrame(results)
    results_df.to_csv("results.csv")


if __name__ == "__main__":
    write_results()
