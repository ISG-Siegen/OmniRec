import json
import time
from pathlib import Path
from sklearn.metrics import mean_squared_error, mean_absolute_error

import numpy as np


def ndcg(top_k_dict, k_options, test, user_column, item_column):
    discounted_gain_per_k = np.array([1 / np.log2(i + 1) for i in range(1, max(k_options) + 1)])
    ideal_discounted_gain_per_k = [discounted_gain_per_k[:ind + 1].sum() for ind, k in enumerate(discounted_gain_per_k)]
    ndcg_per_user_per_k = {}
    for k in k_options:
        ndcg_per_user_per_k[k] = []
    for user, predictions in top_k_dict.items():
        positive_test_interactions = test[item_column][test[user_column] == user].values
        hits = np.in1d(predictions[:max(k_options)], positive_test_interactions)
        user_dcg = np.where(hits, discounted_gain_per_k[:len(hits)], 0)
        for k in k_options:
            user_ndcg = user_dcg[:k].sum() / ideal_discounted_gain_per_k[k - 1]
            ndcg_per_user_per_k[k].append(user_ndcg)
    return ndcg_per_user_per_k


def hr(top_k_dict, k_options, test, user_column, item_column):
    hr_per_user_per_k = {}
    for k in k_options:
        hr_per_user_per_k[k] = []
    for user, predictions in top_k_dict.items():
        positive_test_interactions = test[item_column][test[user_column] == user].values
        hits = np.in1d(predictions[:max(k_options)], positive_test_interactions)
        for k in k_options:
            user_hr = hits[:k].sum()
            user_hr = 1 if user_hr > 0 else 0
            hr_per_user_per_k[k].append(user_hr)
    return hr_per_user_per_k


def recall(top_k_dict, k_options, test, user_column, item_column):
    recall_per_user_per_k = {}
    for k in k_options:
        recall_per_user_per_k[k] = []
    for user, predictions in top_k_dict.items():
        positive_test_interactions = test[item_column][test[user_column] == user].values
        hits = np.in1d(predictions[:max(k_options)], positive_test_interactions)
        for k in k_options:
            if user == 8:
                pass
            user_recall = hits[:k].sum() / min(len(positive_test_interactions), k)
            recall_per_user_per_k[k].append(user_recall)
    return recall_per_user_per_k


def rmse(predictions, test):
    return mean_squared_error(test, predictions, squared=False)


def mae(predictions, test):
    return mean_absolute_error(test, predictions)


def measure_and_log_function_time(func, **kwargs):
    time_before = time.time()
    result = func(**kwargs)
    time_after = time.time()

    Path(f"./energy").mkdir(parents=True, exist_ok=True)
    with open(f"./energy/{kwargs['data_set_name']}_{kwargs['algorithm_name']}_"
              f"{kwargs['algorithm_config']}_{kwargs['fold']}_{kwargs['mode']}.json", "w") as file:
        json.dump({"start": time_before, "end": time_after}, file, indent=4)

    return result
