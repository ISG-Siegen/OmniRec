# Evaluation Metrics

::: omnirec.runner.evaluation.Evaluator
    options:
      show_root_heading: true
      show_root_toc_entry: false

## Metric Base Classes

::: omnirec.metrics.base.Metric
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.metrics.base.Metric.calculate
    options:
      show_root_heading: true
      show_root_toc_entry: false
      heading_level: 3

::: omnirec.metrics.base.MetricResult
    options:
      show_root_heading: true
      show_root_toc_entry: false

## Ranking Metrics

All ranking metrics average over users with predictions and at least one relevant test interaction. In the formulas below, `U` (or `U_eligible`) denotes this set. Predicted users without test interactions are skipped and logged; test users without predictions are outside the average. If the set is empty, each cutoff returns `0.0`. See [Ranking Metric Semantics](../evaluator.md#ranking-metric-semantics) for input columns and examples.

::: omnirec.metrics.ranking.HR
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.metrics.ranking.NDCG
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.metrics.ranking.Precision
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.metrics.ranking.Recall
    options:
      show_root_heading: true
      show_root_toc_entry: false

## Prediction Metrics
::: omnirec.metrics.prediction.MAE
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.metrics.prediction.RMSE
    options:
      show_root_heading: true
      show_root_toc_entry: false
