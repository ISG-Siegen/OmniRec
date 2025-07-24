import os
import subprocess
import sys
from os import PathLike
from pathlib import Path
from subprocess import CalledProcessError
from typing import Optional

from recsyslib import util
from recsyslib.util import _DATA_DIR

_ENVS_DIR = _DATA_DIR / "envs"

logger = util._logger.getChild("envs")


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
        self._packages = ("RPyC",) + packages
        if path:
            self._path = Path(path)
        else:
            self._path = _ENVS_DIR / name

    def create(self):
        try:
            logger.info(f"Creating env '{self._name}' at {self._path}")
            self._run(["uv", "venv", "-p", self._python_version, self._path])

            logger.info("Installing packages...")
            self._run(["uv", "pip", "install", "-p", self.py_path, *self._packages])

        except CalledProcessError as e:
            logger.critical(f"Error while creating env '{self._name}':")
            logger.critical(e)
            logger.critical(f"STDOUT: {e.stdout}")
            logger.critical(f"STDERR: {e.stderr}")

            sys.exit(1)

        logger.info("Done.")

    @property
    def py_path(self):
        if os.name == "nt":
            return self._path / "Scripts/python.exe"
        else:
            return self._path / "bin/python"

    def _run(self, cmd: list):
        return subprocess.run(
            cmd,
            capture_output=True,
            check=True,
            text=True,
        )
