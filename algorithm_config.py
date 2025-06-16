import itertools


def retrieve_configurations(algorithm_name):
    configuration_space = {}
    if algorithm_name == "Pop":
        configuration_space["epochs"] = [1]
    elif algorithm_name == "ItemKNN":
        configuration_space["epochs"] = [1]
        configuration_space["k"] = [100]
    elif algorithm_name == "BPR":
        configuration_space["embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "NeuMF":
        configuration_space["mf_embedding_size"] = [64]
        configuration_space["mlp_embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "ConvNCF":
        configuration_space["embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "DMF":
        configuration_space["user_embedding_size"] = [64]
        configuration_space["item_embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "FISM":
        configuration_space["embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
        configuration_space["split_to"] = [20]
    elif algorithm_name == "NAIS":
        configuration_space["embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
        configuration_space["split_to"] = [20]
    elif algorithm_name == "SpectralCF":
        configuration_space["embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "GCMC":
        configuration_space["embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "NGCF":
        configuration_space["embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "LightGCN":
        configuration_space["embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "DGCF":
        configuration_space["embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "LINE":
        configuration_space["embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "MultiVAE":
        configuration_space["latent_dimension"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "MultiDAE":
        configuration_space["latent_dimension"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "MacridVAE":
        configuration_space["embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "CDAE":
        configuration_space["embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "ENMF":
        configuration_space["embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "NNCF":
        configuration_space["ui_embedding_size"] = [64]
        configuration_space["neigh_embedding_size"] = [64]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "RecVAE":
        configuration_space["latent_dimension"] = [200]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "EASE":
        configuration_space["epochs"] = [1]
        configuration_space["reg_weight"] = [250]
    elif algorithm_name == "SLIMElastic":
        configuration_space["epochs"] = [1]
        configuration_space["alpha"] = [0.2]
    elif algorithm_name == "SGL":
        configuration_space["embedding_size"] = [64]
    elif algorithm_name == "ADMMSLIM":
        configuration_space["epochs"] = [1]
        configuration_space["k"] = [25]
        configuration_space["alpha"] = [0.5]
    elif algorithm_name == "NCEPLRec":
        configuration_space["epochs"] = [1]
        configuration_space["rank"] = [450]
    elif algorithm_name == "SimpleX":
        configuration_space["embedding_size"] = [64]
    elif algorithm_name == "NCL":
        configuration_space["embedding_size"] = [64]
        configuration_space["num_clusters"] = [100]
    elif algorithm_name == "Random":
        configuration_space["epochs"] = [1]
    elif algorithm_name == "DiffRec":
        configuration_space["steps"] = [5]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "LDiffRec":
        configuration_space["steps"] = [5]
        configuration_space["learning_rate"] = [0.01]
    elif algorithm_name == "PopScore":
        configuration_space["score_method"] = ["quantile"]
    elif algorithm_name == "ItemItem":
        configuration_space["nnbrs"] = [100]
        configuration_space["min_nbrs"] = [1]
        configuration_space["min_sim"] = [1e-6]
    elif algorithm_name == "UserUser":
        configuration_space["nnbrs"] = [100]
        configuration_space["min_nbrs"] = [1]
        configuration_space["min_sim"] = [1e-6]
    elif algorithm_name == "ImplicitMF":
        configuration_space["features"] = [50]
        configuration_space["iterations"] = [20]
        configuration_space["reg"] = [0.01]
    elif algorithm_name == "SVD":
        configuration_space["num_components"] = [100]
    elif algorithm_name == "NMF":
        configuration_space["num_components"] = [100]
        configuration_space["alpha"] = [0.0]
    elif algorithm_name == "ItemKNNRP":
        configuration_space["K"] = [100]
        configuration_space["similarity"] = ["cosine"]
    elif algorithm_name == "BiasedMF":
        configuration_space["features"] = [100]
        configuration_space["iterations"] = [20]
        configuration_space["reg"] = [0.1]
    elif algorithm_name == "FunkSVD":
        configuration_space["features"] = [100]
        configuration_space["iterations"] = [100]
        configuration_space["reg"] = [0.015]
    elif algorithm_name == "ItemKNNEL":
        configuration_space["neighbors"] = [100]
        configuration_space["similarity"] = ["cosine"]
        configuration_space["implicit"] = [True]
    elif algorithm_name == "UserKNNEL":
        configuration_space["neighbors"] = [100]
        configuration_space["similarity"] = ["cosine"]
        configuration_space["implicit"] = [True]
    elif algorithm_name == "AMF":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
    elif algorithm_name == "SlopeOne":
        configuration_space["epochs"] = [1]
    elif algorithm_name == "MultiDAEEL":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
    elif algorithm_name == "MultiVAEEL":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
    elif algorithm_name == "LightGCNEL":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
    elif algorithm_name == "NGCFEL":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
    elif algorithm_name == "MostPop":
        configuration_space["epochs"] = [1]
    elif algorithm_name == "BPRMF":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
        configuration_space["factors"] = [100]
    elif algorithm_name == "BPRMF_batch":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
        configuration_space["factors"] = [100]
    elif algorithm_name == "FM":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
        configuration_space["factors"] = [100]
    elif algorithm_name == "FunkSVDEL":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
        configuration_space["factors"] = [100]
    elif algorithm_name == "NonNegMF":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
        configuration_space["factors"] = [100]
    elif algorithm_name == "PureSVD":
        configuration_space["factors"] = [100]
    elif algorithm_name == "SVDpp":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
        configuration_space["factors"] = [100]
    elif algorithm_name == "WRMF":
        configuration_space["epochs"] = [200]
        configuration_space["factors"] = [100]
    elif algorithm_name == "ConvMF":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
        configuration_space["embedding_size"] = [64]
    elif algorithm_name == "DeepFM":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
        configuration_space["factors"] = [100]
    elif algorithm_name == "DMFEL":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
    elif algorithm_name == "GMF":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
    elif algorithm_name == "ItemAutoRec":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
    elif algorithm_name == "NeuMFEL":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
    elif algorithm_name == "UserAutoRec":
        configuration_space["epochs"] = [200]
        configuration_space["lr"] = [0.01]
    else:
        pass

    experiments = [dict(zip(configuration_space.keys(), v)) for v in itertools.product(*configuration_space.values())]
    return experiments
