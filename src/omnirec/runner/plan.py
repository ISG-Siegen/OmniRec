import itertools
import sys
from typing import Any, Optional, TypeAlias

from omnirec.runner.algos import Algorithms
from omnirec.util import util

logger = util._root_logger.getChild("config")

AlgorithmConfig: TypeAlias = dict[str, Any | list[Any]]


class ExperimentPlan:
    # TODO: Top level dict key for each algorithm
    def __init__(self, plan_name: Optional[str] = None):
        self._name = plan_name
        self._config: dict[str, AlgorithmConfig] = {}

    def add_algorithm(
        self,
        algorithm: Algorithms | str,
        algorithm_config: Optional[AlgorithmConfig] = None,
        force=False,
    ):
        """Adds an algorithm to the experiment plan.

        Args:
            algorithm (Algorithms | str): The algorithm to add.
            algorithm_config (Optional[AlgorithmConfig], optional): The configuration for the algorithm. Algorithm config depends of the origin library of the algorithm. We refer to their documentation for details about the algorithm hyperparameters.
            force (bool, optional): Whether to forcefully overwrite an existing algorithm config. Defaults to False.

        Example:
            ```Python
            # Create a new experiment plan
            plan = ExperimentPlan(plan_name="Example Plan")

            # Define algorithm configuration based on the lenskit ItemKNNScorer parameters
            lenskit_itemknn = {"max_nbrs": [10, 20], "min_nbrs": 5, "feedback": "implicit"}

            # Add algorithm with configuration to the plan
            plan.add_algorithm(Algorithms.ItemKNNScorer, lenskit_itemknn)
            ```    
        """
        if isinstance(algorithm, Algorithms):
            algorithm_name = algorithm.value
        else:
            algorithm_name = algorithm
        # TODO: Force option?
        if not algorithm_config:
            algorithm_config = {}
        if algorithm_name in self._config:
            logger.critical(
                f'Config for "{algorithm_name}" already exists! Use "force=True" to overwrite or update it using "update_algorithm_config()"'
            )
            sys.exit(1)

        self._config[algorithm_name] = algorithm_config

    def update_algorithm(self, algorithm_name: str, algorithm_config: AlgorithmConfig):
        """Updates the configuration for an existing algorithm in the experiment plan.

        Args:
            algorithm_name (str): The name of the algorithm to update.
            algorithm_config (AlgorithmConfig): The new configuration for the algorithm.
        """
        if algorithm_name not in self._config:
            self._config[algorithm_name] = algorithm_config
        else:
            self._config[algorithm_name].update(algorithm_config)

    def get_algorithm_config(self, algorithm_name: str) -> AlgorithmConfig:
        return self._config.get(algorithm_name, {})

    def _get_configs(self) -> list[tuple[str, list[dict[str, object]]]]:
        return [
            (
                algorithm,
                [
                    dict(zip(config.keys(), v))
                    for v in itertools.product(
                        *map(
                            lambda x: x if isinstance(x, list) else [x], config.values()
                        )
                    )
                ],
            )
            for algorithm, config in self._config.items()
        ]

    @property
    def plan_name(self):
        if self._name:
            return self._name
        else:
            return "Unnamed-Plan"
