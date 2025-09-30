from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace


class CmdBase(ABC):
    @abstractmethod
    def add_args(self, parser: ArgumentParser) -> None: ...

    @abstractmethod
    def run(self, args: Namespace) -> None: ...
