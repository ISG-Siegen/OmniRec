# Algorithm Configuration

This section explains how to configure algorithms and hyperparameters for recommendation experiments. The experiment planning system provides a flexible approach to define algorithm configurations and automatically generate all hyperparameter combinations.

The [`ExperimentPlan`](API_references.md#omnirec.runner.plan.ExperimentPlan) class manages algorithm configurations and hyperparameter grids. It expands every combination you define, automating the execution of multiple algorithm variants with different hyperparameter settings.

## ExperimentPlan

The [`ExperimentPlan`](API_references.md#omnirec.runner.plan.ExperimentPlan) class serves as the central configuration for all algorithms in your experiments. Create a plan by optionally providing a name, then add algorithms with their hyperparameters:

```python
from omnirec.runner.plan import ExperimentPlan

# Create an experiment plan with optional name
plan = ExperimentPlan("MovieLens-Experiments")
```

The plan name helps organize checkpoints and logs when storing experiment results.

### Algorithm Identifiers

Algorithms are referenced using the format `<Runner>.<Algorithm>`. The framework provides enums in `omnirec.runner.algos` that expose all built-in algorithm names:

```python
from omnirec.runner.algos import LensKit, RecBole

# Access algorithm identifiers via enums
lenskit_algo = LensKit.ImplicitMFScorer  # "LensKit.ImplicitMFScorer"
recbole_algo = RecBole.LightGCN          # "RecBole.LightGCN"
```


### Adding Algorithms

Add algorithms to the plan using the [`add_algorithm`](API_references.md#omnirec.runner.plan.ExperimentPlan.add_algorithm) method. Provide the algorithm identifier and a dictionary of hyperparameters:

```python
from omnirec.runner.algos import LensKit

# Add algorithm with hyperparameters
plan.add_algorithm(
    LensKit.ItemKNNScorer,
    {
        "max_nbrs": 20,        # Fixed value
        "min_nbrs": 5,         # Fixed value
        "center": True         # Fixed value
    }
)
```

**Parameters:**

- `algorithm` (str | Enum): Algorithm identifier in format `<Runner>.<Algorithm>`
- `hyperparameters` (dict): Dictionary of hyperparameter names and values
  - Single values: Parameter is fixed across all runs
  - Lists: Parameter values for grid search (creates multiple runs)


**Hyperparameter Reference:**

Hyperparameter names and default values are defined by each algorithm's original library implementation. The framework passes your hyperparameter dictionary directly to the underlying algorithm, so refer to the respective library documentation for available parameters and their expected formats.

### Hyperparameter Grid Search

Provide lists of values for any hyperparameter to automatically generate a grid search. The framework creates separate runs for every combination:

```python
from omnirec.runner.algos import LensKit

# Grid search with multiple parameter values
plan.add_algorithm(
    LensKit.ItemKNNScorer,
    {
        "max_nbrs": [20, 40],      # Two values
        "min_nbrs": 5,             # Fixed value
        "center": [True, False]    # Two values
    }
)
```

This configuration generates four separate runs (2 × 2 combinations):

- `max_nbrs=20, min_nbrs=5, center=True`
- `max_nbrs=20, min_nbrs=5, center=False`
- `max_nbrs=40, min_nbrs=5, center=True`
- `max_nbrs=40, min_nbrs=5, center=False`

### Multiple Algorithms

Combine multiple algorithms from different runners in the same experiment plan:

```python
from omnirec.runner.algos import LensKit, RecBole

# Add LensKit algorithm
plan.add_algorithm(
    LensKit.ItemKNNScorer,
    {
        "max_nbrs": [20, 40],
        "min_nbrs": 5,
    }
)

# Add RecBole algorithm
plan.add_algorithm(
    RecBole.LightGCN,
    {
        "learning_rate": [0.001, 0.005],
        "embedding_size": 64,
    }
)
```

Each call to [`add_algorithm`](API_references.md#omnirec.runner.plan.ExperimentPlan.add_algorithm) appends a new algorithm configuration. Avoid using the same algorithm identifier multiple times unless you intend to overwrite the previous configuration.

### Updating Algorithms

Modify existing algorithm configurations using the [`update_algorithm`](API_references.md#omnirec.runner.plan.ExperimentPlan.update_algorithm) method:

```python
# Update previously added algorithm
plan.update_algorithm(
    LensKit.ItemKNNScorer,
    {
        "max_nbrs": [20, 40, 60],  # Add third value
        "min_sim": 0.01            # Add new parameter
    }
)
```

The update merges with the existing configuration, adding new parameters and updating existing ones.

## Running Experiments

Pass the configured plan to [`run_omnirec`](API_references.md#omnirec.util.run.run_omnirec) alongside your dataset and evaluator to execute all algorithm configurations:

```python
from omnirec import RecSysDataSet
from omnirec.data_loaders.datasets import DataSet
from omnirec.runner.evaluation import Evaluator
from omnirec.metrics.ranking import NDCG, Recall
from omnirec.preprocess.pipe import Pipe
from omnirec.preprocess.feedback_conversion import MakeImplicit
from omnirec.preprocess.split import UserHoldout
from omnirec.util.run import run_omnirec

# Load and preprocess dataset to implicit feedback
dataset = RecSysDataSet.use_dataloader(DataSet.MovieLens100K)
pipeline = Pipe(
    MakeImplicit(3),           # Convert to implicit feedback
    UserHoldout(0.15, 0.15)    # Split data
)
dataset = pipeline.process(dataset)

# Configure evaluator with ranking metrics (for implicit feedback)
evaluator = Evaluator(NDCG([10]), Recall([10]))

# Run all algorithm configurations
run_omnirec(dataset, plan, evaluator)
```

The framework executes every algorithm configuration in the plan, automatically managing:
- Model training and prediction
- Checkpoint storage under `./checkpoints/<dataset>/<algorithm>/`
- Metric evaluation via the evaluator
- Progress tracking and logging

### Multiple Datasets

Run the same experiment plan across multiple datasets by passing a list of datasets:

```python
# Load multiple datasets
datasets = [
    RecSysDataSet.use_dataloader(DataSet.MovieLens100K),
    RecSysDataSet.use_dataloader(DataSet.HetrecLastFM),
]

# Run all algorithms on all datasets
run_omnirec(datasets, plan, evaluator)
```

Each algorithm configuration in the plan is executed for every dataset. Results are organized separately by dataset in the checkpoint directory structure.

### Complete Example

```python
from omnirec import RecSysDataSet
from omnirec.data_loaders.datasets import DataSet
from omnirec.runner.plan import ExperimentPlan
from omnirec.runner.algos import LensKit, RecBole
from omnirec.runner.evaluation import Evaluator
from omnirec.metrics.ranking import NDCG, Recall
from omnirec.preprocess.pipe import Pipe
from omnirec.preprocess.feedback_conversion import MakeImplicit
from omnirec.preprocess.core_pruning import CorePruning
from omnirec.preprocess.split import UserHoldout
from omnirec.util.run import run_omnirec

# Load dataset and preprocess to implicit feedback
dataset = RecSysDataSet.use_dataloader(DataSet.MovieLens100K)
pipeline = Pipe(
    MakeImplicit(3),           # Convert to implicit (ratings >= 3)
    CorePruning(5),            # Keep 5-core users and items
    UserHoldout(0.15, 0.15)    # Split into train/val/test
)
dataset = pipeline.process(dataset)

# Create experiment plan
plan = ExperimentPlan("Comparison-Study")

# Add multiple algorithms with grid search
plan.add_algorithm(
    LensKit.ItemKNNScorer,
    {
        "max_nbrs": [20, 40],
        "min_nbrs": 5,
        "feedback": "implicit"  # Specify implicit feedback mode
    }
)

plan.add_algorithm(
    RecBole.LightGCN,
    {
        "learning_rate": [0.001, 0.005],
        "embedding_size": [32, 64],
        "n_layers": 3
    }
)

# Configure evaluation with ranking metrics (appropriate for implicit feedback)
evaluator = Evaluator(NDCG([5, 10]), Recall([5, 10]))

# Execute all experiments
run_omnirec(dataset, plan, evaluator)
```

This executes 6 algorithm runs (2 ItemKNN variants + 4 LightGCN variants) with automatic evaluation of NDCG and Recall metrics. Since LightGCN requires implicit feedback, we preprocess MovieLens100K from explicit ratings to implicit feedback using `MakeImplicit(3)`, and use ranking metrics appropriate for implicit feedback evaluation.
