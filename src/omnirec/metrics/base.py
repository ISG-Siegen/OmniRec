from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd



@dataclass
class MetricResult:
    """Represents the result of a metric calculation. It holds the name as str and either a single float result or a dictionary of results for multiple k values.
    """
    name: str
    result: float | dict[int, float]


class Metric(ABC):
    # FIXME: Return type
    @abstractmethod
    def calculate(
        self, predictions: pd.DataFrame, test: pd.DataFrame
    ) -> MetricResult: ...
