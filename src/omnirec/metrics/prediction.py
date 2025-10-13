import pandas as pd
from pandas import DataFrame
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

from omnirec.metrics.base import Metric, MetricResult


class PredictionMetric(Metric):
    def __init__(self) -> None:
        super().__init__()

    def merge(self, predictions: DataFrame, test: DataFrame):
        return pd.merge(
            predictions, test, on=["user", "item"], suffixes=["_pred", "_test"]
        )


class RMSE(PredictionMetric):
    def __init__(self) -> None:
        """Root Mean Squared Error (RMSE) metric. Calculates the square root of the average of the squared differences between predicted and actual ratings, according to the formula:

        $RMSE = \\sqrt{\\frac{1}{n} \\sum_{i=1}^{n} (y_i - \\hat{y}_i)^2}$
        """
        super().__init__()

    def calculate(self, predictions: DataFrame, test: DataFrame) -> MetricResult:
        """Calculate the RMSE metric.

        Args:
            predictions (DataFrame): _description_
            test (DataFrame): _description_

        Returns:
            MetricResult: Contains the name of the metric and the computed RMSE value.
        """
        merged = self.merge(predictions, test)
        rmse = root_mean_squared_error(merged["rating_test"], merged["rating_pred"])
        return MetricResult(__class__.__name__, rmse)


class MAE(PredictionMetric):
    def __init__(self) -> None:
        """Mean Absolute Error (MAE) metric. Calculates the average of the absolute differences between predicted and actual ratings, according to the formula:
        $MAE = \\frac{1}{n} \\sum_{i=1}^{n} |y_i - \\hat{y}_i|$
        """
        super().__init__()

    def calculate(self, predictions: DataFrame, test: DataFrame) -> MetricResult:
        """Calculates the MAE metric.

        Args:
            predictions (DataFrame): Contains the predicted ratings.
            test (DataFrame): Contains the ground truth ratings.

        Returns:
            MetricResult: Contains the name of the metric and the computed MAE value.
        """
        merged = self.merge(predictions, test)
        mae = mean_absolute_error(merged["rating_test"], merged["rating_pred"])
        return MetricResult(__class__.__name__, mae)
