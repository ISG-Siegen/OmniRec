from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

import numpy as np
import pandas as pd
import pytest

from omnirec.data_variants import DataVariant, FoldedData, RawData, SplitData
from omnirec.preprocess.trace import Trace
from omnirec.recsys_data_set import DatasetMeta, RecSysDataSet


class MakeDataset[T: DataVariant](Protocol):
    def __call__(self, variant: type[T], with_lineage=False) -> RecSysDataSet[T]: ...


@pytest.fixture
def make_frame():
    def _make_frame(seed: int):
        rng = np.random.default_rng(seed)

        return pd.DataFrame(
            {
                "user": rng.integers(0, 100, size=10),
                "item": rng.integers(0, 100, size=10),
                "rating": rng.uniform(1.0, 5.0),
                "timestamp": rng.integers(100_000, 1_000_000, size=10),
            }
        )

    return _make_frame


@pytest.fixture
def make_dataset(make_frame) -> MakeDataset:
    def _make_dataset[T: DataVariant](variant: type[T], with_lineage=False):

        if variant == RawData:
            data = RawData(make_frame(42))

        elif variant == SplitData:
            data = SplitData(make_frame(42), make_frame(43), make_frame(44))
        elif variant == FoldedData:
            folds = {}
            for fold in range(5):
                folds[fold] = SplitData(
                    make_frame(42 + fold), make_frame(43 + fold), make_frame(44 + fold)
                )
            data = FoldedData(folds)
        else:
            raise ValueError(f"Unkonw data variant: {variant}")

        meta = DatasetMeta(
            Path("/some/canon/path"), Path("/some/raw/dir"), "TestDataset"
        )
        ds = RecSysDataSet(data, meta)

        if with_lineage:
            # Test all 3 variants of CountSummary
            trace_summaries = [
                {
                    "before_rows": 1000,
                    "before_columns": 4,
                    "after_rows": 750,
                    "after_columns": 3,
                },
                {
                    "before_rows": {"train": 1000, "val": 200, "test": 300},
                    "before_columns": {"train": 4, "val": 4, "test": 4},
                    "after_rows": {"train": 750, "val": 150, "test": 225},
                    "after_columns": {"train": 3, "val": 3, "test": 3},
                },
                {
                    "before_rows": {
                        0: {"train": 1000, "val": 200, "test": 300},
                        1: {"train": 950, "val": 190, "test": 285},
                    },
                    "before_columns": {
                        0: {"train": 4, "val": 4, "test": 4},
                        1: {"train": 4, "val": 4, "test": 4},
                    },
                    "after_rows": {
                        0: {"train": 750, "val": 150, "test": 225},
                        1: {"train": 725, "val": 145, "test": 215},
                    },
                    "after_columns": {
                        0: {"train": 3, "val": 3, "test": 3},
                        1: {"train": 3, "val": 3, "test": 3},
                    },
                },
            ]

            for i, trace_summary in enumerate(trace_summaries):
                trace = Trace(
                    component=f"Component{i}",
                    params={"component": i, "some": "params"},
                    executed_at=datetime.now(UTC),
                    runtime=42,
                    **trace_summary,
                )
                ds._lineage.append(trace)

        return ds

    return _make_dataset
