from os import PathLike
from typing import Iterable, Optional, TypeVar

from rich.console import Console

from omnirec.data_variants import DataVariant
from omnirec.recsys_data_set import RecSysDataSet
from omnirec.runner.coordinator import Coordinator
from omnirec.runner.evaluation import Evaluator
from omnirec.runner.plan import ExperimentPlan

T = TypeVar("T", bound=DataVariant)


def run_omnirec(
    datasets: RecSysDataSet[T] | Iterable[RecSysDataSet[T]],
    plan: ExperimentPlan,
    evaluator: Evaluator,  # TODO: Make optional
    slurm_script: Optional[PathLike | str] = None
):
    """Run the OmniRec framework with the specified datasets, experiment plan, and evaluator.

    Args:
        datasets (RecSysDataSet[T] | Iterable[RecSysDataSet[T]]): The dataset(s) to use for the experiment.
        plan (ExperimentPlan): The experiment plan to follow.
        evaluator (Evaluator): The evaluator to use for the experiment.
        slurm_script (Optional[PathLike | str]): Path to a SLURM script used to schedule experiments
            on an HPC cluster. If not provided, the experiments are run locally in normal mode.
    """
    if slurm_script is not None:
        # TODO:
        raise NotImplementedError()

    c = Coordinator()
    c.run(datasets, plan, evaluator)

    for table in evaluator.get_tables():
        console = Console()
        console.print(table)
