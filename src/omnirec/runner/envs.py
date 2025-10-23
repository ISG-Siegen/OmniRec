import os
import subprocess
import sys
from os import PathLike
from pathlib import Path
from subprocess import Popen
from typing import Optional

from omnirec.util import util
from omnirec.util.util import get_data_dir

logger = util._root_logger.getChild("envs")


class Env:
    def __init__(
        self,
        name: str,
        python_version: str,
        *packages: str,
        path: Optional[PathLike | str] = None,
    ) -> None:
        self._name = name
        self._python_version = python_version
        local_lib_pth = (
            Path(__file__).parent.parent.parent.parent / "packages" / "omnirec_runner"
        )
        if local_lib_pth.exists():
            self._packages = (str(local_lib_pth.resolve()),) + packages
        else:
            self._packages = ("omnirec-runner",) + packages
        if path:
            self._path = Path(path)
        else:
            self._path = get_data_dir() / "envs" / name

    def create(self):
        # TODO: Creating env shows up every time, this might be misleading
        logger.info(f"Creating env '{self._name}' at {self._path}")
        proc = self._run(
            ["uv", "venv", "-p", self._python_version, self._path.resolve()]
        )
        self._handle_proc(proc)

        logger.info("Installing packages...")
        proc = self._run(
            ["uv", "pip", "install", "-p", self.py_path.resolve(), *self._packages]
        )
        self._handle_proc(proc)

        logger.info("Done.")

    @property
    def py_path(self):
        if os.name == "nt":
            return self._path / "Scripts/python.exe"
        else:
            return self._path / "bin/python"

    def _run(self, cmd: list):
        logger.debug(f'Running command "{" ".join(map(str, cmd))}"')
        return subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

    def _handle_proc(self, proc: Popen[str]):
        if proc.stdout is not None:
            for line in proc.stdout:
                logger.debug(f"uv proc: {line.rstrip('\n')}")

        logger.debug("Waiting for proc...")
        proc.wait()
        if proc.returncode != 0:
            logger.critical(f"Error while creating env '{self._name}'")
            sys.exit(1)
