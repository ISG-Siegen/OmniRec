import json
from pathlib import Path
from os import path

import numpy as np
import pandas as pd
import tensorflow as tf

from algorithm_config import retrieve_configurations
import time
import yaml

from run_utils import ndcg, hr, recall, rmse, mae

import importlib

import elliot.hyperoptimization as ho
from elliot.namespace.namespace_model_builder import NameSpaceBuilder
from elliot.utils import logging as logging_project
from elliot.dataset.dataset import DataSetLoader

here = path.abspath(path.dirname(__file__))


def elliot_config(data_set_name, algorithm_name, current_configuration):
    has_configuration = True
    model_name = algorithm_name
    if algorithm_name[-2:] == "EL":
        model_name = model_name[:-2]

    if algorithm_name in ["SlopeOne", "MostPop"]:
        has_configuration = False

    model = {
        model_name: {
            "meta": {
                "hyper_max_evals": 1,
                "save_recs": False
            },
            "early_stopping": {
                "patience": 5,
                "monitor": "nDCG@10",
                "verbose": True,
                "rel_delta": 0.05
            }
        }
    }
    if has_configuration:
        model[model_name].update(current_configuration)

    config_dict = {
        "experiment": {
            "dataset": f"{data_set_name}",
            "data_config": {
                "strategy": "fixed",
                "train_path": f"./data_sets/{data_set_name}/atomic/{data_set_name}.train_split_fold_0.tsv",
                "valid_path": f"./data_sets/{data_set_name}/atomic/{data_set_name}.valid_split_fold_0.tsv",
                "test_path": f"./data_sets/{data_set_name}/atomic/{data_set_name}.test_split_fold_0.tsv"
            },
            "gpu": 1,
            "models": model,
            "evaluation": {
                "simple_metrics": ["nDCG"],
                "cutoffs": [10]
            },
            "top_k": 20
        }
    }

    config_path = Path(f'./elliot_{data_set_name}_{algorithm_name}.yaml')

    if not config_path.exists():
        with open(config_path, 'w') as file:
            yaml.dump(config_dict, file, sort_keys=False, default_flow_style=False)

    return config_path


def elliot_fit(data_set_name, algorithm_name, algorithm_config, fold, **kwargs):
    setup_start_time = time.time()

    configurations = retrieve_configurations(algorithm_name=algorithm_name)
    current_configuration = configurations[algorithm_config]

    config_path = elliot_config(data_set_name, algorithm_name, current_configuration)

    builder = NameSpaceBuilder(config_path, here, path.abspath(path.dirname(config_path)))
    base = builder.base
    logging_project.init("./logger_config.yml", base.base_namespace.path_log_folder)
    logger = logging_project.get_logger("__main__")

    logger.info("Start experiment")
    base.base_namespace.evaluation.relevance_threshold = getattr(base.base_namespace.evaluation,
                                                                 "relevance_threshold", 0)
    dataloader = DataSetLoader(config=base.base_namespace)

    data_test_list = dataloader.generate_dataobjects()
    key, model_base = list(builder.models())[0]
    data_test = data_test_list[0]

    logging_project.prepare_logger(key, base.base_namespace.path_log_folder)

    model_class = getattr(importlib.import_module("elliot.recommender"), key)
    model_placeholder = ho.ModelCoordinator(data_test, base.base_namespace, model_base, model_class, 0)

    logger.info(f"Training begun for {model_class.__name__}\\n")
    model = model_placeholder.model_class(data=model_placeholder.data_objs[0], config=model_placeholder.base,
                                          params=model_placeholder.params)

    # model.evaluate = lambda *args, **kwargs: None
    setup_end_time = time.time()
    fit_start_time = time.time()
    model.train()
    fit_end_time = time.time()

    target_path = f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/config_{algorithm_config}/fold_{fold}/"
    Path(target_path).mkdir(parents=True, exist_ok=True)
    current_time = time.time()
    model_file = f"{target_path}{algorithm_name}-{current_time}"

    if hasattr(model, "_model"):
        if isinstance(model._model, tf.keras.Model):
            checkpoint = tf.train.Checkpoint(model=model._model)
            model_file = f'{model_file}.ckpt'
            checkpoint.write(model_file)
        else:
            model_file = f'{model_file}.pkl'
            model._model.save_weights(model_file)
    else:
        model_file = f"{model_file}.dat"
        with open(f"{model_file}.dat", "wb") as file:
            pass

    fit_log_dict = {
        "model_file": model_file,
        "data_set_name": data_set_name,
        "algorithm_name": algorithm_name,
        "algorithm_config_index": algorithm_config,
        "algorithm_configuration": configurations[algorithm_config],
        "fold": fold,
        "setup_time": setup_end_time - setup_start_time,
        "training_time": fit_end_time - fit_start_time
    }

    with open(f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
              f"config_{algorithm_config}/fold_{fold}/fit_log.json", mode="w") as file:
        json.dump(fit_log_dict, file, indent=4)


