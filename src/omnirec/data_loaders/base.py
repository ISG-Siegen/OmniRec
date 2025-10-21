from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd


@dataclass
class DatasetInfo:
    """
    Metadata about a dataset.

    Attributes
    __________
    
    download_urls : Optional[Union[str, List[str]]]
        URL or list of URLs to download the dataset.
        If a list is provided, URLs are tried in order until one succeeds
        (skipping on checksum mismatch or HTTP errors).

    checksum : Optional[str]
        Optional SHA256 checksum to verify the downloaded file's integrity.
        If provided, the downloaded file will be hashed using SHA256 and compared
        to this value. Use e.g. `hashlib.sha256()` to compute the checksum in python:
    ```
    import hashlib
    hasher = hashlib.sha256()
    with open("ml-100k.zip", "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    print(hasher.hexdigest())
    ```
    """

    download_urls: Optional[str | list[str]] = None
    checksum: Optional[str] = None


class Loader(ABC):
    @staticmethod
    @abstractmethod
    def info(name: str) -> DatasetInfo:
        """Provide metadata information about the dataset identified by `name`.

        Args:
            name (str): The name under which the loader was registered. Different names may return different DatasetInfo
                implementations depending on the dataset. This is useful when multiple
                datasets share the same loading logic but have, for example, different
                download URLs or checksums.

        Returns:
            DatasetInfo: Metadata including download URLs and optional checksum for verification.
        """

    @staticmethod
    @abstractmethod
    def load(source_dir: Path, name: str) -> pd.DataFrame:
        """
        Loads dataset from the given directory into a `pd.DataFrame`.
        The DataFrame should have the standard columns:
        - user
        - item
        - rating
        - timestamp

        Args:
            source_dir (Path): The directory that contains the downloaded dataset files.
            name (str): The name under which the loader was registered. This allows selecting between different
                datasets that share the same loading logic but differ in structure or
                file naming.

        Returns:
            pd.DataFrame: Loaded dataset as a pd.DataFrame with expected columns.
        """
