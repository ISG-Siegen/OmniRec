import sys

from omnirec.recsys_data_set import RawData, RecSysDataSet

from .base import Preprocessor


class MakeImplicit(Preprocessor[RawData, RawData]):
    def __init__(self, threshold: int | float) -> None:
        """Converts explicit feedback to implicit feedback using the specified threshold.

        Args:
            threshold (int | float): The threshold for converting feedback.
                                        int: Used directly as the threshold, e.g. 3 -> only interactions with a rating of 3 or higher are included.
                                        float: Interpreted as a fraction of the maximum rating, e.g. 0.5 -> only interactions with a rating of at least 50% of the maximum rating are included.
        """
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
