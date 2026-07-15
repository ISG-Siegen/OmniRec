import pandas as pd
import pytest

from omnirec.metrics.base import Metric, MetricResult
from omnirec.runner.evaluation import Evaluator


class DummyMetric(Metric):
    def __init__(self, name: str = "Dummy", ks: list[int] | None = None):
        self._name = name
        self._ks = ks or [5, 10]

    def calculate(self, predictions: pd.DataFrame, test: pd.DataFrame) -> MetricResult:
        return MetricResult(self._name, {k: 0.5 for k in self._ks})


@pytest.fixture
def frames():
    predictions = pd.DataFrame({"user": [1], "item": [2], "score": [0.9], "rank": [1]})
    test = pd.DataFrame({"user": [1], "item": [2], "rating": [5.0]})
    return predictions, test


def test_get_results_accumulates_across_evaluations(frames):
    predictions, test = frames
    evaluator = Evaluator(DummyMetric())

    evaluator.run_evaluation("ds-a", "algo1", predictions, test)
    evaluator.run_evaluation("ds-a", "algo2", predictions, test)
    evaluator.run_evaluation("ds-b", "algo1", predictions, test)

    results = evaluator.get_results()
    assert set(results) == {"ds-a", "ds-b"}
    assert len(results["ds-a"]) == 4  # 2 algorithms x 2 k values
    assert len(results["ds-b"]) == 2


def test_scope_all_includes_loaded_results(frames, tmp_path):
    predictions, test = frames

    first = Evaluator(DummyMetric())
    first.run_evaluation("ds-a", "algo1", predictions, test)
    results_path = tmp_path / "results.json"
    first.save_results(results_path)

    fresh = Evaluator(DummyMetric())
    fresh.load_results(results_path)
    fresh.run_evaluation("ds-b", "algo1", predictions, test)

    all_results = fresh.get_results()
    assert set(all_results) == {"ds-a", "ds-b"}
    assert all_results["ds-a"].equals(first.get_results()["ds-a"])


def test_scope_run_excludes_loaded_results(frames, tmp_path):
    predictions, test = frames

    first = Evaluator(DummyMetric())
    first.run_evaluation("ds-a", "algo1", predictions, test)
    results_path = tmp_path / "results.json"
    first.save_results(results_path)

    fresh = Evaluator(DummyMetric())
    fresh._start_run()
    fresh.load_results(results_path)
    fresh.run_evaluation("ds-b", "algo1", predictions, test)

    run_results = fresh.get_results(scope="run")
    assert set(run_results) == {"ds-b"}
    assert len(run_results["ds-b"]) == 2


def test_start_run_resets_only_run_scope(frames):
    predictions, test = frames
    evaluator = Evaluator(DummyMetric())

    evaluator.run_evaluation("ds-a", "algo1", predictions, test)
    evaluator._start_run()
    evaluator.run_evaluation("ds-b", "algo1", predictions, test)

    assert set(evaluator.get_results(scope="run")) == {"ds-b"}
    assert set(evaluator.get_results()) == {"ds-a", "ds-b"}


def test_save_load_roundtrip(frames, tmp_path):
    predictions, test = frames
    evaluator = Evaluator(DummyMetric())
    evaluator.run_evaluation("ds-a", "algo1", predictions, test, fold=0)
    evaluator.run_evaluation("ds-a", "algo1", predictions, test, fold=1)

    results_path = tmp_path / "results.json"
    evaluator.save_results(results_path)

    restored = Evaluator(DummyMetric())
    restored.load_results(results_path)

    original = evaluator.get_results()["ds-a"].reset_index(drop=True)
    loaded = restored.get_results()["ds-a"].reset_index(drop=True)
    assert loaded.astype(object).where(loaded.notna(), None).equals(
        original.astype(object).where(original.notna(), None)
    )
