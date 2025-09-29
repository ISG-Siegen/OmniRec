from enum import StrEnum
from typing import TypeAlias


class LensKit(StrEnum):
    PopScorer = "LensKit.PopScorer"
    ItemKNNScorer = "LensKit.ItemKNNScorer"
    UserKNNScorer = "LensKit.UserKNNScorer"
    ImplicitMFScorer = "LensKit.ImplicitMFScorer"
    BiasedMFScorer = "LensKit.BiasedMFScorer"
    FunkSVDScorer = "LensKit.FunkSVDScorer"


class RecBole(StrEnum):
    Pop = "RecBole.Pop"
    ItemKNN = "RecBole.ItemKNN"
    BPR = "RecBole.BPR"
    NeuMF = "RecBole.NeuMF"
    ConvNCF = "RecBole.ConvNCF"
    DMF = "RecBole.DMF"
    FISM = "RecBole.FISM"
    NAIS = "RecBole.NAIS"
    SpectralCF = "RecBole.SpectralCF"
    GCMC = "RecBole.GCMC"
    NGCF = "RecBole.NGCF"
    LightGCN = "RecBole.LightGCN"
    DGCF = "RecBole.DGCF"
    LINE = "RecBole.LINE"
    MultiVAE = "RecBole.MultiVAE"
    MultiDAE = "RecBole.MultiDAE"
    MacridVAE = "RecBole.MacridVAE"
    CDAE = "RecBole.CDAE"
    ENMF = "RecBole.ENMF"
    NNCF = "RecBole.NNCF"
    RecVAE = "RecBole.RecVAE"
    EASE = "RecBole.EASE"
    SLIMElastic = "RecBole.SLIMElastic"
    SGL = "RecBole.SGL"
    ADMMSLIM = "RecBole.ADMMSLIM"
    NCEPLRec = "RecBole.NCEPLRec"
    SimpleX = "RecBole.SimpleX"
    NCL = "RecBole.NCL"
    Random = "RecBole.Random"
    DiffRec = "RecBole.DiffRec"
    LDiffRec = "RecBole.LDiffRec"


Algorithms: TypeAlias = LensKit | RecBole
