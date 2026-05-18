import functools
import inspect
from abc import ABC, abstractmethod
from datetime import UTC, datetime
from time import perf_counter
from typing import Any, Generic, Self, TypeVar, final

from omnirec.preprocess.trace import Trace
from omnirec.recsys_data_set import DataVariant, RecSysDataSet
from omnirec.util import util

# TODO (Python 3.12+): Replace TypeVar with inline generic syntax `class Box[T](...)`
T = TypeVar("T", bound=DataVariant)
U = TypeVar("U", bound=DataVariant)


class Preprocessor(ABC, Generic[T, U]):
    logger = util._root_logger.getChild("preprocess")

    def __init__(self) -> None:
        self._trace_component: str
        self._trace_params: dict[str, Any]

        if not hasattr(self, "_trace_component"):
            self._trace_component = type(self).__name__
        if not hasattr(self, "_trace_params"):
            self._trace_params = {}
        super().__init__()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if "__init__" in cls.__dict__:
            original_init = cls.__init__

            @functools.wraps(original_init)
            def wrapped_init(self: Self, *args: Any, **kwargs: Any) -> None:
                if not hasattr(self, "_trace_component"):
                    sig = inspect.signature(original_init)
                    bound = sig.bind_partial(self, *args, **kwargs)
                    bound.apply_defaults()

                    self._trace_component = type(self).__name__
                    self._trace_params = {
                        k: v for k, v in bound.arguments.items() if k != "self"
                    }

                original_init(self, *args, **kwargs)

            cls.__init__ = wrapped_init

    @abstractmethod
    def _process(self, dataset: RecSysDataSet[T]) -> RecSysDataSet[U]:
        """Implementation hook for transforming a dataset.

        Subclasses should override this method with the preprocessing logic itself.
        Callers should use ``process()`` rather than invoking this method directly.

        Args:
            dataset (RecSysDataSet[T]): The dataset to transform.

        Returns:
            RecSysDataSet[U]: The transformed dataset.
        """
        pass

    @final
    def process(self, dataset: RecSysDataSet[T]) -> RecSysDataSet[U]:
        """Processes a dataset and records execution metadata in the lineage.

        This is the public entry point for running a preprocessor. It delegates
        the actual transformation to ``process_impl()`` and wraps it with shared
        logic such as timing, dataset shape capture, and trace creation.

        Args:
            dataset (RecSysDataSet[T]): The dataset to process.

        Returns:
            RecSysDataSet[U]: The processed dataset with an appended trace entry.
        """
        before_rows = dataset.num_interactions()
        before_columns = dataset.num_columns()
        start_time = perf_counter()
        new_ds = self._process(dataset)
        runtime = perf_counter() - start_time

        trace = Trace(
            component=self._trace_component,
            params=self._trace_params.copy(),
            executed_at=datetime.now(UTC),
            runtime=runtime,
            before_rows=before_rows,
            before_columns=before_columns,
            after_rows=new_ds.num_interactions(),
            after_columns=new_ds.num_columns(),
        )
        new_ds._lineage.append(trace)
        return new_ds
