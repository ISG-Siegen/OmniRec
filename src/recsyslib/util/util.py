import hashlib
import logging
from pathlib import Path
from urllib.parse import urlparse

# TODO: Maybe we can switch to getLogger(__name__) everywhere instead of using this constant here
# TODO: Get log level from env and provide methods to set it
_LOGGER_NAME = "isg-rec-framework"
_logger = logging.getLogger(_LOGGER_NAME).getChild("util")

_RANDOM_STATE = 42

# TODO: Change path to a more accessible location
_DATA_DIR = Path(__file__).parent.parent.parent / "data"
_DATA_DIR.mkdir(exist_ok=True, parents=True)


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
