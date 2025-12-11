# Getting Started

In this guide we will present how to install OmniRec and to design and implement your first experiments with it.

## Installation

First you need to setup a Python environment with at least Python 3.12 and install the OmniRec library by running:

```bash
pip install omnirec
```

## Loading Datasets

Central part of the OmniRec library is the [`RecSysDataSet`](API_references.md#omnirec.recsys_data_set.RecSysDataSet) class. You can load data by calling the static [`use_dataloader()`](API_references.md#omnirec.recsys_data_set.RecSysDataSet) function that returns a [`RecSysDataSet`](API_references.md#omnirec.recsys_data_set.RecSysDataSet) object. If provided a registered dataset name with DataSet.<dataset_name>, [`use_dataloader()`](API_references.md#omnirec.recsys_data_set.RecSysDataSet) downloads the dataset, removes duplicates and normalizes the identifiers:

```python
from omnirec import RecSysDataSet
from omnirec.data_loaders.datasets import DataSet

# Load the MovieLens 100K dataset
dataset = RecSysDataSet.use_dataloader(DataSet.MovieLens100K)
```

We provide a more detailed documentation in [Loading Datasets](loading_datasets.md) and a list of available datasets in [Datasets Overview](datasets_overview.md).

## Preprocessing Datasets

We can now apply the desired preprocessing steps to the data. The easiest way is to define a preprocessing pipeline:

```python
from omnirec.preprocess.core_pruning import CorePruning
from omnirec.preprocess.feedback_conversion import MakeImplicit
from omnirec.preprocess.pipe import Pipe
from omnirec.preprocess.split import UserHoldout

# Create a preprocessing pipeline
pipe = Pipe(
    MakeImplicit(3),           # Convert to implicit feedback (ratings >= 3)
    CorePruning(5),            # Keep only 5-core users and items
    UserHoldout(0.15, 0.15)    # Split into train/val/test sets
)

# Apply all preprocessing steps
dataset = pipe.process(dataset)
```

The [`pipe.process()`](API_references.md#omnirec.preprocess.pipe.Pipe) function iteratively executes the preprocessing steps.

Alternatively, this can be done step by step by creating a single preprocessing step and calling [`process()`](API_references.md#omnirec.preprocess.subsample.Subsample) on it:

```python
from omnirec.preprocess.subsample import Subsample

# Sample 10% of the interactions
step = Subsample(sample_size=0.1)
dataset = step.process(dataset)
```

More details about the available preprocessing steps can be found in [Preprocessing Pipeline](preprocessing.md).

## Configuring Experiments

To run experiments, you need to create an [`ExperimentPlan`](API_references.md#omnirec.runner.plan.ExperimentPlan) that specifies which algorithms to run and their hyperparameters:

```python
from omnirec.runner.plan import ExperimentPlan
from omnirec.runner.algos import LensKit, RecBole

# Create a new experiment plan
plan = ExperimentPlan(plan_name="My First Experiment")

# Add algorithms with configurations
# For LensKit ItemKNN with different neighborhood sizes
plan.add_algorithm(
    LensKit.ItemKNNScorer,
    {"max_nbrs": [10, 20, 30], "min_nbrs": 5}
)

# Add RecBole BPR algorithm with default parameters
plan.add_algorithm(RecBole.BPR)
```

When you provide a list of values for a hyperparameter (like `[10, 20, 30]` for `max_nbrs`), the framework will run separate experiments for each value.

You can find more information about the available algorithms and how to use them with OmniRec in the [Algorithms Overview](algorithms_overview.md) and [Configure Algorithms](conf_algo.md) documentation.

## Setting Up Evaluation Metrics

Define which metrics to compute on the test set:

```python
from omnirec import NDCG, HR, Recall
from omnirec.runner.evaluation import Evaluator

# Create evaluator with multiple metrics at different k values
evaluator = Evaluator(
    NDCG([5, 10, 20]),      # Normalized Discounted Cumulative Gain
    HR([5, 10, 20]),        # Hit Rate
    Recall([5, 10, 20])     # Recall
)
```
You can find more details about the available metrics and how to use them in the [Evaluator](evaluator.md) documentation.

## Running Experiments

Now we can run the experiments using the [`run_omnirec`](API_references.md#omnirec.util.run.run_omnirec) function:

```python
from omnirec.util.run import run_omnirec

# Run all experiments
run_omnirec(
    datasets=dataset,
    plan=plan,
    evaluator=evaluator
)
```

The [`run_omnirec`](API_references.md#omnirec.util.run.run_omnirec) function will:

1. Set up isolated Python environments for each algorithm framework
2. Train each algorithm configuration on the training data
3. Generate predictions on the test data
4. Compute all specified metrics
5. Save checkpoints to allow resuming interrupted experiments

After experiments complete, the results will be printed to the console and can also be accessed through the checkpoint files.

## Checkpointing and Results

OmniRec automatically saves experiment progress and results to the checkpoint directory. If an experiment is interrupted, simply run it again—the [`run_omnirec`](API_references.md#omnirec.util.run.run_omnirec) function will automatically resume from the last completed phase.

For detailed information about checkpoint structure, resuming experiments, and result formats, see the [Checkpointing and Results](checkpointing.md) documentation.

## Reproducibility

OmniRec uses a global random state to ensure reproducible results across experiments. By default, the random state is set to 42. You can control this using the [`set_random_state()`](API_references.md#omnirec.util.util.set_random_state) and [`get_random_state()`](API_references.md#omnirec.util.util.get_random_state) functions:

```python
from omnirec.util.util import set_random_state, get_random_state

# Set a specific random seed for reproducibility
set_random_state(123)

# Verify the random state
current_seed = get_random_state()
print(f"Current random seed: {current_seed}")  # Output: 123
```

Set the random state before running your experiments to ensure consistent results across multiple runs. This affects all random operations in preprocessing (e.g., data splitting) and algorithm training.

## Complete Example

Here's a complete example that puts it all together:

```python
from omnirec import RecSysDataSet
from omnirec.data_loaders.datasets import DataSet
from omnirec.preprocess.pipe import Pipe
from omnirec.preprocess.feedback_conversion import MakeImplicit
from omnirec.preprocess.core_pruning import CorePruning
from omnirec.preprocess.split import UserHoldout
from omnirec.runner.plan import ExperimentPlan
from omnirec.runner.algos import LensKit, RecBole
from omnirec.runner.evaluation import Evaluator
from omnirec import NDCG, HR
from omnirec.util.run import run_omnirec

# Load and preprocess dataset
dataset = RecSysDataSet.use_dataloader(DataSet.MovieLens100K)

pipeline = Pipe(
    MakeImplicit(3),
    CorePruning(5),
    UserHoldout(0.15, 0.15)
)
dataset = pipeline.process(dataset)

# Configure experiments
plan = ExperimentPlan(plan_name="MovieLens Comparison")
plan.add_algorithm(LensKit.ItemKNNScorer, {"max_nbrs": [20, 30]})
plan.add_algorithm(RecBole.BPR)

# Set up evaluation
evaluator = Evaluator(NDCG(10), HR(10))

# Run experiments
run_omnirec(datasets=dataset, plan=plan, evaluator=evaluator)
```

This example loads MovieLens 100K, preprocesses it, runs ItemKNN and BPR algorithms, evaluates them using NDCG, Hit Rate, and Recall metrics, and displays the results in formatted tables.