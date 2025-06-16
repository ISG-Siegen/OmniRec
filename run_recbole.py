import json
import time
from logging import getLogger

import numpy as np
import pandas as pd
from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from recbole.quick_start import load_data_and_model
from recbole.utils import ModelType, get_model, get_trainer, init_seed, init_logger
from run_utils import ndcg, hr, recall

from algorithm_config import retrieve_configurations
from recbole.utils.case_study import full_sort_topk


def recbole_fit(data_set_name, algorithm_name, algorithm_config, fold, **kwargs):
    setup_start_time = time.time()

    config_dict = {
        "seed": 42,  # default: "2020"
        "data_path": "./data_sets/",  # default: "dataset/"
        "checkpoint_dir": f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
                          f"config_{algorithm_config}/fold_{fold}/",  # default: "saved/"
        "benchmark_filename": [f"train_split_fold_{fold}", f"valid_split_fold_{fold}",
                               f"test_split_fold_{fold}"],
        # default: None
        "field_separator": ",",  # default: "\t"
        "epochs": 200,  # default: 300
        "train_batch_size": 1024,  # default: 2048
        "learner": "adam",  # default: "adam"
        "learning_rate": 0.01,  # default: 0.001
        "training_neg_sample_args":
            {
                "distribution": "uniform",  # default: "uniform"
                "sample_num": 1,  # default: 1
                "dynamic": False,  # default: False
                "candidate_num": 0,  # default: 0
            },
        "eval_step": 5,  # default: 1
        "stopping_step": 5,  # default: 10
        "weight_decay": 0.0,  # default: 0.0
        "eval_args":
            {
                "group_by": "user",  # default: "user"
                "order": "RO",  # default: "RO"
                "split":
                    {
                        # "RS": [8, 1, 1] # default: {"RS": [8, 1, 1]}
                        "LS": "valid_and_test"
                    },
                "mode":
                    {
                        "valid": "full",  # default: "full"
                        "test": "full",  # default: "full"
                    },
            },
        "metrics": ["NDCG"],  # default: ["Recall", "MRR", "NDCG", "Hit", "Precision"]
        "topk": [10],  # default: 10
        "valid_metric": "NDCG@10",  # default: "MRR@10"
        "eval_batch_size": 32768,  # default: 4096
        # misc settings
        "model": algorithm_name,
        "MODEL_TYPE": ModelType.GENERAL,  # default: ModelType.GENERAL
        "dataset": data_set_name,  # default: None
    }

    configurations = retrieve_configurations(algorithm_name=algorithm_name)
    config_dict.update(configurations[algorithm_config])

    config = Config(config_dict=config_dict)
    init_seed(config['seed'], config['reproducibility'])
    init_logger(config)
    logger = getLogger()
    logger.info(config)
    logger.info(f"Running algorithm {algorithm_name} configuration: {configurations[algorithm_config]}.")

    config["data_path"] = f"./data_sets/{data_set_name}/atomic/"
    dataset = create_dataset(config)
    logger.info(dataset)
    train_data, valid_data, test_data = data_preparation(config, dataset)

    logger.info("Loading model.")
    model = get_model(config["model"])(config, train_data.dataset).to(config['device'])
    logger.info(model)
    logger.info("Loading trainer.")
    trainer = get_trainer(config["MODEL_TYPE"], config["model"])(config, model)

    setup_end_time = time.time()
    logger.info(f"Setup time: {setup_end_time - setup_start_time} seconds.")
    fit_start_time = time.time()
    try:
        trainer.fit(train_data, valid_data)
    except ValueError:
        print("ValueError occurred.")
        pass

    fit_end_time = time.time()
    logger.info(f"Training time: {fit_end_time - fit_start_time} seconds")
    model_file = trainer.saved_model_file

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


def recbole_predict(data_set_name, algorithm_name, algorithm_config, fold, **kwargs):
    configurations = retrieve_configurations(algorithm_name=algorithm_name)

    fit_log_file = (f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
                    f"config_{algorithm_config}/fold_{fold}/fit_log.json")
    with open(fit_log_file, "r") as file:
        fit_log = json.load(file)
    model_file = fit_log["model_file"]

    config, model, dataset, train_data, valid_data, test_data = load_data_and_model(model_file=model_file)

    train = pd.read_csv(
        f"./data_sets/{data_set_name}/atomic/{data_set_name}.train_split_fold_{fold}.inter",
        header=0, sep=",")
    test = pd.read_csv(
        f"./data_sets/{data_set_name}/atomic/{data_set_name}.test_split_fold_{fold}.inter",
        header=0, sep=",")

    unique_train_users = train["user_id:token"].unique()
    unique_test_users = test["user_id:token"].unique()
    users_to_predict = np.intersect1d(unique_test_users, unique_train_users)
    uid_series = dataset.token2id(dataset.uid_field, list(map(str, users_to_predict)))
    top_k_score = []
    top_k_iid_list = []
    start_prediction = time.time()
    for uid in uid_series:
        uid_top_k_score, uid_top_k_iid_list = full_sort_topk(np.array([uid]), model, test_data, k=20,
                                                             device=config['device'])
        top_k_score.append(uid_top_k_score.cpu().numpy().tolist()[0])
        top_k_iid_list.append(uid_top_k_iid_list.cpu().numpy().tolist()[0])
    end_prediction = time.time()
    top_k_dict = dict(zip(uid_series.tolist(), zip(top_k_iid_list, top_k_score)))

    with open(f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
              f"config_{algorithm_config}/fold_{fold}/predictions.json", "w") as file:
        json.dump(top_k_dict, file, indent=4)

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


def recbole_evaluate(data_set_name, algorithm_name, algorithm_config, fold, **kwargs):
    configurations = retrieve_configurations(algorithm_name=algorithm_name)

    predict_log_file = (f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
                        f"config_{algorithm_config}/fold_{fold}/predict_log.json")
    with open(predict_log_file, "r") as file:
        predict_log = json.load(file)
    model_file = predict_log["model_file"]

    config, model, dataset, train_data, valid_data, test_data = load_data_and_model(model_file=model_file)

    test = pd.read_csv(
        f"./data_sets/{data_set_name}/atomic/{data_set_name}.test_split_fold_{fold}.inter",
        header=0, sep=",")
    test["user_id:token"] = dataset.token2id(dataset.uid_field, list(map(str, test["user_id:token"].values)))
    test["item_id:token"] = dataset.token2id(dataset.iid_field, list(map(str, test["item_id:token"].values)))

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

    evaluate_log_dict = {
        "model_file": model_file,
        "data_set_name": data_set_name,
        "algorithm_name": algorithm_name,
        "algorithm_config_index": algorithm_config,
        "algorithm_configuration": configurations[algorithm_config],
        "fold": fold,
        "evaluation_time": end_evaluation - start_evaluation
    }

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

    with open(f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
              f"config_{algorithm_config}/fold_{fold}/evaluate_log.json", 'w') as file:
        json.dump(evaluate_log_dict, file, indent=4)
