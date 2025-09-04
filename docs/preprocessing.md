# Preprocessing Pipeline

This section explains how to preprocess datasets using the framework's preprocessing pipeline. The preprocessing system provides a modular approach to transform datasets through various operations like subsampling, feedback conversion, core pruning, and data splitting.

All preprocessing operations inherit from the `Preprocessor` base class, which defines a common interface for processing datasets. Each preprocessor takes a `RecSysDataSet` as input and returns a transformed dataset, potentially of a different data variant.

## Pipe Class

The `Pipe` class allows you to chain multiple preprocessing steps together into a single preprocessing pipeline:

```python
from recsyslib.preprocess import Pipe, Subsample, MakeImplicit, CorePruning

# Create a preprocessing pipeline
pipeline = Pipe(
    Subsample(0.1),
    MakeImplicit(3),
    CorePruning(5),
)

# Apply all steps sequentially
processed_dataset = pipeline.process(dataset)
```

The pipeline executes each step in the order they were provided, passing the output of one step as input to the next.

## Data Processing

**Subsample** - Reduces the dataset size by sampling a subset of interactions:

```python
from recsyslib.preprocess import Subsample

# Sample 10% of interactions
subsample = Subsample(0.1)
dataset = subsample.process(dataset)

# Sample exactly 1000 interactions
subsample = Subsample(1000)
dataset = subsample.process(dataset)
```

**Parameters:**
- `sample_size` (int | float): Number or fraction of interactions to sample
  - `int`: Absolute number of interactions
  - `float`: Fraction of dataset (0.0 to 1.0)

**MakeImplicit** - Converts explicit feedback to implicit feedback by filtering interactions above a threshold:

```python
from recsyslib.preprocess import MakeImplicit

# Keep ratings >= 3
make_implicit = MakeImplicit(3)
dataset = make_implicit.process(dataset)

# Keep top 50% of ratings
make_implicit = MakeImplicit(0.5)
dataset = make_implicit.process(dataset)
```

**Parameters:**
- `threshold` (int | float): Threshold for filtering interactions
  - `int`: Direct rating threshold
  - `float`: Fraction of maximum rating (0.0 to 1.0)

**CorePruning** - Removes users and items with fewer than a specified number of interactions:

```python
from recsyslib.preprocess import CorePruning

# Keep only users and items with at least 5 interactions
core_pruning = CorePruning(5)
dataset = core_pruning.process(dataset)
```

**Parameters:**
- `core` (int): Minimum number of interactions required for users and items

## Data Splitting

**Holdout Splits** - Create train/validation/test splits:

```python
from recsyslib.preprocess import UserHoldout, RandomHoldout

# User-aware split (each user appears in all sets)
user_split = UserHoldout(validation_size=0.15, test_size=0.15)
dataset = user_split.process(dataset)

# Random split (no user constraints)
random_split = RandomHoldout(validation_size=0.15, test_size=0.15)
dataset = random_split.process(dataset)
```

**Parameters:**
- `validation_size` (float | int): Size of validation set
  - `float`: Proportion of dataset (0.0 to 1.0)
  - `int`: Absolute number of interactions
- `test_size` (float | int): Size of test set
  - `float`: Proportion of dataset (0.0 to 1.0)
  - `int`: Absolute number of interactions

**Cross-Validation** - Create multiple folds for cross-validation:

```python
from recsyslib.preprocess import UserCrossValidation, RandomCrossValidation

# User-aware cross-validation (each user appears in all splits)
user_cv = UserCrossValidation(num_folds=5, validation_size=0.1)
dataset = user_cv.process(dataset)

# Random cross-validation (no user constraints)
random_cv = RandomCrossValidation(num_folds=5, validation_size=0.1)
dataset = random_cv.process(dataset)
```

**Parameters:**
- `num_folds` (int): Number of cross-validation folds
- `validation_size` (float | int): Size of validation set in each fold
  - `float`: Proportion of training data (0.0 to 1.0)
  - `int`: Absolute number of interactions

## Data Variant Transformation

The preprocessing operations transform datasets between different data variants:

- `Subsample`, `MakeImplicit`, `CorePruning`: RawData → RawData
- `UserHoldout`, `RandomHoldout`: RawData → SplitData  
- `UserCrossValidation`, `RandomCrossValidation`: RawData → FoldedData

**Random State** - All operations that involve randomness (sampling, splitting) use a consistent random state for reproducibility.

## Complete Example

```python
from recsyslib import RecSysDataSet
from recsyslib.preprocess import (
    Pipe, Subsample, MakeImplicit, CorePruning, UserCrossValidation
)

# Load dataset
dataset = RecSysDataSet.use_dataloader("MovieLens100K")

# Create and apply comprehensive preprocessing pipeline
pipeline = Pipe(
    Subsample(0.1),                    # Sample 10% of interactions
    MakeImplicit(3),                   # Convert to implicit (ratings >= 3)
    CorePruning(5),                    # Keep 5-core users and items
    UserCrossValidation(5, 0.1)        # 5-fold CV with 10% validation
)

processed_dataset = pipeline.process(dataset)

# Access the cross-validation folds
for fold_idx, split_data in processed_dataset._data.folds.items():
    print(f"Fold {fold_idx}:")
    print(f"  Train: {len(split_data.train)} interactions")
    print(f"  Validation: {len(split_data.val)} interactions")
    print(f"  Test: {len(split_data.test)} interactions")
```
