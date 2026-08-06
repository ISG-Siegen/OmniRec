import logging
import math
from itertools import permutations

import pytest
from pandas import DataFrame

from omnirec.metrics.ranking import HR, NDCG, Precision, RankingMetric, Recall
from tests.metrics.conftest import MakeDf


@pytest.mark.parametrize("metric_class", [NDCG, HR, Recall, Precision])
def test_ranking_metric_perfect_ranking(
    metric_class: type[RankingMetric], make_pred_df: MakeDf, make_test_df: MakeDf
):
    """All ranking metrics score a perfect ranking as 1.0."""
    res = metric_class(5).calculate(make_pred_df(5), make_test_df(5))

    assert res.result == {5: pytest.approx(1.0)}


@pytest.mark.parametrize("metric_class", [NDCG, HR, Recall, Precision])
def test_ranking_metric_zero_hits(
    metric_class: type[RankingMetric], make_pred_df: MakeDf
):
    """All ranking metrics score disjoint predictions as 0.0."""
    test = DataFrame({"user": [1, 1, 1], "item": [100, 101, 102]})

    res = metric_class(5).calculate(make_pred_df(5), test)

    assert res.result == {5: pytest.approx(0.0)}


@pytest.mark.parametrize(
    ("metric_class", "expected_score"),
    [(NDCG, 1.0), (HR, 1.0), (Recall, 1.0), (Precision, 0.05)],
)
def test_ranking_metric_k_larger_than_prediction_length(
    metric_class: type[RankingMetric],
    expected_score: float,
    make_pred_df: MakeDf,
    make_test_df: MakeDf,
):
    """The metrics handle a requested cutoff beyond the predictions correctly."""
    res = metric_class(100).calculate(make_pred_df(5), make_test_df(5))

    assert res.result == {100: pytest.approx(expected_score)}


@pytest.mark.parametrize(
    ("metric_class", "expected_score"),
    [(HR, 1.0), (Recall, 1.0), (Precision, 1 / 3)],
)
@pytest.mark.parametrize("items", list(permutations([10, 20, 30])))
def test_non_discounted_ranking_metrics_are_invariant_to_item_order(
    metric_class: type[RankingMetric], expected_score: float, items: tuple[int]
):
    """HR, Recall, and Precision do not discount a hit's position within k."""
    pred = DataFrame(
        {
            "user": [1, 1, 1],
            "item": items,
            "score": [3.0, 2.0, 1.0],
            "rank": [1, 2, 3],
        }
    )
    test = DataFrame({"user": [1], "item": [20]})

    res = metric_class(3).calculate(pred, test)

    assert res.result == {3: pytest.approx(expected_score)}


@pytest.mark.parametrize(
    ("metric_class", "expected_result"),
    [
        (NDCG, {5: 0.0, 10: 1 / math.log2(7)}),
        (HR, {5: 0.0, 10: 1.0}),
        (Recall, {5: 0.0, 10: 1.0}),
        (Precision, {5: 0.0, 10: 0.1}),
    ],
)
def test_ranking_metric_k_cutoff_isolation(
    metric_class: type[RankingMetric], expected_result: dict
):
    """A hit beyond one cutoff must only count at the larger cutoff."""
    pred = DataFrame(
        {
            "user": [1] * 10,
            "item": list(range(1, 11)),
            "score": list(range(10, 0, -1)),
            "rank": list(range(1, 11)),
        }
    )
    test = DataFrame({"user": [1], "item": [6]})

    res = metric_class([5, 10]).calculate(pred, test)

    assert res.result == {
        k: pytest.approx(score) for k, score in expected_result.items()
    }


@pytest.mark.parametrize("metric_class", [NDCG, HR, Recall, Precision])
def test_ranking_metric_multiple_k_dictionary_structure(
    metric_class: type[RankingMetric], make_pred_df: MakeDf, make_test_df: MakeDf
):
    """All requested cutoffs must appear in every result dictionary."""
    res = metric_class([1, 5, 10]).calculate(make_pred_df(10), make_test_df(3))

    assert isinstance(res.result, dict)
    assert set(res.result.keys()) == {1, 5, 10}
    assert all(isinstance(score, float) for score in res.result.values())


