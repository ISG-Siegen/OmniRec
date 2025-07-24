from typing import Generic, TypeVar

from recsyslib.preprocess.base import Preprocessor
from recsyslib.recsys_data_set import DataVariant, RecSysDataSet

# TODO: DOCS

T = TypeVar("T", bound=DataVariant)

# TODO: Add explaining node with link to PEP that will enable better typing here in the future


class Pipe(Preprocessor, Generic[T]):
    def __init__(self, *steps: Preprocessor) -> None:
        super().__init__()
        self._steps = steps

    def process(self, dataset: RecSysDataSet) -> RecSysDataSet[T]:
        for step in self._steps:
            dataset = step.process(dataset)
        return dataset
