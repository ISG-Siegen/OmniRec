from argparse import ArgumentParser

from omnirec.cli.cmd_base import CmdBase
from omnirec.cli.gen_algos import GenAlgos
from omnirec.cli.gen_datasets import GenDatasets


def main():
    # TODO: Set name and desc
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(title="sub-command", dest="cmd", required=True)

    cmds: dict[str, CmdBase] = {
        "gen-datasets": GenDatasets(),
        "gen-algos": GenAlgos(),
    }

    for name, cmd in cmds.items():
        cmd_parser = subparsers.add_parser(name)
        cmd.add_args(cmd_parser)

    args = parser.parse_args()
    cmds[args.cmd].run(args)


if __name__ == "__main__":
    main()
