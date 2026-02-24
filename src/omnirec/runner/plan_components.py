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
    values: Iterable[T]

    def get_values(self) -> Iterable[T]:
        return self.values


@dataclass
class RandomChoice[T](RandomBase[T]):
    choices: Sequence[T]
    n: int

    def __post_init__(self):
        super().__init__()

    def get_values(self) -> Iterable[T]:
        return self.rng.sample(self.choices, self.n)


@dataclass
class RandomRange[T: (int, float)](RandomBase[T]):
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
