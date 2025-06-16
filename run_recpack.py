import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from recpack.algorithms import SVD, NMF, ItemKNN
from scipy.sparse import csr_matrix
import pickle as pkl

from algorithm_config import retrieve_configurations

from run_utils import ndcg, hr, recall


def recpack_load_transform(data_set_name, fold, csr_split):
    train = pd.read_csv(f"./data_sets/{data_set_name}/atomic/{data_set_name}.train_split_fold_{fold}.inter",
                        header=0, sep=",")
    valid = pd.read_csv(f"./data_sets/{data_set_name}/atomic/{data_set_name}.valid_split_fold_{fold}.inter",
                        header=0, sep=",")
    test = pd.read_csv(f"./data_sets/{data_set_name}/atomic/{data_set_name}.test_split_fold_{fold}.inter",
                       header=0, sep=",")

    data = pd.concat([train, valid, test])
    shape = (int(data['user_id:token'].max() + 1), int(data['item_id:token'].max() + 1))

    def transform_csr(data_in, shape_in):
        data_indices = data_in[['user_id:token', 'item_id:token']].values
        data_indices = data_indices[:, 0], data_indices[:, 1]

        data_out = csr_matrix((np.ones(data_in.shape[0]), data_indices), shape=shape_in, dtype=np.float32)
        return data_out

    if csr_split == 1:
        train_csr = transform_csr(train, shape)
        valid_csr = transform_csr(valid, shape)
        test_csr = transform_csr(test, shape)
    else:
        def split_in_chunks(data_in, shape_in, split_in):
            grouped = data_in.groupby('user_id:token')
            num_users = len(grouped)
            chunk_size = int(np.ceil(num_users / split_in))
            chunks = [group for _, group in grouped]
            chunked_data = [chunks[i:i + chunk_size] for i in range(0, num_users, chunk_size)]
            final_chunks = [pd.concat(sub_chunk) for sub_chunk in chunked_data]
            csr_chunks = [transform_csr(chunk, shape_in) for chunk in final_chunks]
            return csr_chunks
        train_csr = split_in_chunks(train, shape, csr_split)
        valid_csr = split_in_chunks(valid, shape, csr_split)
        test_csr = split_in_chunks(test, shape, csr_split)


    return train_csr, valid_csr, test_csr, train, valid, test


def recpack_fit(data_set_name, algorithm_name, algorithm_config, fold, **kwargs):
    setup_start_time = time.time()

    train, _, _, _, _, _ = recpack_load_transform(data_set_name, fold, 1)

    configurations = retrieve_configurations(algorithm_name=algorithm_name)
    current_configuration = configurations[algorithm_config]

    if algorithm_name == "SVD":
        model = SVD(**current_configuration, seed=42)
    elif algorithm_name == "NMF":
        model = NMF(**current_configuration, seed=42)
    elif algorithm_name == "ItemKNNRP":
        model = ItemKNN(**current_configuration)
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
    model_file = f"{target_path}{algorithm_name}-{current_time}.pkl"
    with open(model_file, "wb") as file:
        pkl.dump(model, file)

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


def recpack_predict(data_set_name, algorithm_name, algorithm_config, fold, **kwargs):
    configurations = retrieve_configurations(algorithm_name=algorithm_name)

    fit_log_file = (f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
                    f"config_{algorithm_config}/fold_{fold}/fit_log.json")
    with open(fit_log_file, "r") as file:
        fit_log = json.load(file)
    model_file = fit_log["model_file"]

    model = pkl.load(open(model_file, "rb"))

    train, _, _, train_orig, _, test_orig = recpack_load_transform(data_set_name, fold, 20)

    unique_train_users = train_orig["user_id:token"].unique()
    unique_test_users = test_orig["user_id:token"].unique()
    users_to_predict = np.intersect1d(unique_test_users, unique_train_users)

    top_k_dict = {}
    start_prediction = time.time()
    for chunk in train:
        predictions = model.predict(chunk)
        predictions = predictions - predictions.multiply(chunk.astype(bool).astype(chunk.dtype))

        row_ind, col_ind = predictions.nonzero()
        data = predictions.data
        df = pd.DataFrame({'Row': row_ind, 'Column': col_ind, 'Value': data})
        grouped = df.groupby('Row').agg({'Column': list, 'Value': list})

        inter_top_k_dict = grouped.to_dict(orient='index')
        for key, value in inter_top_k_dict.items():
            column_list = list(value['Column'])
            value_list = list(value['Value'])
            sorted_indices = sorted(range(len(value_list)), key=lambda k: value_list[k], reverse=True)
            sorted_columns = [column_list[i] for i in sorted_indices]
            sorted_values = [value_list[i] for i in sorted_indices]
            inter_top_k_dict[key] = (sorted_columns[:20], sorted_values[:20])
        inter_top_k_dict = {key: value for key, value in inter_top_k_dict.items() if key in users_to_predict}
        top_k_dict.update(inter_top_k_dict)

    end_prediction = time.time()

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


def recpack_evaluate(data_set_name, algorithm_name, algorithm_config, fold, **kwargs):
    configurations = retrieve_configurations(algorithm_name=algorithm_name)

    predict_log_file = (f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
                        f"config_{algorithm_config}/fold_{fold}/predict_log.json")
    with open(predict_log_file, "r") as file:
        predict_log = json.load(file)
    model_file = predict_log["model_file"]

    _, _, _, _, _, test = recpack_load_transform(data_set_name, fold, 1)

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
