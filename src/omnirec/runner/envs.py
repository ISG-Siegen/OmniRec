import os
import subprocess
import sys
from os import PathLike
from pathlib import Path
from subprocess import Popen
from typing import Optional

from omnirec.util import util
from omnirec.util.util import _DATA_DIR

_ENVS_DIR = _DATA_DIR / "envs"

logger = util._root_logger.getChild("envs")


class Env:
    def __init__(
        self,
        name: str,
        python_version: str,
        packages: list[str],
        build_packages: list[str] = [],
        path: Optional[PathLike | str] = None,
    ) -> None:
        self._name = name
        self._python_version = python_version
        local_lib_pth = (
            Path(__file__).parent.parent.parent.parent / "packages" / "omnirec_runner"
        )
        if local_lib_pth.exists():
            self._packages = [str(local_lib_pth.resolve())] + packages
        else:
            # TODO: Change package name once we have a name
            self._packages = ["omnirec-runner"] + packages
        if build_packages:
            self._no_isolate_build = True
        else:
            self._no_isolate_build = False
        self._build_packages = ["hatchling"] + build_packages
        if path:
            self._path = Path(path)
        else:
            self._path = _ENVS_DIR / name

    def create(self):
        # TODO: Creating env shows up every time, this might be misleading
        logger.info(f"Creating env '{self._name}' at {self._path}")
        proc = self._run(["uv", "venv", "-p", self._python_version, self._path])
        self._handle_proc(proc)

        if self._no_isolate_build:
            logger.debug("Using non isolated build environment!")
            logger.debug("Installing build packages...")
            proc = self._run(
                [
                    "uv",
                    "pip",
                    "install",
                    "--no-build-isolation",
                    "-p",
                    str(self.py_path),
                    *self._build_packages,
                ]
            )

        logger.info("Installing packages...")
        cmd = ["uv", "pip", "install"]
        if self._no_isolate_build:
            cmd.append("--no-build-isolation")
        cmd.extend(["-p", str(self.py_path), *self._packages])

        proc = self._run(cmd)
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
