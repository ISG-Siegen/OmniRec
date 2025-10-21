# Checkpointing and Results

OmniRec automatically saves experiment progress and results to enable fault tolerance and result persistence.

## Checkpoint Directory Structure

The checkpoint directory organizes experiments hierarchically:

```
checkpoints/
├── progress.json                                    # Global progress tracker
├── out.log                                          # Runner stdout logs
├── err.log                                          # Runner stderr logs
└── {dataset-name}-{hash}/                          # Per dataset
    └── {algorithm-name}-{hash}/                    # Per algorithm configuration
        ├── predictions.json                        # Model predictions
        ├── fold_0/                                 # For cross-validation
        │   └── predictions.json
        ├── fold_1/
        │   └── predictions.json
        └── ...
```

**Key files:**

- **`progress.json`**: Tracks experiment phases (Fit, Predict, Eval, Done) for each configuration. Enables resuming interrupted experiments.
- **`predictions.json`**: Contains model predictions with columns: `user`, `item`, `score`, `rank`.
- **`out.log` / `err.log`**: Runner process output for debugging.

**Hash-Based Organization**

The [`Coordinator`](API_references.md#omnirec.runner.coordinator.Coordinator) generates unique hashes for datasets and configurations:

- **Dataset hash**: Based on the number of interactions, ensuring identical datasets share the same checkpoint directory
- **Configuration hash**: Based on algorithm name and hyperparameters, ensuring identical configurations are deduplicated

This hash-based system enables efficient caching and prevents redundant computation.

## Resuming Experiments

If an experiment is interrupted, simply run it again with the same configuration:

```python
from omnirec.util.run import run_omnirec

# First run - interrupted during training
run_omnirec(datasets=dataset, plan=plan, evaluator=evaluator)

# Second run - automatically resumes from last checkpoint
run_omnirec(datasets=dataset, plan=plan, evaluator=evaluator)
```

The framework automatically:
1. Loads the progress tracker from `progress.json`
2. Skips completed phases (Fit, Predict, Eval)
3. Continues from the last incomplete phase
4. Reuses existing predictions instead of retraining

**Progress Phases**

Each experiment goes through four phases:

1. **Fit**: Train the model on training data
2. **Predict**: Generate predictions on test data
3. **Eval**: Compute metrics on predictions
4. **Done**: Experiment complete

The `progress.json` file tracks the current phase for each experiment configuration. If interrupted, the next run resumes from the last incomplete phase.

**Cross-Validation Support**

For cross-validation experiments (FoldedData), progress is tracked per fold:

- Each fold goes through all phases independently
- The progress tracker maintains the current fold number
- Interrupted experiments resume from the incomplete fold

## Result Format

Results are displayed in formatted tables showing:

- **Algorithm**: The algorithm name and configuration hash
- **Fold**: Cross-validation fold number (if applicable, hidden if single split)
- **Metrics**: All computed metrics at specified k values (e.g., NDCG@10, HR@20)

**Example Output**

```
MovieLens100K-a3f8e2c1: Evaluation Results
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┓
┃ Algorithm              ┃ NDCG@10 ┃ NDCG@20 ┃ HR@10  ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━┩
│ LensKit.ItemKNN-b7d4a9 │ 0.3245  │ 0.3891  │ 0.6142 │
│ RecBole.BPR-c8e5f1a3   │ 0.3156  │ 0.3802  │ 0.5987 │
└────────────────────────┴─────────┴─────────┴────────┘
```

For cross-validation results with multiple folds:

```
MovieLens100K-a3f8e2c1: Evaluation Results
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━┓
┃ Algorithm              ┃ Fold ┃ NDCG@10 ┃ HR@10   ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━┩
│ LensKit.ItemKNN-b7d4a9 │ 0    │ 0.3201  │ 0.6089  │
│                        │ 1    │ 0.3289  │ 0.6195  │
│                        │ 2    │ 0.3245  │ 0.6142  │
└────────────────────────┴──────┴─────────┴─────────┘
```

## Caching and Deduplication

Experiments are cached based on dataset and configuration hashes. If you run the same experiment multiple times:

- The coordinator detects identical configurations via hash comparison
- Skips redundant computation (all phases marked as Done)
- Reuses cached predictions and results

This ensures efficient experimentation and prevents accidental duplication of expensive training runs.

**When Caching Triggers**

Caching activates when:
- Same dataset (same data and number of interactions)
- Same algorithm and hyperparameters
- Same preprocessing pipeline

Even with different variable names or execution contexts, identical experiments are recognized and deduplicated.

## Log Files

**stdout (out.log)**

Contains standard output from runner processes, including:

- Algorithm initialization messages
- Training progress
- Model information
- Framework-specific logs

**stderr (err.log)**

Contains error output from runner processes, including:

- Warning messages
- Error traces
- Framework warnings
- Debugging information

Both log files are appended to across multiple experiment runs, providing a complete history of runner activity.

### Debugging

If experiments fail:

1. Check `err.log` for error messages
2. Review `out.log` for algorithm output
3. Examine `progress.json` to see which phase failed
4. Verify dataset preprocessing and splitting
