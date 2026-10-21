import math

import pytest
from pandas import DataFrame

from omnirec.metrics.ranking import NDCG
from tests.metrics.conftest import MakeDf


def test_ndcg_known_hand_calculated_value(make_pred_df: MakeDf):
    """A single relevant item at rank two has the expected discounted score."""
    pred = make_pred_df(3)
    test = DataFrame({"user": [1], "item": [2]})

    res = NDCG(3).calculate(pred, test)

    assert res.result == {3: pytest.approx(1.0 / math.log2(3))}


def test_ndcg_positional_monotonicity():
    """A relevant item at a higher rank must yield a higher NDCG score."""
    test = DataFrame({"user": [1], "item": [99]})
    pred_rank_1 = DataFrame(
        {
            "user": [1, 1, 1],
            "item": [99, 2, 3],
            "score": [3.0, 2.0, 1.0],
            "rank": [1, 2, 3],
        }
    )
    pred_rank_3 = DataFrame(
        {
            "user": [1, 1, 1],
            "item": [1, 2, 99],
            "score": [3.0, 2.0, 1.0],
            "rank": [1, 2, 3],
        }
    )

    res_rank_1 = NDCG(3).calculate(pred_rank_1, test)
    res_rank_3 = NDCG(3).calculate(pred_rank_3, test)

    assert isinstance(res_rank_1.result, dict)
    assert isinstance(res_rank_3.result, dict)
    assert res_rank_1.result[3] > res_rank_3.result[3]
