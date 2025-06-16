import json
from pathlib import Path

import numpy as np
import pandas as pd
from lenskit.algorithms import Recommender
from lenskit.algorithms.basic import PopScore, Fallback, Bias
from lenskit.algorithms.item_knn import ItemItem
from lenskit.algorithms.user_knn import UserUser
from lenskit.algorithms.als import ImplicitMF, BiasedMF
from lenskit.algorithms.funksvd import FunkSVD

from algorithm_config import retrieve_configurations
import binpickle
import time

from run_utils import ndcg, hr, recall, rmse, mae


def lenskit_load_transform(data_set_name, fold, partition):
    if partition == "train":
        data = pd.read_csv(f"./data_sets/{data_set_name}/atomic/{data_set_name}.train_split_fold_{fold}.inter",
                           header=0, sep=",")
    elif partition == "valid":
        data = pd.read_csv(f"./data_sets/{data_set_name}/atomic/{data_set_name}.valid_split_fold_{fold}.inter",
                           header=0, sep=",")
    elif partition == "test":
        data = pd.read_csv(f"./data_sets/{data_set_name}/atomic/{data_set_name}.test_split_fold_{fold}.inter",
                           header=0, sep=",")
    else:
        print(f"Partition {partition} not found.")
        return

    data.rename(columns={'user_id:token': 'user', 'item_id:token': 'item', 'rating:float': 'rating'}, inplace=True)
    return data


def lenskit_fit(data_set_name, algorithm_name, algorithm_config, fold, **kwargs):
    setup_start_time = time.time()

    train = lenskit_load_transform(data_set_name, fold, "train")

    configurations = retrieve_configurations(algorithm_name=algorithm_name)
    current_configuration = configurations[algorithm_config]

    if algorithm_name == "PopScore":
        model = Recommender.adapt(PopScore(**current_configuration))
    elif algorithm_name == "ItemItem":
        if "rating" in train.columns:
            model = Recommender.adapt(Fallback(ItemItem(**current_configuration, feedback="explicit"), Bias()))
        else:
            model = Recommender.adapt(ItemItem(**current_configuration, feedback="implicit"))
    elif algorithm_name == "UserUser":
        if "rating" in train.columns:
            model = Recommender.adapt(Fallback(UserUser(**current_configuration, feedback="explicit"), Bias()))
        else:
            model = Recommender.adapt(UserUser(**current_configuration, feedback="implicit"))
    elif algorithm_name == "ImplicitMF":
        model = Recommender.adapt(ImplicitMF(**current_configuration, rng_spec=42))
    elif algorithm_name == "BiasedMF":
        model = Recommender.adapt(Fallback(BiasedMF(**current_configuration, rng_spec=42), Bias()))
    elif algorithm_name == "FunkSVD":
        model = Recommender.adapt(Fallback(FunkSVD(**current_configuration, random_state=42), Bias()))
    else:
        print(f"Algorithm {algorithm_name} not found.")
        return

    setup_end_time = time.time()

    fit_start_time = time.time()
    model.fit(train)
    fit_end_time = time.time()

    target_path = f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/config_{algorithm_config}/fold_{fold}/"
    Path(target_path).mkdir(parents=True, exist_ok=True)
    current_time = time.time()
    model_file = f"{target_path}{algorithm_name}-{current_time}.bpk"
    binpickle.dump(model, model_file)

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


def lenskit_predict(data_set_name, algorithm_name, algorithm_config, fold, **kwargs):
    configurations = retrieve_configurations(algorithm_name=algorithm_name)

    fit_log_file = (f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
                    f"config_{algorithm_config}/fold_{fold}/fit_log.json")
    with open(fit_log_file, "r") as file:
        fit_log = json.load(file)
    model_file = fit_log["model_file"]

    model = binpickle.load(model_file)

    train = lenskit_load_transform(data_set_name, fold, "train")
    test = lenskit_load_transform(data_set_name, fold, "test")

    predict_log_dict = {
        "model_file": model_file,
        "data_set_name": data_set_name,
        "algorithm_name": algorithm_name,
        "algorithm_config_index": algorithm_config,
        "algorithm_configuration": configurations[algorithm_config],
        "fold": fold
    }

    if "rating" not in train.columns:
        unique_train_users = train["user"].unique()
        unique_test_users = test["user"].unique()
        users_to_predict = np.intersect1d(unique_test_users, unique_train_users)

        top_k_dict = {}
        start_prediction = time.time()
        for user in users_to_predict:
            predictions = model.recommend(user, n=20)
            top_k_dict[int(user)] = [predictions["item"].tolist(), predictions["score"].tolist()]
        end_prediction = time.time()

        with open(f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
                  f"config_{algorithm_config}/fold_{fold}/predictions.json", "w") as file:
            json.dump(top_k_dict, file, indent=4)

        predict_log_dict.update({
            "train_users": len(unique_train_users),
            "test_users": len(unique_test_users),
            "users_to_predict": len(users_to_predict),
            "prediction_time": end_prediction - start_prediction
        })
    else:
        test_interactions = len(test)
        start_prediction = time.time()
        predictions = model.predict(test.drop(columns="rating"))
        end_prediction = time.time()

        predictions.to_csv(f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
                           f"config_{algorithm_config}/fold_{fold}/predictions.csv", index=False)

        predict_log_dict.update({
            "test_interactions": test_interactions,
            "prediction_time": end_prediction - start_prediction
        })

    with open(f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
              f"config_{algorithm_config}/fold_{fold}/predict_log.json", "w") as file:
        json.dump(predict_log_dict, file, indent=4)


def lenskit_evaluate(data_set_name, algorithm_name, algorithm_config, fold, **kwargs):
    configurations = retrieve_configurations(algorithm_name=algorithm_name)

    predict_log_file = (f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
                        f"config_{algorithm_config}/fold_{fold}/predict_log.json")
    with open(predict_log_file, "r") as file:
        predict_log = json.load(file)
    model_file = predict_log["model_file"]

    test = lenskit_load_transform(data_set_name, fold, "test")

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
        ndcg_per_user_per_k = ndcg(top_k_dict, k_options, test, "user", "item")
        hr_per_user_per_k = hr(top_k_dict, k_options, test, "user", "item")
        recall_per_user_per_k = recall(top_k_dict, k_options, test, "user", "item")
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
