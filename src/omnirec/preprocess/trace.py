import getpass
import os
import platform
import re
import socket
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from functools import lru_cache
from importlib import metadata
from pprint import pformat
from typing import Any, Self

import psutil

from omnirec.types import CountSummary


def _run_command(command: list[str]) -> list[str]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=2,
        )
    except (OSError, subprocess.SubprocessError):
        return []

    if result.returncode != 0:
        return []

    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _unique_non_empty(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def _format_bytes(num_bytes: int) -> str:
    value = float(num_bytes)
    units = ("B", "KiB", "MiB", "GiB", "TiB")

    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} {unit}"
        value /= 1024

    return f"{num_bytes} B"


def _parse_size_to_bytes(value: str) -> int | None:
    match = re.fullmatch(
        r"\s*(\d+(?:\.\d+)?)\s*([KMGT]?i?B)\s*",
        value,
        flags=re.IGNORECASE,
    )
    if match is None:
        return None

    amount = float(match.group(1))
    unit = match.group(2).upper()
    unit_factors = {
        "B": 1,
        "KB": 1000,
        "MB": 1000**2,
        "GB": 1000**3,
        "TB": 1000**4,
        "KIB": 1024,
        "MIB": 1024**2,
        "GIB": 1024**3,
        "TIB": 1024**4,
    }
    factor = unit_factors.get(unit)
    if factor is None:
        return None

    return int(amount * factor)


@lru_cache(maxsize=1)
def _resolve_library_version() -> str:
    try:
        return metadata.version("omnirec")
    except metadata.PackageNotFoundError:
        return "unknown"


def _resolve_author() -> str:
    try:
        author = getpass.getuser()
    except OSError:
        author = ""

    return author or os.getenv("USER") or os.getenv("USERNAME") or "unknown"


def _resolve_hostname() -> str:
    return socket.gethostname() or "unknown"


@lru_cache(maxsize=1)
def _detect_cpu() -> str:
    for candidate in (
        platform.processor().strip(),
        platform.uname().processor.strip(),
        platform.machine().strip(),
    ):
        if candidate:
            return candidate
    return "unknown"


@lru_cache(maxsize=1)
def _detect_cpu_cores() -> int | None:
    return psutil.cpu_count(logical=True)


@lru_cache(maxsize=1)
def _detect_ram() -> int | None:
    try:
        return int(psutil.virtual_memory().total)
    except (AttributeError, ValueError, OSError):
        return None


@lru_cache(maxsize=1)
def _detect_gpu() -> str | None:
    gpu_names = _run_command(
        ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"]
    )
    if gpu_names:
        return ", ".join(_unique_non_empty(gpu_names))

    system = platform.system()
    if system == "Windows":
        gpu_names = _run_command(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name",
            ]
        )
        if gpu_names:
            return ", ".join(_unique_non_empty(gpu_names))
    elif system == "Darwin":
        chipset_models = [
            line.split(":", maxsplit=1)[1].strip()
            for line in _run_command(["system_profiler", "SPDisplaysDataType"])
            if "Chipset Model:" in line
        ]
        if chipset_models:
            return ", ".join(_unique_non_empty(chipset_models))
    elif system == "Linux":
        gpu_lines = [
            line
            for line in _run_command(["lspci"])
            if any(tag in line.lower() for tag in ("vga", "3d controller", "display"))
        ]
        if gpu_lines:
            parsed_gpu_names = [
                line.split(": ", maxsplit=2)[-1].strip() for line in gpu_lines
            ]
            return ", ".join(_unique_non_empty(parsed_gpu_names))

    return None


@lru_cache(maxsize=1)
def _detect_gpu_vram() -> tuple[int, ...] | None:
    gpu_memory = _run_command(
        ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"]
    )
    if gpu_memory:
        try:
            return tuple(int(mem) * 1024 * 1024 for mem in gpu_memory)
        except ValueError:
            pass

    system = platform.system()
    if system == "Windows":
        adapter_ram = _run_command(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty AdapterRAM",
            ]
        )
        if adapter_ram:
            try:
                return tuple(int(vram) for vram in adapter_ram)
            except ValueError:
                pass
    elif system == "Darwin":
        vram_lines = [
            line.split(":", maxsplit=1)[1].strip()
            for line in _run_command(["system_profiler", "SPDisplaysDataType"])
            if "VRAM" in line
        ]
        if vram_lines:
            parsed_vram = [
                parsed
                for line in vram_lines
                if (parsed := _parse_size_to_bytes(line)) is not None
            ]
            if parsed_vram:
                return tuple(parsed_vram)

    return None


