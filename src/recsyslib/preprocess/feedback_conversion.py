import sys

from recsyslib.recsys_data_set import RawData, RecSysDataSet

from .base import Preprocessor

# TODO: DOCS


class MakeImplicit(Preprocessor):
    def __init__(self, threshold: int | float) -> None:
        super().__init__()
        self.threshold = threshold

    def process(self, dataset: RecSysDataSet[RawData]) -> RecSysDataSet[RawData]:
        self.logger.info(f"Making data set implicit with threshold {self.threshold}.")
        self.logger.info(f"Minimum rating: {dataset.min_rating()}")
        self.logger.info(f"Maximum rating: {dataset.max_rating()}")
        self.logger.info(f"Number of interactions before: {dataset.num_interactions()}")
        if isinstance(self.threshold, int):
            dataset._data.df = dataset._data.df[
                dataset._data.df["rating"] >= self.threshold
            ][["user", "item"]]
        elif isinstance(self.threshold, float) and (0 <= self.threshold <= 1):
            scaled_max_rating = abs(dataset.max_rating()) + abs(dataset.min_rating())
            rating_cutoff = round(scaled_max_rating * self.threshold) - abs(
                dataset.min_rating()
            )
            dataset._data.df = dataset._data.df[
                dataset._data.df["rating"] >= rating_cutoff
            ][["user", "item"]]
        else:
            self.logger.critical(
                f"Threshold must be an integer or a float between 0 and 1. Got {type(self.threshold)} with value {self.threshold} instead."
            )
            sys.exit(1)
        # self.set_feedback_type() # TODO: ?

        self.logger.info(f"Number of interactions after: {dataset.num_interactions()}")
        return dataset
