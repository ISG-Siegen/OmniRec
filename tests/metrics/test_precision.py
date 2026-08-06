import pytest
from pandas import DataFrame

from omnirec.metrics.ranking import Precision


def test_precision_counts_each_hit_within_the_cutoff():
    """Two relevant items in the top four must yield precision 2/4."""
    pred = DataFrame(
        {
            "user": [1, 1, 1, 1],
            "item": [10, 20, 30, 40],
            "score": [4.0, 3.0, 2.0, 1.0],
            "rank": [1, 2, 3, 4],
        }
    )
    test = DataFrame({"user": [1, 1], "item": [10, 20]})

    res = Precision(4).calculate(pred, test)

    assert res.result == {4: pytest.approx(0.5)}