def elliot_predict(data_set_name, algorithm_name, algorithm_config, fold, **kwargs):
    configurations = retrieve_configurations(algorithm_name=algorithm_name)
    current_configuration = configurations[algorithm_config]

    config_path = elliot_config(data_set_name, algorithm_name, current_configuration)

    builder = NameSpaceBuilder(config_path, here, path.abspath(path.dirname(config_path)))
    base = builder.base
    logging_project.init("./logger_config.yml", base.base_namespace.path_log_folder)
    logger = logging_project.get_logger("__main__")

    logger.info("Start experiment")
    base.base_namespace.evaluation.relevance_threshold = getattr(base.base_namespace.evaluation, "relevance_threshold",
                                                                 0)
    dataloader = DataSetLoader(config=base.base_namespace)

    data_test_list = dataloader.generate_dataobjects()
    key, model_base = list(builder.models())[0]
    data_test = data_test_list[0]

    logging_project.prepare_logger(key, base.base_namespace.path_log_folder)

    model_class = getattr(importlib.import_module("elliot.recommender"), key)
    model_placeholder = ho.ModelCoordinator(data_test, base.base_namespace, model_base, model_class, 0)

    logger.info(f"Training begun for {model_class.__name__}\\n")
    model = model_placeholder.model_class(data=model_placeholder.data_objs[0], config=model_placeholder.base,
                                          params=model_placeholder.params)

    fit_log_file = (f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
                    f"config_{algorithm_config}/fold_{fold}/fit_log.json")
    with open(fit_log_file, "r") as file:
        fit_log = json.load(file)
    model_file = fit_log["model_file"]

    if hasattr(model, "_model"):
        if isinstance(model._model, tf.keras.Model):
            checkpoint = tf.train.Checkpoint(model=model._model)
            checkpoint.restore(model_file).expect_partial()
        else:
            model._model.load_weights(model_file)

    start_prediction = time.time()
    recs = model.get_recommendations(model.evaluator.get_needed_recommendations())
    end_prediction = time.time()

    recs = {int(key): [[int(t[0]) for t in value], [float(t[1]) for t in value]] for key, value in recs[0].items()}

    with open(f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
              f"config_{algorithm_config}/fold_{fold}/predictions.json", "w") as file:
        json.dump(recs, file, indent=4)

    train = pd.read_csv(
        f"./data_sets/{data_set_name}/atomic/{data_set_name}.train_split_fold_{fold}.inter",
        header=0, sep=",")
    test = pd.read_csv(
        f"./data_sets/{data_set_name}/atomic/{data_set_name}.test_split_fold_{fold}.inter",
        header=0, sep=",")

    unique_train_users = train["user_id:token"].unique()
    unique_test_users = test["user_id:token"].unique()
    users_to_predict = np.intersect1d(unique_test_users, unique_train_users)

    predict_log_dict = {
        "model_file": model_file,
        "data_set_name": data_set_name,
        "algorithm_name": algorithm_name,
        "algorithm_config_index": algorithm_config,
        "algorithm_configuration": configurations[algorithm_config],
        "fold": fold,
        "train_users": len(unique_train_users),
        "test_users": len(unique_test_users),
        "users_to_predict": len(users_to_predict),
        "prediction_time": end_prediction - start_prediction
    }

    with open(f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
              f"config_{algorithm_config}/fold_{fold}/predict_log.json", "w") as file:
        json.dump(predict_log_dict, file, indent=4)


