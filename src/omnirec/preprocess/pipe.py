from typing import Any, Generic, TypeVar, TypeVarTuple, Unpack, cast

from omnirec.preprocess.base import Preprocessor
from omnirec.recsys_data_set import DataVariant, RecSysDataSet


T = TypeVar("T", bound=DataVariant)
Ts = TypeVarTuple("Ts")


class Pipe(Generic[T]):
    def __init__(self, *steps: Unpack[tuple[Unpack[Ts], Preprocessor[Any, T]]]) -> None:
        """Pipeline for automatically applying sequential preprocessing steps. Takes as input a sequence of Preprocessor objects.
        If process() is called, each step's process method is called in the order they were provided.
        Example:
            ```Python
                # Define preprocessing steps
                pipe = Pipe(
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

    def process(self, data: RecSysDataSet) -> RecSysDataSet[T]:
        for step in self._steps[:-1]:
            step = cast(Preprocessor, step)
            data = step.process(data)
        data = self._steps[-1].process(data)
        return data
