from typing import Optional

import pandas as pd

from omnirec.data_variants import RawData
from omnirec.preprocess.base import Preprocessor
from omnirec.recsys_data_set import RecSysDataSet


class TimeFilter(Preprocessor[RawData, RawData]):
    def __init__(
        self, start: Optional[pd.Timestamp] = None, end: Optional[pd.Timestamp] = None
    ) -> None:
        """Filters the interactions by a time range. Only interactions within the specified start and end timestamps are retained.

        Args:
            start (Optional[pd.Timestamp], optional): The start timestamp for the filter. Defaults to None.
            end (Optional[pd.Timestamp], optional): The end timestamp for the filter. Defaults to None.
        """
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


class RatingFilter(Preprocessor[RawData, RawData]):
    def __init__(
        self, lower: Optional[int | float] = None, upper: Optional[int | float] = None
    ) -> None:
        """Filters the interactions by rating values. Only interactions with ratings within the specified lower and upper bounds are retained.

        Args:
            lower (Optional[int  |  float], optional): The lower bound for the filter. Defaults to None.
            upper (Optional[int  |  float], optional): The upper bound for the filter. Defaults to None.
        """
        super().__init__()
        self._lower = lower
        self._upper = upper

    def process(self, dataset: RecSysDataSet[RawData]) -> RecSysDataSet[RawData]:
        df = dataset._data.df
        mask = pd.Series(True, index=df.index)
        if self._lower is not None:
            mask &= df["rating"] >= self._lower
        if self._upper is not None:
            mask &= df["rating"] <= self._upper
        df = df.loc[mask]
        return dataset.replace_data(RawData(df))
