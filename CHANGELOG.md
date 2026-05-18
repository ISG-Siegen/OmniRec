## v1.0.0 (2026-05-13)

### Feat

- install the resolved omnirec-runner version in managed envs
- expose metadata and lineage summaries
- add versioned dataset save/load support
- add lineage tracing for preprocessing steps
- add number of columns statistic to RecSysDataSet
- Improve robustness in coordinator-runner communication
- add precision@k ranking metric
- store algorithm config in progress.json for run hash identification
- add more flexible component for the `ExperimentPlan` to better distinguish between literal hyper-parameters and grid search. Also add additional random search component
- add get_results method to evaluator to export internal results data
- skip subprocess call to uv if venv already exist

### Fix

- replace deprecated pandas Series.view with astype in `RecSysDataSet`
- honor force when overwriting algorithm configs in `ExperimentPlan`
- preserve timestamps in implicit feedback conversion
- solve status timeout issues caused by GIL thread starvation
- avoid shared _DatasetMeta default instance in RecSysDataSet
- resolve crash in elliot runner by removing local absolute path
- include random seed in config hash
- pin setuptools to version <82 in RecBole environment
- Do not resolve symlinks when invoking uv in enviroment manager. Use absolute path instead.

### Refactor

- move registered runners to a separate file

## v0.2.0 (2026-01-16)

### Feat

- add additional datasets

### Fix

- auto download for behance dataset

## v0.1.1 (2025-12-11)

### Feat

- add rating filter
- add time filter
- add time based holdout
- add normalization of timestamps to _canonicalize in RSDS
- add 72 more datasets
- add optional slurm_script to run_omnirec
- add exception to recpack runner to exit early if started with explicit feedback
- run_omnirec prints evaluation results automatically at the end
- add elliot runner
- debug logging uv output live while running instead of just capturing it
- add recpack runner
- add method for creating rich table to evaluator
- add amazon 2023 dataset
- add amazon 2018 dataset
- add code generation tool for static type checking stubs for datasets and algorithms
- add smarter type inference for Pipe
- changed metrics parameter of Evaluator to be a variadic argument instead of Iterable
- replace temporary prints in coordinator with proper logging
- automatically configure logging using rich.logging
- add run_omnirec convenience function
- rename logger to omnirec
- add recbole runner
- pass dataset name to runner
- add fit predict cycle, metric implementations, lenskit runner

### Fix

- **docs**: fixed code example in user guide.
- runner path resolution now works when installing from pypi
- move data dir to .omnirec by default and make it configurable
- add correct results checkpointing
- _normalize_timestamps now handles other time formats that did not work before
- bug in recbole runner
- change runner method signatures to older typing syntax to support older python versions
- changed column to rating when doing rating prediction
- remove code that was used for testing
- return evaluator at the right point from Coordinator.run
- handle runner stdout/stderr correctly
- adapt lenskit runner to new column format in metric implementation
- update column names in make_topk_dict in ranking.py
- handle new prediction format in metric implementations
- correctly load dataset metadata in RecSysDataSet.load
- added syntax highlighting to api reference examples
- UserCrossValidation now correctly concatenates the data at the end of process

### Refactor

- remove unused method from evaluator
- rename package from recsyslib to omnirec
- move util to separate package
