import numpy as np
from pandas import DataFrame

from omnirec.metrics.base import Metric, MetricResult


# TODO: Warn if dataset is not implicit
class RankingMetric(Metric):
    def __init__(self, k: int | list[int]) -> None:
        super().__init__()
        if isinstance(k, list):
            self._k_list = k
        else:
            self._k_list = [k]

    def make_topk_dict(
        self, predictions: DataFrame
    ) -> dict[int, tuple[list[int], list[float]]]:
        """
        Convert predictions DataFrame with columns [user, item, rating, rank]
        into {user: ([items sorted by rank], [scores])}.
        """
        topk = {}
        for user, group in predictions.sort_values("rank").groupby("user"):
            items = group["item"].to_list()
            scores = group["rating"].to_list()
            topk[user] = (items, scores)
        return topk


class NDCG(RankingMetric):
    # TODO: Docs, maybe add latex formula on how computed?
    def __init__(self, k: int | list[int]) -> None:
        super().__init__(k)

    def calculate(self, predictions: DataFrame, test: DataFrame) -> MetricResult:
        top_k_dict = self.make_topk_dict(predictions)

        discounted_gain_per_k = np.array(
            [1 / np.log2(i + 1) for i in range(1, max(self._k_list) + 1)]
        )
        ideal_discounted_gain_per_k = [
            discounted_gain_per_k[: ind + 1].sum()
            for ind in range(len(discounted_gain_per_k))
        ]
        ndcg_per_user_per_k: dict[int, list] = {}
        for user, (pred, _) in top_k_dict.items():
            positive_test_interactions = test["item"][test["user"] == user].to_numpy()
            hits = np.isin(pred[: max(self._k_list)], positive_test_interactions)
            user_dcg = np.where(hits, discounted_gain_per_k[: len(hits)], 0)
            for k in self._k_list:
                user_ndcg = user_dcg[:k].sum() / ideal_discounted_gain_per_k[k - 1]
                ndcg_per_user_per_k.setdefault(k, []).append(user_ndcg)

        scores: list[float] = [
            float(sum(v)) / len(v) for v in ndcg_per_user_per_k.values()
        ]
        scores_dict = {k: score for k, score in zip(self._k_list, scores)}
        return MetricResult(__class__.__name__, scores_dict)


class HR(RankingMetric):
    # TODO: Docs, maybe add latex formula on how computed?
    def __init__(self, k: int | list[int]) -> None:
        super().__init__(k)

    def calculate(self, predictions: DataFrame, test: DataFrame) -> MetricResult:
        top_k_dict = self.make_topk_dict(predictions)

        hr_per_user_per_k: dict[int, list] = {}
        # FIXME: Fix metric implementation, adapt to new data format
        for user, (pred, _) in top_k_dict.items():
            positive_test_interactions = test["item"][test["user"] == user].to_numpy()
            hits = np.isin(pred[: max(self._k_list)], positive_test_interactions)
            for k in self._k_list:
                user_hr = hits[:k].sum()
                user_hr = 1 if user_hr > 0 else 0
                hr_per_user_per_k.setdefault(k, []).append(user_hr)
        scores: list[float] = [sum(v) / len(v) for v in hr_per_user_per_k.values()]
        scores_dict = {k: score for k, score in zip(self._k_list, scores)}
        return MetricResult(__class__.__name__, scores_dict)


class Recall(RankingMetric):
    # TODO: Docs, maybe add latex formula on how computed?
    def __init__(self, k: int | list[int]) -> None:
        super().__init__(k)

    def calculate(self, predictions: DataFrame, test: DataFrame) -> MetricResult:
        top_k_dict = self.make_topk_dict(predictions)

        recall_per_user_per_k: dict[int, list] = {}
        for user, (pred, _) in top_k_dict.items():
            positive_test_interactions = test["item"][test["user"] == user].to_numpy()
            hits = np.isin(pred[: max(self._k_list)], positive_test_interactions)
            for k in self._k_list:
                user_recall = hits[:k].sum() / min(len(positive_test_interactions), k)
                recall_per_user_per_k.setdefault(k, []).append(user_recall)
        scores: list[float] = [
            float(sum(v)) / len(v) for v in recall_per_user_per_k.values()
        ]
        scores_dict = {k: score for k, score in zip(self._k_list, scores)}
        return MetricResult(__class__.__name__, scores_dict)
