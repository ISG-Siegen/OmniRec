# Preprocessing Pipeline

::: omnirec.preprocess.base.Preprocessor
    options:
      show_root_heading: true
      show_root_toc_entry: false
      members:
        - process
        - _process

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

## Filtering

::: omnirec.preprocess.filter.TimeFilter
    options:
      show_root_heading: true
      show_root_toc_entry: false
      heading_level: 3

::: omnirec.preprocess.filter.RatingFilter
    options:
      show_root_heading: true
      show_root_toc_entry: false
      heading_level: 3

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

::: omnirec.preprocess.split.TimeBasedHoldout
    options:
      show_root_heading: true
      show_root_toc_entry: false

::: omnirec.preprocess.pipe.Pipe
    options:
      show_root_heading: true
      show_root_toc_entry: false
