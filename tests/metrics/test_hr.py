import pytest
from pandas import DataFrame

from omnirec.metrics.ranking import HR
from tests.metrics.conftest import MakeDf


def test_hr_multiple_hits_still_count_as_one_hit(make_pred_df: MakeDf):
    """Several relevant recommendations must not increase a user's HR above 1.0."""
    pred = make_pred_df(3)
    test = DataFrame({"user": [1, 1], "item": [1, 2]})

    res = HR(3).calculate(pred, test)

    assert res.result == {3: pytest.approx(1.0)}
