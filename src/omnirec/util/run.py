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
    c = Coordinator()
    c.run(datasets, plan, evaluator)