def elliot_evaluate(data_set_name, algorithm_name, algorithm_config, fold, **kwargs):
    configurations = retrieve_configurations(algorithm_name=algorithm_name)

    config_path = Path(f'./elliot_{data_set_name}_{algorithm_name}.yaml')
    if config_path.exists():
        config_path.unlink()

    predict_log_file = (f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
                        f"config_{algorithm_config}/fold_{fold}/predict_log.json")
    with open(predict_log_file, "r") as file:
        predict_log = json.load(file)
    model_file = predict_log["model_file"]

    test = pd.read_csv(
        f"./data_sets/{data_set_name}/atomic/{data_set_name}.test_split_fold_{fold}.inter",
        header=0, sep=",")

    evaluate_log_dict = {
        "model_file": model_file,
        "data_set_name": data_set_name,
        "algorithm_name": algorithm_name,
        "algorithm_config_index": algorithm_config,
        "algorithm_configuration": configurations[algorithm_config],
        "fold": fold
    }

    if "rating" not in test.columns:

        with open(f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
                  f"config_{algorithm_config}/fold_{fold}/predictions.json", "r") as file:
            top_k_dict = json.load(file)

        top_k_dict = {int(k): v[0] for k, v in top_k_dict.items()}
        k_options = [1, 3, 5, 10, 20]

        start_evaluation = time.time()
        ndcg_per_user_per_k = ndcg(top_k_dict, k_options, test, "user_id:token", "item_id:token")
        hr_per_user_per_k = hr(top_k_dict, k_options, test, "user_id:token", "item_id:token")
        recall_per_user_per_k = recall(top_k_dict, k_options, test, "user_id:token", "item_id:token")
        end_evaluation = time.time()

        evaluate_log_dict["evaluation_time"] = end_evaluation - start_evaluation

        for k in k_options:
            score = sum(ndcg_per_user_per_k[k]) / len(ndcg_per_user_per_k[k])
            print(f"NDCG@{k}: {score}")
            evaluate_log_dict[f"NDCG@{k}"] = score
            score = sum(hr_per_user_per_k[k]) / len(hr_per_user_per_k[k])
            print(f"HR@{k}: {score}")
            evaluate_log_dict[f"HR@{k}"] = score
            score = sum(recall_per_user_per_k[k]) / len(recall_per_user_per_k[k])
            print(f"Recall@{k}: {score}")
            evaluate_log_dict[f"Recall@{k}"] = score
    else:
        predictions = pd.read_csv(f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
                                  f"config_{algorithm_config}/fold_{fold}/predictions.csv")

        start_evaluation = time.time()
        rmse_score = rmse(predictions["prediction"], test["rating"])
        mae_score = mae(predictions["prediction"], test["rating"])
        end_evaluation = time.time()

        evaluate_log_dict["evaluation_time"] = end_evaluation - start_evaluation
        print(f"RMSE: {rmse_score}")
        evaluate_log_dict["RMSE"] = rmse_score
        print(f"MAE: {mae_score}")
        evaluate_log_dict["MAE"] = mae_score

    with open(f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
              f"config_{algorithm_config}/fold_{fold}/evaluate_log.json", 'w') as file:
        json.dump(evaluate_log_dict, file, indent=4)
