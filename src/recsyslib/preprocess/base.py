from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from recsyslib.recsys_data_set import DataVariant, RecSysDataSet
from recsyslib.util import util

# TODO (Python 3.12+): Replace TypeVar with inline generic syntax `class Box[T](...)`
T = TypeVar("T", bound=DataVariant)
U = TypeVar("U", bound=DataVariant)


class Preprocessor(ABC, Generic[T, U]):
    logger = util._logger.getChild("preprocess")

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def process(self, dataset: RecSysDataSet[T]) -> RecSysDataSet[U]:
        """Processes the dataset and returns a new dataset variant.

            Args:
                dataset (RecSysDataSet[T]): The dataset to process.

            Returns:
                RecSysDataSet[U]: The processed dataset.
        """
        pass
        
