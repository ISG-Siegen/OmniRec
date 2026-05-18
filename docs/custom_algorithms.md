# Implementing Custom Algorithms

The OmniRec framework uses an isolated runner architecture via RPyC to execute algorithms. This ensures that different algorithms can run in completely separate environments without dependency conflicts. To implement a custom algorithm and use it in your experiments, you need to create a custom runner.

Implementing a custom algorithm involves three main development steps:

1. **Subclassing the base Runner**: Create an isolated execution script that inherits from `omnirec_runner.runner.Runner`.
2. **Implementing the Training Logic**: Override the `fit()` method by implementing your algorithm's training logic.
3. **Implementing the Inference Logic**: Override the `predict()` method to generate predictions correctly formatted for the evaluator.

## Creating the Custom Runner

Create a new Python script (e.g., `my_runner.py`). In this script, subclass the `Runner` base class from `omnirec_runner.runner`. You must implement the abstract `fit()` and `predict()` methods. You can also optionally override `setup_fit()`, `post_fit()`, `setup_predict()`, and `post_predict()`.

During execution, the runner automatically populates various instance variables that you can use:

* `self.algorithm_name` (`str`): The name of the currently running algorithm.
* `self.algorithm_config` (`dict[str, Any]`): A dictionary containing the JSON-parsed hyperparameters for the current run.
* `self.train_file`, `self.val_file`, `self.test_file` (`Path`): Objects pointing to the standard CSV dataset splits. Typically you will load these via `pandas.read_csv()`.
* `self.checkpoint_dir`, `self.tmp_dir` (`Path`): Directories for saving model checkpoints or any temporary files. Saving your fitted model here natively allows reusing it during the predict phase.

### Prediction Output Format

The `predict()` method must return a dictionary of lists typing out to `Dict[Any, Any]` (so it can be dumped to JSON). The easiest approach is generating a `pandas.DataFrame` and returning `df.to_dict(orient="list")`. Depending on whether your algorithms predict explicit ratings or top-k rankings for implicit feedback, the expected columns/keys differ:

* **Explicit Feedback** (Prediction metrics like RMSE, MAE): 
  Requires `user`, `item`, and `rating`.
* **Implicit Feedback** (Ranking metrics like NDCG, HR): 
  Requires `user`, `item`, `score`, and `rank`. You must explicitly calculate and assign 1-based ranks to your ordered predictions for computing hits/gain properly.

### Example Runner Script

Below is a complete example highlighting the standard data types, loading the CSV with `pandas`, grouping ranks, and formatting the return value as expected by OmniRec's evaluation engine.

```python
from typing import Any, Dict
import pandas as pd
from omnirec_runner.runner import Runner

class MyCustomRunner(Runner):
    
    def fit(self) -> None:
        # 1. Load train file stored as CSV
        self.train_df: pd.DataFrame = pd.read_csv(self.train_file)
        
        # 2. Extract hyperparameters
        # E.g., fallback default values
        self.popularity_weight = self.algorithm_config.get("pop_weight", 1.0)
        
        # 3. Fit loop
        # Calculate scores in training space (mock example logic)
        self.item_scores = self.train_df["item"].value_counts() * self.popularity_weight
        
    def predict(self) -> Dict[Any, Any]:
        # 1. Load test data
        test_df: pd.DataFrame = pd.read_csv(self.test_file)
        
        # 2. Create predictions for relevant users
        predictions = []
        for _, row in test_df.iterrows():
            item = row["item"]
            score = self.item_scores.get(item, 0.0)
            predictions.append({
                "user": row["user"],
                "item": item,
                "score": float(score)
            })
            
        pred_df = pd.DataFrame(predictions)
        
        # 3. Explicitly sort by score descending and assign a 1-based "rank" column
        # This is strictly required for implicit ranking metrics (like NDCG or HR)
        pred_df = pred_df.sort_values(["user", "score"], ascending=[True, False])
        pred_df["rank"] = pred_df.groupby("user").cumcount() + 1
        
        # 4. Return as Dict[Any, Any] containing lists of values
        return pred_df.to_dict(orient="list")

if __name__ == "__main__":
    # This is required to start the RPyC server context
    MyCustomRunner.main()
```

## Registering the Custom Runner

Before you can use your custom algorithm, you must register its script using `register_runner`. You do this in your main experiment script before defining the `ExperimentPlan`.

**Note:** The registration is *not* persistent across Python sessions. It dynamically maps your runner's paths and instructions into the framework's internal registry (`_RUNNER_REGISTRY`) strictly for the lifecycle of the currently running evaluation script. You must actively execute the `register_runner` line every time you launch your experiment suite.

You will define a `RunnerInfo` generic object identifying the script's `Path`, the named algorithms it exposes, its required Python version, and any package dependencies.

```python
from pathlib import Path
from omnirec.runner.registry import register_runner
from omnirec_runner.runner import RunnerInfo

# Define the runner context
my_runner_info = RunnerInfo(
    runner_path=Path("my_runner.py"), # Absolute or relative Path object to your runner
    algorithms=["MyDummyAlgo"],       # List: string identifiers for algorithms exposed
    python_version="3.11",            # String: target python env version
    packages=["pandas"]               # List: string definitions matching dependencies
)

# Register the runner under a specific prefix name
register_runner("MyRunner", my_runner_info)
```

## Complete Example

To see everything in action, save the `MyCustomRunner` class from above as `my_runner.py` and the following script as `main_experiment.py` in the same directory. 

This experiment script correctly registers your runner, hooks seamlessly into one of the default datasets with a preprocessing pipeline, configures your `ExperimentPlan`, and evaluates your custom logic end-to-end.

```python
from pathlib import Path

from omnirec import RecSysDataSet
from omnirec.data_loaders.datasets import DataSet
from omnirec.metrics.ranking import NDCG
from omnirec.preprocess.pipe import Pipe
from omnirec.preprocess.feedback_conversion import MakeImplicit
from omnirec.preprocess.split import UserHoldout
from omnirec.runner.evaluation import Evaluator
from omnirec.runner.plan import ExperimentPlan
from omnirec.runner.registry import register_runner
from omnirec_runner.runner import RunnerInfo
from omnirec.util.run import run_omnirec

# 1. Register the Custom Runner
# The resolved absolute path ensures the RPyC server can spawn it accurately
my_runner_info = RunnerInfo(
    runner_path=Path("my_runner.py").resolve(),
    algorithms=["MyDummyAlgo"],
    python_version="3.11",
    packages=["pandas"]
)
register_runner("MyRunner", my_runner_info)

# 2. Load and Preprocess the Dataset
dataset = RecSysDataSet.use_dataloader(DataSet.MovieLens100K)
pipeline = Pipe(
    MakeImplicit(3),
    UserHoldout(validation_size=0.2, test_size=0.1)
)
dataset = pipeline.process(dataset)

# 3. Create the Experiment Plan
plan = ExperimentPlan("Custom-Algo-Experiment")
plan.add_algorithm(
    "MyRunner.MyDummyAlgo", 
    {"pop_weight": 0.8}
)

# 4. Evaluate and Run
evaluator = Evaluator(NDCG(k=[10, 20]))
run_omnirec(dataset, plan, evaluator)
```