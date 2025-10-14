# API Reference

## Dataset Management
::: omnirec.recsys_data_set.RecSysDataSet
    options:
      show_root_heading: true
      show_root_toc_entry: false
      members_order: source

## Preprocessing Pipeline

::: omnirec.preprocess.subsample.Subsample
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.preprocess.core_pruning.CorePruning
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.preprocess.feedback_conversion.MakeImplicit
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.preprocess.split.RandomCrossValidation
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.preprocess.split.RandomHoldout
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.preprocess.split.UserCrossValidation
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.preprocess.split.UserHoldout
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.preprocess.pipe.Pipe
    options:
      show_root_heading: true
      show_root_toc_entry: false

## Evaluation Metrics

::: omnirec.runner.evaluation.Evaluator
    options:
      show_root_heading: true
      show_root_toc_entry: false

### Ranking Metrics
::: omnirec.metrics.ranking.HR
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.metrics.ranking.NDCG
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.metrics.ranking.Recall
    options:
      show_root_heading: true
      show_root_toc_entry: false

### Prediction Metrics
::: omnirec.metrics.prediction.MAE
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.metrics.prediction.RMSE
    options:
      show_root_heading: true
      show_root_toc_entry: false


## Experiment Planning
::: omnirec.runner.plan.ExperimentPlan
    options:
      show_root_heading: true
      show_root_toc_entry: false

## Runner Function
::: omnirec.util.run.run_omnirec
    options:
      show_root_heading: true
      show_root_toc_entry: false

## Coordinator Class
::: omnirec.runner.coordinator.Coordinator
    options:
      show_root_heading: true
      show_root_toc_entry: false
