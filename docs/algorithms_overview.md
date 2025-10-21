# Algorithm Overview

The framework integrates algorithms from multiple recommendation system libraries through unified runner interfaces. Use the algorithm identifiers with the [`ExperimentPlan`](API_references.md#omnirec.runner.plan.ExperimentPlan) to configure experiments. Here is the comprehensive list of all available algorithms:

## LensKit Algorithms

LensKit provides traditional collaborative filtering algorithms optimized for research reproducibility.

| Algorithm Name        | Type                    | Feedback   | Description                                    |
|-----------------------|-------------------------|------------|------------------------------------------------|
| LensKit.PopScorer     | Baseline                | Both       | Popularity-based scorer                        |
| LensKit.ItemKNNScorer | Neighborhood            | Both       | Item-based k-nearest neighbors                 |
| LensKit.UserKNNScorer | Neighborhood            | Both       | User-based k-nearest neighbors                 |
| LensKit.ImplicitMFScorer | Matrix Factorization | Implicit   | Implicit feedback matrix factorization (ALS)   |
| LensKit.BiasedMFScorer | Matrix Factorization  | Explicit   | Biased matrix factorization                    |
| LensKit.FunkSVDScorer | Matrix Factorization   | Explicit   | FunkSVD matrix factorization                   |

## RecPack Algorithms

RecPack provides efficient implementations of collaborative filtering algorithms with a focus on scalability and performance.

| Algorithm Name        | Type                    | Feedback   | Description                                    |
|-----------------------|-------------------------|------------|------------------------------------------------|
| RecPack.SVD           | Matrix Factorization    | Explicit   | Singular Value Decomposition                    |
| RecPack.NMF           | Matrix Factorization    | Explicit   | Non-negative Matrix Factorization               |
| RecPack.ItemKNN       | Neighborhood            | Both       | Item-based k-nearest neighbors                 |

## Elliot Algorithms

Elliot provides a comprehensive framework for reproducible recommender systems evaluation with implementations of state-of-the-art algorithms.

### Baseline and Neighborhood Methods

| Algorithm Name       | Type                    | Feedback   | Description                                    |
|----------------------|-------------------------|------------|------------------------------------------------|
| Elliot.MostPop       | Baseline                | Both       | Most popular items baseline                     |
| Elliot.ItemKNN       | Neighborhood            | Both       | Item-based k-nearest neighbors                 |
| Elliot.UserKNN       | Neighborhood            | Both       | User-based k-nearest neighbors                 |
| Elliot.SlopeOne      | Slope One               | Explicit   | Slope One collaborative filtering              |

### Matrix Factorization and Factorization Machines

| Algorithm Name       | Type                    | Feedback   | Description                                    |
|----------------------|-------------------------|------------|------------------------------------------------|
| Elliot.AMF           | Matrix Factorization    | Explicit   | Alternating Matrix Factorization                |
| Elliot.BPRMF         | Matrix Factorization    | Implicit   | Bayesian Personalized Ranking Matrix Factorization |
| Elliot.BPRMF_batch   | Matrix Factorization    | Implicit   | BPRMF with batch processing                     |
| Elliot.FM            | Factorization Machine   | Explicit   | Factorization Machine                           |
| Elliot.FunkSVD       | Matrix Factorization    | Explicit   | FunkSVD matrix factorization                   |
| Elliot.NonNegMF      | Matrix Factorization    | Explicit   | Non-negative Matrix Factorization               |
| Elliot.PureSVD       | Matrix Factorization    | Explicit   | Pure SVD                                       |
| Elliot.SVDpp         | Matrix Factorization    | Explicit   | SVD++                                          |
| Elliot.WRMF          | Matrix Factorization    | Implicit   | Weighted Regularized Matrix Factorization       |
| Elliot.ConvMF        | Matrix Factorization    | Explicit   | Convolutional Matrix Factorization              |
| Elliot.DeepFM        | Deep Learning           | Explicit   | Deep Factorization Machine                      |
| Elliot.DMF           | Matrix Factorization    | Explicit   | Deep Matrix Factorization                       |
| Elliot.GMF           | Matrix Factorization    | Explicit   | Generalized Matrix Factorization                |
| Elliot.NeuMF         | Deep Learning           | Implicit   | Neural Matrix Factorization                     |

### Autoencoder-Based Methods

| Algorithm Name       | Type                    | Feedback   | Description                                    |
|----------------------|-------------------------|------------|------------------------------------------------|
| Elliot.MultiDAE      | Deep Learning           | Implicit   | Multi-layer Denoising Autoencoder              |
| Elliot.MultiVAE      | Deep Learning           | Implicit   | Multi-layer Variational Autoencoder            |
| Elliot.ItemAutoRec   | Deep Learning           | Explicit   | Item-based Autoencoder                          |
| Elliot.UserAutoRec   | Deep Learning           | Explicit   | User-based Autoencoder                          |

### Graph-Based Methods

| Algorithm Name       | Type                    | Feedback   | Description                                    |
|----------------------|-------------------------|------------|------------------------------------------------|
| Elliot.LightGCN      | Graph Neural Network    | Implicit   | Light Graph Convolutional Network               |
| Elliot.NGCF          | Graph Neural Network    | Implicit   | Neural Graph Collaborative Filtering            |

## Using Algorithms in Experiments

## RecBole Algorithms

RecBole provides a comprehensive collection of modern recommendation algorithms including deep learning and graph-based methods.

### Baseline and Neighborhood Methods

| Algorithm Name       | Type                    | Feedback   | Description                                    |
|----------------------|-------------------------|------------|------------------------------------------------|
| RecBole.Pop          | Baseline                | Both       | Popularity-based recommender                   |
| RecBole.ItemKNN      | Neighborhood            | Both       | Item-based k-nearest neighbors                 |
| RecBole.Random       | Baseline                | Both       | Random recommendation baseline                 |

### Matrix Factorization

| Algorithm Name       | Type                    | Feedback   | Description                                    |
|----------------------|-------------------------|------------|------------------------------------------------|
| RecBole.BPR          | Matrix Factorization    | Implicit   | Bayesian Personalized Ranking                  |
| RecBole.FISM         | Matrix Factorization    | Implicit   | Factored Item Similarity Models                |
| RecBole.NAIS         | Matrix Factorization    | Implicit   | Neural Attentive Item Similarity               |
| RecBole.DMF          | Matrix Factorization    | Explicit   | Deep Matrix Factorization                      |
| RecBole.ENMF         | Matrix Factorization    | Implicit   | Efficient Neural Matrix Factorization          |
| RecBole.NNCF         | Matrix Factorization    | Implicit   | Neural Network Collaborative Filtering         |

### Deep Learning Methods

| Algorithm Name       | Type                    | Feedback   | Description                                    |
|----------------------|-------------------------|------------|------------------------------------------------|
| RecBole.NeuMF        | Deep Learning           | Implicit   | Neural Matrix Factorization                    |
| RecBole.ConvNCF      | Deep Learning           | Implicit   | Convolutional Neural Collaborative Filtering   |
| RecBole.CDAE         | Deep Learning           | Implicit   | Collaborative Denoising Auto-Encoder           |
| RecBole.MultiVAE     | Deep Learning           | Implicit   | Variational Autoencoders for Collaborative Filtering |
| RecBole.MultiDAE     | Deep Learning           | Implicit   | Denoising Autoencoders for Collaborative Filtering |
| RecBole.MacridVAE    | Deep Learning           | Implicit   | Macroscopic and Microscopic Variational Autoencoder |
| RecBole.RecVAE       | Deep Learning           | Implicit   | Variational Autoencoders for Recommendations   |
| RecBole.DiffRec      | Deep Learning           | Implicit   | Diffusion Recommender Model                    |
| RecBole.LDiffRec     | Deep Learning           | Implicit   | Latent Diffusion Recommender Model             |

### Graph-Based Methods

| Algorithm Name       | Type                    | Feedback   | Description                                    |
|----------------------|-------------------------|------------|------------------------------------------------|
| RecBole.SpectralCF   | Graph Neural Network    | Implicit   | Spectral Collaborative Filtering               |
| RecBole.GCMC         | Graph Neural Network    | Explicit   | Graph Convolutional Matrix Completion          |
| RecBole.NGCF         | Graph Neural Network    | Implicit   | Neural Graph Collaborative Filtering           |
| RecBole.LightGCN     | Graph Neural Network    | Implicit   | Light Graph Convolutional Network              |
| RecBole.DGCF         | Graph Neural Network    | Implicit   | Disentangled Graph Collaborative Filtering     |
| RecBole.SGL          | Graph Neural Network    | Implicit   | Self-supervised Graph Learning                 |
| RecBole.NCL          | Graph Neural Network    | Implicit   | Neighborhood-enriched Contrastive Learning     |
| RecBole.LINE         | Graph Embedding         | Implicit   | Large-scale Information Network Embedding      |

### Linear and Optimization-Based Methods

| Algorithm Name       | Type                    | Feedback   | Description                                    |
|----------------------|-------------------------|------------|------------------------------------------------|
| RecBole.EASE         | Linear                  | Implicit   | Embarrassingly Shallow Autoencoders            |
| RecBole.SLIMElastic  | Linear                  | Implicit   | Sparse Linear Method with ElasticNet           |
| RecBole.ADMMSLIM     | Linear                  | Implicit   | ADMM SLIM for Top-N Recommendation             |
| RecBole.NCEPLRec     | Linear                  | Implicit   | Neighborhood-based Collaborative Filtering with Pairwise Learning |
| RecBole.SimpleX      | Linear                  | Implicit   | Simple and Effective Collaborative Filtering   |

## Using Algorithms in Experiments

Reference algorithms using the format `<Runner>.<Algorithm>` in your experiment plan:

```python
from omnirec.runner.plan import ExperimentPlan
from omnirec.runner.algos import LensKit, RecBole

# Create experiment plan
plan = ExperimentPlan("Algorithm-Comparison")

# Add LensKit algorithm
plan.add_algorithm(
    LensKit.ItemKNNScorer,
    {"max_nbrs": 20, "min_nbrs": 5}
)

# Add RecBole algorithm
plan.add_algorithm(
    RecBole.LightGCN,
    {"embedding_size": 64, "n_layers": 3}
)
```

See the [Algorithm Configuration](conf_algo.md) guide for detailed information on configuring algorithms and hyperparameters.

<!-- ## Algorithm Selection Guidelines

**For Explicit Feedback (ratings)**:
- Baseline: `LensKit.PopScorer`, `RecBole.Pop`
- Traditional: `LensKit.BiasedMFScorer`, `LensKit.FunkSVDScorer`
- Deep Learning: `RecBole.DMF`
- Graph-based: `RecBole.GCMC`

**For Implicit Feedback (clicks, views)**:
- Baseline: `RecBole.Pop`, `RecBole.Random`
- Neighborhood: `LensKit.ItemKNNScorer`, `RecBole.ItemKNN`
- Matrix Factorization: `LensKit.ImplicitMFScorer`, `RecBole.BPR`
- Linear: `RecBole.EASE`, `RecBole.SLIMElastic`
- Deep Learning: `RecBole.NeuMF`, `RecBole.MultiVAE`
- Graph-based: `RecBole.LightGCN`, `RecBole.NGCF`

**Performance Considerations**:
- Fast training: Neighborhood methods, linear methods (`EASE`, `SLIM`)
- Best accuracy: Graph neural networks (`LightGCN`, `NGCF`), deep learning methods
- Large datasets: Linear methods, graph-based methods with mini-batching
- Cold-start scenarios: Popularity-based methods, content-aware algorithms -->