@pytest.mark.parametrize(
    ("metric_class", "expected_score"),
    [(NDCG, 0.5), (HR, 0.5), (Recall, 0.5), (Precision, 0.25)],
)
def test_ranking_metric_multi_user_averaging(
    metric_class: type[RankingMetric], expected_score: float
):
    """Per-user scores must be averaged with each metric's semantics."""
    pred = DataFrame(
        {
            "user": [1, 1, 2, 2],
            "item": [10, 20, 30, 40],
            "score": [2.0, 1.0, 2.0, 1.0],
            "rank": [1, 2, 1, 2],
        }
    )
    test = DataFrame({"user": [1, 2], "item": [10, 99]})

    res = metric_class(2).calculate(pred, test)

    assert res.result == {2: pytest.approx(expected_score)}


@pytest.mark.parametrize(
    ("metric_class", "expected_result"),
    [
        (NDCG, {1: 1.0, 2: 1.0}),
        (HR, {1: 1.0, 2: 1.0}),
        (Recall, {1: 1.0, 2: 1.0}),
        (Precision, {1: 1.0, 2: 0.5}),
    ],
)
def test_ranking_metric_skips_users_with_no_ground_truth_items(
    metric_class: type[RankingMetric],
    expected_result: dict,
    caplog: pytest.LogCaptureFixture,
):
    """Users without test items must be excluded and reported through logs."""
    pred = DataFrame(
        {
            "user": [1, 1, 2, 2, 3, 3],
            "item": [1, 2, 3, 4, 5, 6],
            "score": [2.0, 1.0, 2.0, 1.0, 2.0, 1.0],
            "rank": [1, 2, 1, 2, 1, 2],
        }
    )
    test = DataFrame({"user": [1], "item": [1]})
    caplog.set_level(logging.DEBUG, logger="omnirec.data")

    res = metric_class([1, 2]).calculate(pred, test)

    assert res.result == {
        k: pytest.approx(score) for k, score in expected_result.items()
    }
    warning_records = [
        record for record in caplog.records if record.levelno == logging.WARNING
    ]
    debug_records = [
        record for record in caplog.records if record.levelno == logging.DEBUG
    ]
    assert len(warning_records) == 1
    assert "Skipped 2 user(s)" in warning_records[0].message
    assert "empty test set" in warning_records[0].message
    assert len(debug_records) == 1
    assert "[2, 3]" in debug_records[0].message


@pytest.mark.parametrize("metric_class", [NDCG, HR, Recall, Precision])
def test_ranking_metric_does_not_log_when_all_users_have_ground_truth_items(
    metric_class: type[RankingMetric],
    make_pred_df: MakeDf,
    make_test_df: MakeDf,
    caplog: pytest.LogCaptureFixture,
):
    """Eligible users must not cause skip-related logs."""
    caplog.set_level(logging.DEBUG, logger="omnirec.data")

    metric_class(2).calculate(make_pred_df(2), make_test_df(2))

    assert not caplog.records


@pytest.mark.parametrize("metric_class", [NDCG, HR, Recall, Precision])
def test_ranking_metric_all_users_skipped_returns_zero_for_each_cutoff(
    metric_class: type[RankingMetric], caplog: pytest.LogCaptureFixture
):
    """No eligible users must retain the result shape and be reported."""
    pred = DataFrame(
        {
            "user": [1, 1, 2, 2],
            "item": [1, 2, 3, 4],
            "score": [2.0, 1.0, 2.0, 1.0],
            "rank": [1, 2, 1, 2],
        }
    )
    test = DataFrame({"user": [], "item": []})
    caplog.set_level(logging.DEBUG, logger="omnirec.data")

    res = metric_class([1, 2]).calculate(pred, test)

    assert res.result == {1: pytest.approx(0.0), 2: pytest.approx(0.0)}
    assert "Skipped 2 user(s)" in caplog.text
    assert "[1, 2]" in caplog.text
