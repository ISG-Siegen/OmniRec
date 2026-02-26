import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Sequence

from omnirec.util.util import get_random_state


class PlanComponentBase[T](ABC):
    @abstractmethod
    def get_values(self) -> Iterable[T]: ...


class RandomBase[T](PlanComponentBase[T]):
    def __init__(self) -> None:
        super().__init__()
        self.rng = random.Random(get_random_state())


@dataclass
class Grid[T](PlanComponentBase[T]):
    """Exhaustive grid search over a fixed set of values.

    All provided values are returned by `get_values()`, and the framework
    generates one experiment run for every combination across all `Grid`
    parameters in an `algorithm_config`.

    Args:
        values (Iterable[T]): The values to enumerate.

    Example:
        ```python
        from omnirec.runner.plan_components import Grid

        config = {"max_nbrs": Grid([10, 20, 50]), "min_nbrs": 1}
        # Produces three runs: max_nbrs=10, max_nbrs=20, max_nbrs=50
        ```
    """

    values: Iterable[T]

    def get_values(self) -> Iterable[T]:
        return self.values


@dataclass
class RandomChoice[T](RandomBase[T]):
    """Random sampling of `n` items from a discrete list of choices.

    Useful for random search over a predefined set of candidate values.
    The sample is drawn without replacement using the global OmniRec random
    state, ensuring reproducibility.

    Args:
        choices (Sequence[T]): Pool of candidate values to sample from.
        n (int): Number of values to draw.

    Example:
        ```python
        from omnirec.runner.plan_components import RandomChoice

        config = {"max_nbrs": RandomChoice([10, 20, 50, 100, 200], n=3)}
        # Picks 3 values at random from the list
        ```
    """

    choices: Sequence[T]
    n: int

    def __post_init__(self):
        super().__init__()

    def get_values(self) -> Iterable[T]:
        return self.rng.sample(self.choices, self.n)


@dataclass
class RandomRange[T: (int, float)](RandomBase[T]):
    """Random sampling of `n` values from a numeric range.

    - If both `start` and `end` are `int`, values are drawn without replacement
      from the integer range `[start, end]` (inclusive).
    - If either bound is a `float`, values are drawn independently from a
      uniform distribution over `[start, end]`.

    The random state is derived from the global OmniRec random seed, ensuring
    reproducibility.

    Args:
        start (int | float): Lower bound of the range (inclusive).
        end (int | float): Upper bound of the range (inclusive).
        n (int): Number of values to sample.

    Example:
        ```python
        from omnirec.runner.plan_components import RandomRange

        config = {
            "learning_rate": RandomRange(0.0001, 0.01, n=4),  # 4 random floats
            "embedding_size": RandomRange(32, 256, n=3),       # 3 random ints
        }
        ```
    """

    start: T
    end: T
    n: int

    def __post_init__(self):
        super().__init__()

    def get_values(self) -> Iterable[T]:
        if isinstance(self.start, int) and isinstance(self.end, int):
            return self.rng.sample(range(self.start, self.end + 1), self.n)
        else:
            return [self.rng.uniform(self.start, self.end) for _ in range(self.n)]
