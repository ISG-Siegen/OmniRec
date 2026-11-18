import pytest
import requests

from omnirec.data_loaders.base import DatasetInfo, Loader
from omnirec.data_loaders.registry import _run_loader, register_dataloader


class BrokenDownloadLoader(Loader):
    @staticmethod
    def info(name):
        return DatasetInfo(download_urls="https://example.com/data.zip", checksum="0" * 64)

    @staticmethod
    def load(source_dir, name):
        raise AssertionError("load must not be reached")


class FakeResponse:
    status_code = 200
    headers = {}

    def iter_content(self, chunk_size):
        yield b"<html>not the dataset</html>"


def test_checksum_failure_exits_with_error(monkeypatch, tmp_path):
    register_dataloader("BrokenDownloadTest", BrokenDownloadLoader)
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: FakeResponse())

    with pytest.raises(SystemExit) as exc:
        _run_loader("BrokenDownloadTest", raw_dir=tmp_path)

    assert exc.value.code == 1