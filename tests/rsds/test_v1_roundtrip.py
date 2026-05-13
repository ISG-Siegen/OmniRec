import pandas as pd

from omnirec.data_variants import FoldedData, RawData, SplitData
from omnirec.recsys_data_set import RecSysDataSet
from omnirec.rsds.dispatcher import load_dataset, save_dataset
from tests.conftest import MakeDataset


def test_raw_roundtrip(make_dataset: MakeDataset[RawData], tmp_path):
    ds = make_dataset(RawData, with_lineage=True)
    path = tmp_path / "test.rsds"

    save_dataset(ds, path, 1)
    loaded: RecSysDataSet[RawData] = load_dataset(path)

    assert loaded._lineage == []
    assert ds._meta == loaded._meta
    pd.testing.assert_frame_equal(ds._data.df, loaded._data.df)


def test_split_roundtrip(make_dataset: MakeDataset[SplitData], tmp_path):
    ds = make_dataset(SplitData)
    path = tmp_path / "test.rsds"

    save_dataset(ds, path, 1)
    loaded: RecSysDataSet[SplitData] = load_dataset(path)

    assert ds._meta == loaded._meta
    for split in ("train", "val", "test"):
        pd.testing.assert_frame_equal(ds._data.get(split), loaded._data.get(split))


def test_folded_roundtrip(make_dataset: MakeDataset[FoldedData], tmp_path):
    ds = make_dataset(FoldedData)
    path = tmp_path / "test.rsds"

    save_dataset(ds, path, 1)
    loaded: RecSysDataSet[FoldedData] = load_dataset(path)

    assert ds._meta == loaded._meta
    assert ds._data.folds.keys() == loaded._data.folds.keys()
    for fold_x, x in ds._data.folds.items():
        y = loaded._data.folds[fold_x]
        for split in ("train", "val", "test"):
            pd.testing.assert_frame_equal(x.get(split), y.get(split))
