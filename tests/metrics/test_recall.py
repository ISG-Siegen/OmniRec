import pytest
from pandas import DataFrame

from omnirec.metrics.ranking import Recall
from tests.metrics.conftest import MakeDf


def test_recall_is_capped_by_the_cutoff(make_pred_df: MakeDf):
    """The documented denominator allows full recall when all k slots are hits."""
    pred = make_pred_df(3)
    test = DataFrame({"user": [1, 1, 1, 1, 1], "item": [1, 2, 3, 4, 5]})

    res = Recall(3).calculate(pred, test)

    assert res.result == {3: pytest.approx(1.0)}
