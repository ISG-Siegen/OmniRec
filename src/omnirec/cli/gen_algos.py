from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Iterable

from omnirec.cli.cmd_base import CmdBase
from omnirec.runner.coordinator import _RUNNER_REGISTRY, Coordinator
from omnirec.util import util

logger = util._root_logger.getChild("gen-algos")


def code_template(cls_names: Iterable[str], enum_cls_code: Iterable[str]) -> str:
    code = """from enum import StrEnum
from typing import TypeAlias


"""
    code += "\n\n\n".join(enum_cls_code)
    code += f"\n\n\nAlgorithms: TypeAlias = {' | '.join(cls_names)}\n"
    return code


def enum_cls_template(name: str, enum_entries: Iterable[str]) -> str:
    return f"class {name}(StrEnum):\n{'\n'.join(enum_entries)}"


def enum_entry_template(runner_name: str, algo_name: str) -> str:
    return f'    {algo_name} = "{runner_name}.{algo_name}"'


class GenAlgos(CmdBase):
    def add_args(self, parser: ArgumentParser):
        parser.add_argument(
            "-o",
            dest="output_file",
            help="Output file. Defaults to internal library file.",
        )

    def run(self, args: Namespace):
        logger.info("Generating algorithm stubs...")

        # HACK: This is currently a bit whacky
        # Initialize a Coordinator so it registers the default runners
        Coordinator()

        enum_cls_names: list[str] = []
        enum_cls_code: list[str] = []
        algo_count = 0

        for runner_name, runner in _RUNNER_REGISTRY.items():
            enum_entries = [
                enum_entry_template(runner_name, algo) for algo in runner.algorithms
            ]
            enum_cls_names.append(runner_name)
            enum_cls_code.append(enum_cls_template(runner_name, enum_entries))
            algo_count += len(enum_entries)

        logger.info(
            f"Found {len(enum_cls_names)} runner(s) and {algo_count} algorithm(s)!"
        )

        code = code_template(enum_cls_names, enum_cls_code)

        if args.output_file:
            output_file = Path(args.output_file)
        else:
            runner_dir = Path(__file__).parent.parent / "runner"
            output_file = runner_dir / "algos.py"

        logger.info(f'Writing to file "{output_file}"...')
        output_file.write_text(code)
        logger.info("Done.")
