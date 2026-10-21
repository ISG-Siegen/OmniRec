from collections.abc import Callable

import pytest
from pandas import DataFrame

MakeDf = Callable[[int], DataFrame]


@pytest.fixture
def make_pred_df() -> MakeDf:
    """Factory fixture to generate a simple prediction DataFrame of size `num_items` with only one user with id `1`."""

    def _make(num_items: int = 5) -> DataFrame:
        items = list(range(1, num_items + 1))
        return DataFrame(
            {
                "user": [1] * num_items,
                "item": items,
                "score": [float(x) for x in items],
                "rank": items,
            }
        )

    return _make


@pytest.fixture
def make_test_df() -> MakeDf:
    """Factory fixture to generate a simple test DataFrame of size `num_items` with only one user with id `1`."""

    def _make(num_items: int = 5) -> DataFrame:
        return DataFrame(
            {
                "user": [1] * num_items,
                "item": list(range(1, num_items + 1)),
            }
        )

    return _make
