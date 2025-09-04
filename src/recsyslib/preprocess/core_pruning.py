from collections import Counter

from recsyslib.preprocess.base import Preprocessor
from recsyslib.recsys_data_set import RawData, RecSysDataSet


class CorePruning(Preprocessor):
    def __init__(self, core: int) -> None:
        """Prune the dataset to the specified core. 
        Core pruning with a threshold of e.g. 5 means that only users and items with at least 5 interactions are included in the pruned dataset.

        Args:
            core (int): The core threshold for pruning.
        """
        super().__init__()
        self.core = core

    def process(self, dataset: RecSysDataSet[RawData]) -> RecSysDataSet[RawData]:
        self.logger.info(f"Pruning data set to {self.core}-core.")
        self.logger.info(f"Number of interactions before: {dataset.num_interactions()}")

        while True:
            # efficient pandas solution for core pruning loop
            while True:
                u_cnt = Counter(dataset._data.df["user"])
                i_cnt = Counter(dataset._data.df["item"])

                u_sig = set(k for k in u_cnt if u_cnt[k] >= self.core)
                i_sig = set(k for k in i_cnt if i_cnt[k] >= self.core)

                original_length = len(dataset._data.df)

                dataset._data.df = dataset._data.df[
                    dataset._data.df["user"].isin(u_sig)
                    & dataset._data.df["item"].isin(i_sig)
                ]

                if len(dataset._data.df) == original_length:
                    break

            if len(dataset._data.df) == 0:
                self.logger.warning("Data set is empty after pruning.")
                break
            else:
                # remove users that interacted with all items
                max_number_interactions = u_cnt.most_common()[0][1]
                number_of_items = len(i_cnt)
                if max_number_interactions == number_of_items:
                    u_sig = set(
                        user
                        for user, interaction_count in u_cnt.items()
                        if interaction_count < number_of_items
                    )
                    self.logger.info(
                        f"Removing {len(u_cnt) - len(u_sig)} users that interacted with all items."
                    )
                    dataset._data.df = dataset._data.df[
                        dataset._data.df["user"].isin(u_sig)
                    ]
                else:
                    break

        self.logger.info(f"Number of interactions after: {dataset.num_interactions()}")

        return dataset
