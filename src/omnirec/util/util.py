import hashlib
import logging
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from rich.logging import RichHandler

# Lazy import to solve circular import
if TYPE_CHECKING:
    from omnirec.data_variants import SplitData

_LOGGER_NAME = "omnirec"
_root_logger = logging.getLogger(_LOGGER_NAME)
_logger = _root_logger.getChild("util")

logging.basicConfig(
    format="%(message)s", datefmt="[%Y/%m/%d %H:%M:%S]", handlers=[RichHandler()]
)

_RANDOM_STATE = 42

# TODO: Change path to a more accessible location
_DATA_DIR = Path(__file__).parent.parent.parent / "data"
_DATA_DIR.mkdir(exist_ok=True, parents=True)


def set_log_level(level: str):
    level = level.upper()
    if level in logging._nameToLevel:
        _root_logger.setLevel(level)
        _root_logger.debug("LOG LEVEL IS SET TO DEBUG")
    else:
        raise ValueError(f"Unknown log level: {level}")


def is_valid_url(url) -> bool:
    parsed = urlparse(url)
    return all([parsed.scheme in ("http", "https"), parsed.netloc])


# TODO: What chunk size to choose
def calculate_checksum(file_pth: Path, chunk_size=1024 * 1024) -> str:
    hash = hashlib.sha256()
    with open(file_pth, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash.update(chunk)
        return hash.hexdigest()


def verify_checksum(file_pth: Path, checksum: str | None) -> bool:
    if not checksum:
        _logger.warning("No checksum provided, skipping checksum verification...")
        return True
    else:
        _logger.info("Verifying checksum...")
        res = calculate_checksum(file_pth) == checksum
        if res:
            _logger.info("Checksum verified successfully!")
        else:
            _logger.warning("Checksum verification failed!")

        return res


def set_random_state(random_state: int) -> None:
    """Set the global random state for reproducibility.

    Args:
        random_state (int): The random state seed.
    """
    global _RANDOM_STATE
    _RANDOM_STATE = random_state


def get_random_state() -> int:
    """Get the global random state for reproducibility.

    Returns:
        int: The current random state seed.
    """
    return _RANDOM_STATE


# TODO: Doc
def splits_to_csv(files: tuple[Path, Path, Path], split_data: "SplitData"):
    for split_file, (_, data) in zip(files, split_data.iter_splits()):
        data.to_csv(split_file, index=False)
