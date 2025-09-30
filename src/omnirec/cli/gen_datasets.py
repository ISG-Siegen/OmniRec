import importlib
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Iterable

from omnirec.cli.cmd_base import CmdBase
from omnirec.data_loaders.registry import list_datasets
from omnirec.util import util

logger = util._root_logger.getChild("gen-datasets")


def file_template(enum_entries: Iterable[str]):
    return f"""from enum import StrEnum, auto


class DataSet(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> str:
        return name  # keep exact case for using auto

{"\n".join(enum_entries)}
"""


def enum_entry_template(name: str) -> str:
    return f"    {name} = auto()"


class GenDatasets(CmdBase):
    def add_args(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "-o",
            dest="output_file",
            help="Output file. Defaults to internal library file.",
        )

    def run(self, args: Namespace) -> None:
        logger.info("Generating dataset stubs...")
        dl_dir = Path(__file__).parent.parent / "data_loaders"
        for p in dl_dir.glob("*.py"):
            module = p.stem
            if module in ["__init__", "base", "registry", "datasets"]:
                importlib.import_module(f"omnirec.data_loaders.{module}")

        datasets = list_datasets()
        logger.info(f"Found {len(datasets)} dataset(s)!")
        enum_entries = map(enum_entry_template, datasets)
        code = file_template(enum_entries)

        if args.output_file:
            output_file = Path(args.output_file)
        else:
            output_file = dl_dir / "datasets.py"

        logger.info(f'Writing to file "{output_file}"...')
        output_file.write_text(code)
        logger.info("Done.")
