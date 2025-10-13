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
        Convert predictions DataFrame with columns [user, item, score, rank]
        into {user: ([items sorted by rank], [scores])}.
        """
        topk: dict[int, tuple[list[int], list[float]]] = {}
        for user, group in predictions.sort_values("rank").groupby("user"):
            items = group["item"].to_list()
            scores = group["score"].to_list()
            topk[user] = (items, scores)
        return topk


class NDCG(RankingMetric):

    def __init__(self, k: int | list[int]) -> None:
        """Initializes the NDCG (Normalized Discounted Cumulative Gain) metric. k is the number of top predictions to consider.
        It can be a single integer or a list of integers, in which case the metric will be computed for each value of k.

        The NDCG considers the position of relevant items in a ranked list of predictions.

        For a user u, the discounted cumulative gain at cutoff k is

        $DCG@k(u) = \\sum_{i=1}^{k} \\frac{\\mathbf{1}\\{\\text{pred}_i \\in \\text{Rel}(u)\\}}{\\log_2(i+1)}$

        where $\\mathbf{1}\\{\\cdot\\}$ is the indicator function and
        
        $\\text{Rel}(u)$ is the set of relevant items for user u.

        The ideal discounted cumulative gain is

        $IDCG@k = \\sum_{i=1}^{k} \\frac{1}{\\log_2(i+1)}$

        The normalized score is

        $NDCG@k(u) = \\frac{DCG@k(u)}{IDCG@k}$

        Finally, the reported score is averaged over all users:

        $\\text{NDCG@k} = \\frac{1}{|U|} \\sum_{u \\in U} NDCG@k(u)$

        Args:
            k (int | list[int]): The number of top predictions to consider.
        """
        super().__init__(k)

    def calculate(self, predictions: DataFrame, test: DataFrame) -> MetricResult:
        """Computes the Normalized Discounted Cumulative Gain (NDCG). Considers the top-k predictions for one or multiple k values.

        Args:
            predictions (DataFrame): Contains the top k predictions for one or more users.
            test (DataFrame): Contains the ground truth relevant items for one or more users.

        Returns:
            MetricResult: The computed NDCG scores for each value k. If multiple users are provided, the scores are averaged.
        """
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
    
    def __init__(self, k: int | list[int]) -> None:
        """
        Computes the HR metric. k is the number of top recommendations to consider.
        It can be a single integer or a list of integers, in which case the metric will be computed for each value of k.

        It follows the formula:
        
        $HR@k = \\frac{1}{|U|} \\sum_{u \\in U} \\mathbf{1}\\{\\text{Rel}(u) \\cap \\text{Pred}_k(u) \\neq \\emptyset\\}$

        where $\\text{Pred}_k(u)$ is the set of top-k predicted items for user u.

        Args:
            k (int | list[int]): The number of top recommendations to consider.
        """
        super().__init__(k)

    def calculate(self, predictions: DataFrame, test: DataFrame) -> MetricResult:
        """Calculates the Hit Rate (HR) metric. Considers the top-k predictions for one or multiple k values.

        Args:
            predictions (DataFrame): Contains the top k predictions for one or more users.
            test (DataFrame): Contains the ground truth relevant items for one or more users.

        Returns:
            MetricResult: The computed HR scores for each value k. If multiple users are provided, the scores are averaged.
        """
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

    def __init__(self, k: int | list[int]) -> None:
        """Calculates the average recall at k for one or multiple k values. Recall at k is defined as the proportion of relevant items that are found in the top-k recommendations.
        
        It follows the formula:

        $Recall@k = \\frac{1}{|U|} \\sum_{u \\in U} \\frac{|\\text{Rel}(u) \\cap \\text{Pred}_k(u)|}{\\min(|\\text{Rel}(u)|, k)}$

        where $\\text{Pred}_k(u)$ is the set of top-k predicted items for user u.

        Args:
            k (int | list[int]): The number of top recommendations to consider.
        """
        super().__init__(k)

    def calculate(self, predictions: DataFrame, test: DataFrame) -> MetricResult:
        """Calculates the Recall metric. Considers the top-k predictions for one or multiple k values.

        Args:
            predictions (DataFrame): Contains the top k predictions for one or more users.
            test (DataFrame): Contains the ground truth relevant items for one or more users.

        Returns:
            list[float]: The computed Recall scores for each value k. If multiple users are provided, the scores are averaged.
        """
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
