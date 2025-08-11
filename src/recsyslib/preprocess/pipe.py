from typing import Generic, TypeVar

from recsyslib.preprocess.base import Preprocessor
from recsyslib.recsys_data_set import DataVariant, RecSysDataSet

# TODO: DOCS

T = TypeVar("T", bound=DataVariant)

# TODO: Add explaining node with link to PEP that will enable better typing here in the future


class Pipe(Preprocessor, Generic[T]):
    def __init__(self, *steps: Preprocessor) -> None:
        """Pipeline for automatically applying sequential preprocessing steps. Takes as input a sequence of Preprocessor objects.
            If process() is called, each step's process method is called in the order they were provided.
        Example:
            ```
                # Define preprocessing steps
                pipe = Pipe[FoldedData](
                    Subsample(0.1),
                    MakeImplicit(3),
                    CorePruning(5),
                    UserCrossValidation(5, 0.1),
                )

                # Apply the steps
                dataset = pipe.process(dataset)
            ```
        """
        super().__init__()
        self._steps = steps

    def process(self, dataset: RecSysDataSet) -> RecSysDataSet[T]:
        for step in self._steps:
            dataset = step.process(dataset)
        return dataset
