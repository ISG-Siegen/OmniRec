import importlib
import sys
from http import HTTPStatus
from pathlib import Path
from typing import Optional

import requests
from pandas import DataFrame
from tqdm import tqdm

from recsyslib.data_loaders.base import Loader
from recsyslib.util import util
from recsyslib.util.util import _DATA_DIR, is_valid_url, verify_checksum

logger = util._root_logger.getChild("registry")

_DATA_LOADERS: dict[str, type[Loader]] = {}


# TODO: Switch some log messages from info to debug; we dont need that much clutter

# TODO: DOCS


def _add_loader(name: str, cls: type):
    if name in _DATA_LOADERS:
        logger.error(
            f'Failed to register data loader "{cls.__name__}" under name "{name}".\nThere is already another loader registered under this name!'
        )
        return
    _DATA_LOADERS[name] = cls


def register_dataloader(names: str | list[str], cls: type[Loader]):
    """Register a data loader class under one or multiple names.

    Args:
        names (str | list[str]): Name(s) to register the loader under.
        cls (type[Loader]): Loader class to register. Must inherit from the common `Loader` base class.
    """
    if type(names) is list:
        for n in names:
            _add_loader(n, cls)
    elif type(names) is str:
        _add_loader(names, cls)


def list_datasets():
    """List all registered dataset names.

    Returns:
        list[str]: A list of all registered dataset names.
    """
    return list(_DATA_LOADERS.keys())


def _loader(names: str | list[str]):
    """
    Internal decorator to simplify registering loader classes.

    Usage:
    ------
    Used only internally to avoid repetitive registration calls.
    """

    def decorator(cls: type):
        register_dataloader(names, cls)
        return cls

    return decorator


for p in Path(__file__).parent.glob("*.py"):
    module = p.stem
    if module != "__init__":
        importlib.import_module(f"recsyslib.data_loaders.{module}")


def _get_loader(name: str) -> Optional[type[Loader]]:
    return _DATA_LOADERS.get(name)


def _run_loader(
    name: str, force_download=False, raw_dir: Optional[Path] = None
) -> DataFrame:
    loader = _get_loader(name)
    if not loader:
        logger.critical(
            f"Loader '{name}' was not registered. Did you register it first? "
            "Also, make sure the loader name is correct (case-sensitive) if you intended to use one "
            "of the internally implemented loaders."
        )
        sys.exit(1)

    info = loader.info(name)

    if isinstance(info.download_urls, list):
        urls = info.download_urls
    elif isinstance(info.download_urls, str):
        urls = [info.download_urls]
    else:
        urls: list[str] = []

    success = False

    if not raw_dir:
        raw_dir = _DATA_DIR / "raw" / name
    raw_dir.mkdir(exist_ok=True, parents=True)
    for idx, u in enumerate(urls, 1):
        save_pth = (raw_dir / Path(u).name).resolve()
        if save_pth.exists() and not force_download:
            if verify_checksum(save_pth, info.checksum):
                logger.info(f"Dataset {name} already exists, skipping download...")
                success = True
                break
            else:
                logger.warning(
                    "Trying to redownload existing dataset, because checksum verification failed..."
                )
                save_pth.unlink()
        elif save_pth.exists() and force_download:
            logger.info(
                f"Dataset {name} already exists, but {force_download=}. Trying redownload.."
            )
            save_pth.unlink()
        logger.info(f"Trying to download {name} from {u}...")
        if not is_valid_url(u):
            logger.warning(f"Invalid URL: {u}. Skipping...")
            continue
        try:
            res = requests.get(u, stream=True)
        except Exception as e:
            logger.warning(f"Failed to make request to {u}: {e}. Skipping...")
            continue

        if res.status_code != 200:
            logger.warning(
                f"Request to {u} failed: Error {res.status_code}: {HTTPStatus(res.status_code).phrase}. Skipping..."
            )
            continue
        total_size = int(res.headers.get("content-length", 0))
        with (
            open(save_pth, "wb") as save_f,
            tqdm(total=total_size, unit_scale=True) as bar,
        ):
            for chunk in res.iter_content(
                chunk_size=1024 * 1024
            ):  # TODO: Figure out best chunksize
                if chunk:
                    save_f.write(chunk)
                    bar.update(len(chunk))

        if not verify_checksum(save_pth, info.checksum):
            if idx == len(urls):
                logger.critical(
                    f"Download failed for {name}. Checksum verification failed and no further download links available! Exiting..."
                )
                sys.exit()
            logger.info(
                "Continuing with next download link because of checksum verification fail..."
            )
            continue

        success = True
        break

    if not success:
        logger.critical(
            f"Download failed for {name}. None of the provides download urls were successful! Exiting..."
        )
        sys.exit(1)

    logger.info(f"Loading {name}...")
    try:
        data = loader.load(raw_dir, name)
        logger.info(f"Successfully loaded {name}!")
        return data
    except Exception as e:
        raise NotImplementedError(e)
