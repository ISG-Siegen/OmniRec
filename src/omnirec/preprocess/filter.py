from typing import Optional

import pandas as pd

from omnirec.data_variants import RawData
from omnirec.preprocess.base import Preprocessor
from omnirec.recsys_data_set import RecSysDataSet


class TimeFilter(Preprocessor[RawData, RawData]):
    def __init__(
        self, start: Optional[pd.Timestamp] = None, end: Optional[pd.Timestamp] = None
    ) -> None:
        super().__init__()
        self._start = start
        self._end = end

    def process(self, dataset: RecSysDataSet[RawData]) -> RecSysDataSet[RawData]:
        df = dataset._data.df
        mask = pd.Series(True, index=df.index)
        if self._start is not None:
            mask &= df["timestamp"] >= self._start.timestamp()
        if self._end is not None:
            mask &= df["timestamp"] <= self._end.timestamp()
        df = df.loc[mask]
        return dataset.replace_data(RawData(df))
