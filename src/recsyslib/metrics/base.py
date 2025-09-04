from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd

# TODO: Docs


@dataclass
class MetricResult:
    name: str
    result: float | dict[int, float]


class Metric(ABC):
    # FIXME: Return type
    @abstractmethod
    def calculate(
        self, predictions: pd.DataFrame, test: pd.DataFrame
    ) -> MetricResult: ...
