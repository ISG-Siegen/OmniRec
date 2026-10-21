from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd

from omnirec.util import util


@dataclass
class MetricResult:
    """Represents the result of a metric calculation. It holds the name as str and either a single float result or a dictionary of results for multiple k values."""

    name: str
    result: float | dict[int, float]


class Metric(ABC):
    def __init__(self):
        self.logger = util._root_logger.getChild("data")

    # FIXME: Return type
    @abstractmethod
    def calculate(
        self, predictions: pd.DataFrame, test: pd.DataFrame
    ) -> MetricResult: ...
