import sys

from omnirec.preprocess.base import Preprocessor
from omnirec.recsys_data_set import RawData, RecSysDataSet
from omnirec.util.util import get_random_state

# TODO: DOCS


class Subsample(Preprocessor):
    def __init__(self, sample_size: int | float) -> None:
        """Subsamples the dataset to a specified size.

        Args:
            sample_size (int | float): The size of the sample to draw from the dataset.
                                        int: The absolute number of interactions to include in the sample.
                                        float: The fraction of the dataset to include in the sample (between 0 and 1).
        """
        super().__init__()
        self.sample_size = sample_size

    def process(self, dataset: RecSysDataSet[RawData]) -> RecSysDataSet[RawData]:
        if isinstance(self.sample_size, int):
            if len(dataset._data.df) < self.sample_size:
                self.logger.critical(
                    f"Data set has less interactions {len(dataset._data.df)} than the sample size {self.sample_size}. Unable to subsample."
                )
                sys.exit(1)

            self.logger.info(
                f"Subsampling data set to {self.sample_size} interactions."
            )
            self.logger.info(
                f"Number of interactions before: {dataset.num_interactions()}"
            )
            dataset._data.df = dataset._data.df.sample(
                n=self.sample_size, random_state=get_random_state()
            )
            self.logger.info(
                f"Number of interactions after: {dataset.num_interactions()}"
            )

        elif isinstance(self.sample_size, float) and (0 <= self.sample_size <= 1):
            self.logger.info(f"Subsampling data set to fraction {self.sample_size}.")
            self.logger.info(
                f"Number of interactions before: {dataset.num_interactions()}"
            )
            dataset._data.df = dataset._data.df.sample(
                frac=self.sample_size, random_state=get_random_state()
            )
            self.logger.info(
                f"Number of interactions after: {dataset.num_interactions()}"
            )

        else:
            self.logger.critical(
                f"Sample size must be an integer or a float between 0 and 1. Got {type(self.sample_size)} with value {self.sample_size} instead."
            )
            sys.exit(1)

        return dataset
