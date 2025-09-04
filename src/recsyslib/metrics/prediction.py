import pandas as pd
from pandas import DataFrame
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

from recsyslib.metrics.base import Metric, MetricResult


class PredictionMetric(Metric):
    def __init__(self) -> None:
        super().__init__()

    def merge(self, predictions: DataFrame, test: DataFrame):
        return pd.merge(
            predictions, test, on=["user", "item"], suffixes=["_pred", "_test"]
        )


class RMSE(PredictionMetric):
    # TODO: Docs, maybe add latex formula on how computed?
    def __init__(self) -> None:
        super().__init__()

    def calculate(self, predictions: DataFrame, test: DataFrame) -> MetricResult:
        merged = self.merge(predictions, test)
        rmse = root_mean_squared_error(merged["rating_test"], merged["rating_pred"])
        return MetricResult(__class__.__name__, rmse)


class MAE(PredictionMetric):
    # TODO: Docs, maybe add latex formula on how computed?
    def __init__(self) -> None:
        super().__init__()

    def calculate(self, predictions: DataFrame, test: DataFrame) -> MetricResult:
        merged = self.merge(predictions, test)
        mae = mean_absolute_error(merged["rating_test"], merged["rating_pred"])
        return MetricResult(__class__.__name__, mae)
