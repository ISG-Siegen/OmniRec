import sys
from typing import Iterable, Optional, TypeAlias

from pandas import DataFrame

from omnirec.metrics.base import Metric, MetricResult
from omnirec.util import util

logger = util._root_logger.getChild("eval")


EvalutaionResults: TypeAlias = dict[
    str, list[MetricResult] | dict[int, list[MetricResult]]
]


class Evaluator:
    def __init__(self, metrics: Metric | Iterable[Metric]) -> None:
        if not isinstance(metrics, Iterable):
            metrics = [metrics]
        self._metrics = metrics
        self._results: EvalutaionResults = {}

    def run_evaluation(
        self,
        algorithm: str,
        predictions: DataFrame,
        test: DataFrame,
        fold: Optional[int] = None,
    ):
        if algorithm in self._results:
            if fold is not None:
                res = self._results[algorithm]
                if isinstance(res, dict) and fold in res.keys():
                    self._eval_error(algorithm)
            else:
                self._eval_error(algorithm)

        for m in self._metrics:
            mr = m.calculate(predictions, test)
            if fold is not None:
                res = self._results.setdefault(algorithm, {})
                if isinstance(res, dict):
                    res.setdefault(fold, []).append(mr)
                else:
                    logger.critical("Invalid result type")
                    sys.exit(1)
            else:
                self._results.setdefault(algorithm, []).append(mr)  # type: ignore

    def _eval_error(self, algorithm: str):
        logger.critical(f"Algorithm {algorithm} already evaluated!")
        sys.exit(1)
