from typing import Iterable, TypeVar

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
):
    """Run the OmniRec framework with the specified datasets, experiment plan, and evaluator.

    Args:
        datasets (RecSysDataSet[T] | Iterable[RecSysDataSet[T]]): The dataset(s) to use for the experiment.
        plan (ExperimentPlan): The experiment plan to follow.
        evaluator (Evaluator): The evaluator to use for the experiment.
    """
    c = Coordinator()
    c.run(datasets, plan, evaluator)
