import itertools
import sys
from typing import Any, Optional, TypeAlias

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
        algorithm_name: str,
        algorithm_config: Optional[AlgorithmConfig] = None,
        force=False,
    ):
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
