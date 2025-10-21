# Evaluation Metrics

This section explains how to configure and use metrics to evaluate recommendation algorithms. The evaluation system provides a flexible approach to compute various metrics after model predictions, supporting both explicit and implicit feedback scenarios.

The [`Evaluator`](API_references.md#omnirec.runner.evaluation.Evaluator) class manages metric computation across all algorithm runs. It automatically loads predictions and applies the specified metrics, supporting both holdout and cross-validation splits.

## Evaluator Class

The [`Evaluator`](API_references.md#omnirec.runner.evaluation.Evaluator) class coordinates metric calculation across experiments. Create an evaluator by passing one or more metric instances, then provide it to [`run_omnirec`](API_references.md#omnirec.util.run.run_omnirec) to automatically evaluate all algorithm runs:

```python
from omnirec.runner.evaluation import Evaluator
from omnirec.metrics.ranking import NDCG, HR, Recall

# Create evaluator with ranking metrics for implicit feedback
evaluator = Evaluator(
    NDCG([5, 10, 20]),
    HR([5, 10, 20]),
    Recall([5, 10, 20])
)
```

The evaluator can combine multiple metrics of the same type in a single evaluation run. Choose metrics appropriate for your feedback type: use prediction metrics ([`RMSE`](API_references.md#omnirec.metrics.prediction.RMSE), [`MAE`](API_references.md#omnirec.metrics.prediction.MAE)) for explicit ratings, and ranking metrics ([`NDCG`](API_references.md#omnirec.metrics.ranking.NDCG), [`HR`](API_references.md#omnirec.metrics.ranking.HR), [`Recall`](API_references.md#omnirec.metrics.ranking.Recall)) for implicit feedback or top-k recommendations.

## Available Metrics

**Prediction Metrics** - For explicit feedback scenarios where ratings are predicted:

```python
from omnirec.metrics.prediction import RMSE, MAE

# Root Mean Squared Error
rmse = RMSE()

# Mean Absolute Error  
mae = MAE()
```

Use prediction metrics when evaluating algorithms that predict rating values, such as matrix factorization methods on explicit feedback datasets.

**Ranking Metrics** - For top-k recommendation scenarios:

```python
from omnirec.metrics.ranking import NDCG, HR, Recall

# Normalized Discounted Cumulative Gain at k=[5, 10, 20]
ndcg = NDCG([5, 10, 20])

# Hit Rate at k=[5, 10]
hr = HR([5, 10])

# Recall at k=[10, 20]
recall = Recall([10, 20])
```

Ranking metrics evaluate the quality of top-k recommendation lists. Specify cutoff values (k) to measure performance at different list lengths. For example, [`NDCG([5, 10, 20])`](API_references.md#omnirec.metrics.ranking.NDCG) computes NDCG@5, NDCG@10, and NDCG@20.

## Running Experiments with Evaluation

Provide the evaluator when launching experiments with [`run_omnirec`](API_references.md#omnirec.util.run.run_omnirec). The framework automatically applies all metrics after each algorithm completes:

```python
from omnirec import RecSysDataSet
from omnirec.runner.plan import ExperimentPlan
from omnirec.runner.evaluation import Evaluator
from omnirec.runner.algos import RecBole
from omnirec.metrics.ranking import NDCG, Recall
from omnirec.preprocess.pipe import Pipe
from omnirec.preprocess.feedback_conversion import MakeImplicit
from omnirec.preprocess.split import UserHoldout
from omnirec.util.run import run_omnirec

# Load dataset and convert to implicit feedback
dataset = RecSysDataSet.use_dataloader("MovieLens100K")
pipeline = Pipe(
    MakeImplicit(3),           # Convert ratings >= 3 to implicit feedback
    UserHoldout(0.15, 0.15)    # Split data
)
dataset = pipeline.process(dataset)

# Create experiment plan with implicit feedback algorithm
plan = ExperimentPlan("MyExperiment")
plan.add_algorithm(RecBole.BPR)  # BPR is for implicit feedback

# Configure evaluator with ranking metrics (appropriate for implicit feedback)
evaluator = Evaluator(NDCG([10]), Recall([10]))

# Run experiments with automatic evaluation
run_omnirec(dataset, plan, evaluator)
```

All metric computations happen automatically without additional code. Ensure your metrics match your data type: ranking metrics (NDCG, HR, Recall) for implicit feedback, and prediction metrics (RMSE, MAE) for explicit feedback.

Additionally, metric results are logged during execution and stored in checkpoint directories alongside model predictions.

## Custom Metrics

To implement custom evaluation metrics, create a subclass of [`omnirec.metrics.base.Metric`](API_references.md#omnirec.metrics.base.Metric) and implement the [`calculate`](API_references.md#omnirec.metrics.base.Metric.calculate) method:

```python
from omnirec.metrics.base import Metric, MetricResult
import pandas as pd

class CustomMetric(Metric):
    def calculate(
        self, 
        predictions: pd.DataFrame, 
        test: pd.DataFrame
    ) -> MetricResult:
        """
        Calculate custom metric from predictions and test data.
        
        Args:
            predictions: DataFrame with predictions
            test: DataFrame with ground truth test data
            
        Returns:
            MetricResult with metric name and computed value
        """
        # Implement your metric calculation logic
        metric_value = self._compute_value(predictions, test)
        
        return MetricResult(
            name="CustomMetric",
            result=metric_value
        )
    
    def _compute_value(
        self, 
        predictions: pd.DataFrame, 
        test: pd.DataFrame
    ) -> float:
        # Custom calculation logic
        pass
```

Use custom metrics the same way as built-in metrics:

```python
from omnirec.metrics.prediction import RMSE

# Add custom metric to evaluator (both for explicit feedback)
evaluator = Evaluator(
    RMSE(),
    CustomMetric()
)
```

The custom metric will be automatically applied to all algorithm runs alongside the standard metrics. Ensure your custom metric is appropriate for the feedback type of your dataset.

