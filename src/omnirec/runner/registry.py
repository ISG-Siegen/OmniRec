import sys
from pathlib import Path

import omnirec_runner
from omnirec_runner.runner import RunnerInfo

from omnirec.util import util

logger = util._root_logger.getChild("runner_registry")

_RUNNER_REGISTRY: dict[str, RunnerInfo] = {}


def register_runner(name: str, info: RunnerInfo):
    if name in _RUNNER_REGISTRY:
        logger.critical(
            f"A runner with the name {name} is already registered. Choose a different one!"
        )
        sys.exit(1)

    _RUNNER_REGISTRY[name] = info
    logger.debug(f"Runner {name} registered")


def _register_default_runners():
    runner_dir = Path(omnirec_runner.__file__).parent.resolve()

    # TODO: Add other runner:
    # TODO: Maybe move this to a config file or smth and dont hard code
    register_runner(
        "LensKit",
        RunnerInfo(
            runner_dir / "lenskit_runner.py",
            [
                "PopScorer",
                "ItemKNNScorer",
                "UserKNNScorer",
                "ImplicitMFScorer",
                "BiasedMFScorer",
                "FunkSVDScorer",
            ],
            "3.11",
            ["lenskit==2025.2.0", "binpickle", "numba"],
        ),
    )

    register_runner(
        "RecBole",
        RunnerInfo(
            runner_dir / "recbole_runner.py",
            [
                "Pop",
                "ItemKNN",
                "BPR",
                "NeuMF",
                "ConvNCF",
                "DMF",
                "FISM",
                "NAIS",
                "SpectralCF",
                "GCMC",
                "NGCF",
                "LightGCN",
                "DGCF",
                "LINE",
                "MultiVAE",
                "MultiDAE",
                "MacridVAE",
                "CDAE",
                "ENMF",
                "NNCF",
                "RecVAE",
                "EASE",
                "SLIMElastic",
                "SGL",
                "ADMMSLIM",
                "NCEPLRec",
                "SimpleX",
                "NCL",
                "Random",
                "DiffRec",
                "LDiffRec",
            ],
            "3.11",
            [
                "setuptools<82",
                "recbole==1.2.1",
                "numpy==1.26.4",
                "torch==2.5.1",
            ],
        ),
    )

    register_runner(
        "RecPack",
        RunnerInfo(
            runner_dir / "recpack_runner.py",
            ["SVD", "NMF", "ItemKNN"],
            "3.12",
            ["recpack==0.3.6"],
        ),
    )
    register_runner(
        "Elliot",
        RunnerInfo(
            runner_dir / "elliot_runner.py",
            [
                "ItemKNN",
                "UserKNN",
                "AMF",
                "SlopeOne",
                "MultiDAE",
                "MultiVAE",
                "LightGCN",
                "NGCF",
                "MostPop",
                "BPRMF",
                "BPRMF_batch",
                "FM",
                "FunkSVD",
                "NonNegMF",
                "PureSVD",
                "SVDpp",
                "WRMF",
                "ConvMF",
                "DeepFM",
                "DMF",
                "GMF",
                "ItemAutoRec",
                "NeuMF",
                "UserAutoRec",
            ],
            "3.8",
            [
                # patched elliot version
                "git+https://github.com/moritz-baumgart/elliot.git",
            ],
        ),
    )


_register_default_runners()