@dataclass(frozen=True)
class SystemInfo:
    os: str
    cpu: str
    cpu_cores: int | None
    ram: int | None
    gpu: str | None
    gpu_vram: tuple[int, ...] | None
    python_version: str

    @classmethod
    @lru_cache(maxsize=1)
    def detect(cls) -> Self:
        return cls(
            os=platform.platform(),
            cpu=_detect_cpu(),
            cpu_cores=_detect_cpu_cores(),
            ram=_detect_ram(),
            gpu=_detect_gpu(),
            gpu_vram=_detect_gpu_vram(),
            python_version=platform.python_version(),
        )


@dataclass
class Trace:
    component: str
    params: dict[str, Any]
    executed_at: datetime
    runtime: float | None = None
    hostname: str = field(default_factory=_resolve_hostname)
    library_version: str = field(default_factory=_resolve_library_version)
    author: str = field(default_factory=_resolve_author)
    system_info: SystemInfo = field(default_factory=SystemInfo.detect)
    before_rows: CountSummary | None = None
    before_columns: CountSummary | None = None
    after_rows: CountSummary | None = None
    after_columns: CountSummary | None = None

    def __repr__(self) -> str:
        params_str = ", ".join(f"{k}={v!r}" for k, v in self.params.items())
        signature = (
            f"{self.component}({params_str})" if params_str else f"{self.component}()"
        )
        extras: list[str] = []

        if self.runtime is not None:
            extras.append(f"runtime={self.runtime:.4f}s")

        if extras:
            return f"{signature} [{', '.join(extras)}]"
        return signature

    @staticmethod
    def _append_field(
        lines: list[str], label: str, value: Any, indent_level: int = 1
    ) -> None:
        prefix = "  " * indent_level

        if value is None:
            rendered = "unknown"
        elif isinstance(value, datetime):
            rendered = value.isoformat()
        elif isinstance(value, (dict, list, tuple, set)):
            rendered = pformat(value, sort_dicts=False)
        else:
            rendered = str(value)

        rendered_lines = rendered.splitlines()
        if len(rendered_lines) == 1:
            lines.append(f"{prefix}{label}: {rendered_lines[0]}")
            return

        lines.append(f"{prefix}{label}:")
        lines.extend(f"{prefix}  {line}" for line in rendered_lines)

    @staticmethod
    def _format_vram(vram: tuple[int, ...] | None) -> str | None:
        if vram is None:
            return None
        if len(vram) == 1:
            return _format_bytes(vram[0])
        return ", ".join(_format_bytes(amount) for amount in vram)

    def format_details(self) -> str:
        lines = [f"Component: {self.component}"]

        self._append_field(lines, "Parameters", self.params)
        self._append_field(lines, "Executed at (UTC)", self.executed_at)
        self._append_field(
            lines,
            "Runtime",
            f"{self.runtime:.4f}s" if self.runtime is not None else None,
        )
        self._append_field(lines, "Hostname", self.hostname)
        self._append_field(lines, "OmniRec version", self.library_version)
        self._append_field(lines, "Author", self.author)

        lines.append("  System info:")
        self._append_field(lines, "OS", self.system_info.os, indent_level=2)
        self._append_field(lines, "CPU", self.system_info.cpu, indent_level=2)
        self._append_field(
            lines, "CPU cores (logical)", self.system_info.cpu_cores, indent_level=2
        )
        self._append_field(
            lines,
            "RAM",
            _format_bytes(self.system_info.ram)
            if self.system_info.ram is not None
            else None,
            indent_level=2,
        )
        self._append_field(lines, "GPU", self.system_info.gpu, indent_level=2)
        self._append_field(
            lines,
            "GPU VRAM",
            self._format_vram(self.system_info.gpu_vram),
            indent_level=2,
        )
        self._append_field(
            lines, "Python version", self.system_info.python_version, indent_level=2
        )

        lines.append("  Dataset shape:")
        lines.append("    Rows:")
        self._append_field(lines, "Before", self.before_rows, indent_level=3)
        self._append_field(lines, "After", self.after_rows, indent_level=3)
        lines.append("    Columns:")
        self._append_field(lines, "Before", self.before_columns, indent_level=3)
        self._append_field(lines, "After", self.after_columns, indent_level=3)

        return "\n".join(lines)

    __str__ = __repr__
