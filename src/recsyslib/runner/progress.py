import sys
from enum import IntEnum, auto
from pathlib import Path
from typing import Optional, Self

from pydantic import BaseModel

from recsyslib.util import util

logger = util._root_logger.getChild("progress")


class Phase(IntEnum):
    Fit = 0
    Predict = auto()
    Eval = auto()
    Done = auto()


class _Job(BaseModel):
    next_phase: Phase = Phase.Fit
    next_fold: Optional[int] = None


class _RunProgress(BaseModel):
    jobs: dict[str, _Job] = {}


class RunProgress:
    _progress: _RunProgress
    _progress_path: Path

    def save(self) -> None:
        logger.debug(f"Saving progress to {self._progress_path.resolve()}")
        self._progress_path.write_text(self._progress.model_dump_json(indent=4))

    @classmethod
    def load_or_create(
        cls, checkpoint_dir: Path, add_job: Optional[tuple[str, str]] = None
    ) -> Self:
        progress_path = checkpoint_dir / "progress.json"
        if progress_path.exists():
            p = _RunProgress.model_validate_json(progress_path.read_text())
        else:
            p = _RunProgress()

        c = cls()
        c._progress = p
        c._progress_path = progress_path

        if add_job:
            c.add_job(*add_job)

        c.save()
        return c

    def add_job(self, dataset_namehash: str, config_namehash: str) -> None:
        key = self.make_key(dataset_namehash, config_namehash)
        self._progress.jobs.setdefault(key, _Job())
        self.save()

    def get_job(self, dataset_namehash: str, config_namehash: str) -> _Job:
        return self._get_job_or_error(dataset_namehash, config_namehash)

    def get_next_phase(self, dataset_namehash: str, config_namehash: str) -> Phase:
        job = self._get_job_or_error(dataset_namehash, config_namehash)
        return job.next_phase

    def advance_phase(self, dataset_namehash: str, config_namehash: str) -> None:
        job = self._get_job_or_error(dataset_namehash, config_namehash)
        if job.next_phase == Phase.Done:
            logger.critical(f"Cannot advance last phase {job.next_phase}")
            sys.exit(1)
        job.next_phase = Phase(job.next_phase + 1)
        self.save()

    def reset_phase(self, dataset_namehash: str, config_namehash: str):
        job = self._get_job_or_error(dataset_namehash, config_namehash)
        job.next_phase = Phase.Fit
        self.save()

    def get_next_fold_or_init(self, dataset_namehash: str, config_namehash: str) -> int:
        job = self._get_job_or_error(dataset_namehash, config_namehash)
        if job.next_fold is None:
            job.next_fold = 0
            self.save()
            return 0

        return job.next_fold

    def advance_fold(self, dataset_namehash: str, config_namehash: str) -> None:
        job = self._get_job_or_error(dataset_namehash, config_namehash)
        if job.next_fold is None:
            logger.critical("Cannot advance fold if it is None")
            sys.exit(1)
        job.next_fold += 1
        self.save()

    @staticmethod
    def make_key(dataset_namehash: str, config_namehash: str) -> str:
        return f"{dataset_namehash}|{config_namehash}"

    def _get_job_or_error(self, dataset_namehash: str, config_namehash: str) -> _Job:
        key = self.make_key(dataset_namehash, config_namehash)
        try:
            return self._progress.jobs[key]
        except KeyError:
            logger.critical(f"No saved progress for {key=}")
            sys.exit(1)
