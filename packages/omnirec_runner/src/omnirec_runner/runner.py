import json
import socket
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from concurrent.futures import Future, ProcessPoolExecutor
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from time import time
from typing import Any, Callable, Dict, List, Type
from uuid import uuid4

import rpyc
from rpyc.utils.authenticators import SSLAuthenticator
from rpyc.utils.server import ThreadedServer


@dataclass
class RunnerInfo:
    runner_path: Path
    algorithms: List[str]
    python_version: str
    packages: List[str]


@dataclass
class RunnerConfig:
    algorithm: str
    config: dict
    data_dir: Path
    checkpoint_dir: Path
    tmp_dir: Path


class _RunnerService(ABC):
    @abstractmethod
    def _config(
        self,
        algorithm_name: str,
        algorithm_config: str,
        dataset_name: str,
        train_file: str,
        val_file: str,
        test_file: str,
        predictions_file: str,
        checkpoint_dir: str,
        tmp_dir: str,
    ): ...

    @abstractmethod
    def _fit(self) -> str: ...

    @abstractmethod
    def _predict(self) -> str: ...

    @abstractmethod
    def _status(self, job_id: str) -> "JobState": ...

    @abstractmethod
    def _shutdown(self): ...


@rpyc.service
class RunnerService(_RunnerService, rpyc.Service):

    def __init__(self, runner_cls: Type["Runner"]) -> None:
        super().__init__()

        self._executor = ProcessPoolExecutor(max_workers=1)
        self._jobs: dict[str, Future[None]] = {}
        self._runner_cls = runner_cls

    def run(self):
        parser = ArgumentParser()
        parser.add_argument("key_pth", type=Path)
        parser.add_argument("cert_pth", type=Path)

        args = parser.parse_args()

        server = RunnerServer(args.key_pth, args.cert_pth, self)
        address = server.get_address()
        print(f"{address[0]} {address[1]}")
        server.start()

    def _submit_job(self, job: Callable[[], None]):
        job_id = str(uuid4())
        fut = self._executor.submit(job)
        self._jobs[job_id] = fut
        return job_id

    @rpyc.exposed
    def _config(
        self,
        algorithm_name: str,
        algorithm_config: str,
        dataset_name: str,
        train_file: str,
        val_file: str,
        test_file: str,
        predictions_file: str,
        checkpoint_dir: str,
        tmp_dir: str,
    ):
        self._runner = self._runner_cls(
            algorithm_name,
            json.loads(algorithm_config),
            dataset_name,
            Path(train_file),
            Path(val_file),
            Path(test_file),
            Path(predictions_file),
            Path(checkpoint_dir),
            Path(tmp_dir),
        )

    # TODO: Stopping time
    # TODO: Preparing files somewhere? Adapter code in each runner impl?
    @rpyc.exposed
    def _fit(self):
        return self._submit_job(self._runner._fit_job)

    @rpyc.exposed
    def _predict(self):
        return self._submit_job(self._runner._predict_job)

    @rpyc.exposed
    def _status(self, job_id: str):
        fut = self._jobs.get(job_id)
        if fut is None:
            return JobState.INVALID_ID

        if fut.cancelled():
            return JobState.CANCELLED

        if fut.running():
            return JobState.RUNNING

        if fut.done():
            exc = fut.exception()
            if exc is None:
                return JobState.FINISHED
            else:
                raise exc

        return JobState.PENDING

    @rpyc.exposed
    def _shutdown(self):
        self._executor.shutdown(cancel_futures=True)


@dataclass
class Runner(ABC):
    algorithm_name: str
    algorithm_config: dict[str, Any]
    dataset_name: str
    train_file: Path
    val_file: Path
    test_file: Path
    predictions_file: Path
    checkpoint_dir: Path
    tmp_dir: Path

    def _fit_job(self):
        self.init_runner()

        start = time()
        self.setup_fit()
        setup_end = time()
        self.fit()
        fit_end = time()
        self.post_fit()
        end = time()

    def _predict_job(self):
        self.init_runner()

        start = time()
        self.setup_predict()
        setup_end = time()

        predictions = self.predict()
        self.predictions_file.write_text(json.dumps(predictions))

        post_predict_start = time()
        self.post_predict()
        post_predict_end = time()

    def init_runner(self): ...

    def setup_fit(self): ...

    @abstractmethod
    def fit(self): ...

    def post_fit(self): ...

    def setup_predict(self): ...

    @abstractmethod
    def predict(self) -> Dict[Any, Any]: ...

    def post_predict(self): ...


class RunnerServer:
    def __init__(
        self,
        key_pth: Path,
        cert_pth: Path,
        service: RunnerService,
    ) -> None:
        auth = SSLAuthenticator(key_pth, cert_pth)

        self._server = ThreadedServer(service, authenticator=auth)

    def get_address(self):
        host = socket.gethostbyname(socket.gethostname())
        return host, self._server.port

    def start(self):
        self._server.start()


class JobState(IntEnum):
    PENDING = 1
    RUNNING = 2
    FINISHED = 3
    CANCELLED = 4
    INVALID_ID = 5
