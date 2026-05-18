import os

from omnirec.data_loaders.registry import list_datasets, register_dataloader
from omnirec.metrics.ranking import HR, NDCG, Recall
from omnirec.recsys_data_set import DatasetMeta, RecSysDataSet
from omnirec.util.util import set_log_level

__all__ = [
    "RecSysDataSet",
    "DatasetMeta",
    "list_datasets",
    "register_dataloader",
    "NDCG",
    "HR",
    "Recall",
]


set_log_level(os.getenv("OMNIREC_LOG", "INFO"))
