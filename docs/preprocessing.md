# Preprocessing Pipeline

This section explains how to preprocess datasets using the framework's preprocessing pipeline. The preprocessing system provides a modular approach to transform datasets through various operations like subsampling, feedback conversion, core pruning, and data splitting.

All preprocessing operations inherit from the [`Preprocessor`](API_references.md#omnirec.preprocess.base.Preprocessor) base class, which defines a common interface for processing datasets. Each preprocessor takes a [`RecSysDataSet`](API_references.md#omnirec.recsys_data_set.RecSysDataSet) as input and returns a transformed dataset, potentially of a different data variant.

## Pipe Class

The [`Pipe`](API_references.md#omnirec.preprocess.pipe.Pipe) class allows you to chain multiple preprocessing steps together into a single preprocessing pipeline:

```python
from omnirec.preprocess import Pipe, Subsample, MakeImplicit, CorePruning

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
from omnirec.preprocess import Subsample

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
from omnirec.preprocess import MakeImplicit

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
from omnirec.preprocess import CorePruning

# Keep only users and items with at least 5 interactions
core_pruning = CorePruning(5)
dataset = core_pruning.process(dataset)
```

**Parameters:**

- `core` (int): Minimum number of interactions required for users and items

### Filtering

Apply filtering based on timestamps or ratings to the dataset:

**TimeFilter** - Filters interactions based on timestamp range:

```python
import pandas as pd
from omnirec.preprocess.filter import TimeFilter

# Keep interactions from January 1998
time_filter = TimeFilter(
    start=pd.Timestamp(year=1998, month=1, day=1),
    end=pd.Timestamp(year=1998, month=1, day=30),
)
dataset = time_filter.process(dataset)

# Keep interactions after a specific date (no end date)
time_filter = TimeFilter(start=pd.Timestamp(year=1998, month=3, day=1))
dataset = time_filter.process(dataset)
```

**Parameters:**

- `start` (Optional[pd.Timestamp]): Start timestamp for the filter (inclusive)
- `end` (Optional[pd.Timestamp]): End timestamp for the filter (inclusive)

**RatingFilter** - Filters interactions based on rating values:

```python
from omnirec.preprocess.filter import RatingFilter

# Keep ratings between 1 and 3
rating_filter = RatingFilter(lower=1, upper=3)
dataset = rating_filter.process(dataset)

# Keep ratings >= 4 (no upper bound)
rating_filter = RatingFilter(lower=4)
dataset = rating_filter.process(dataset)
```

**Parameters:**

- `lower` (Optional[int | float]): Lower bound for rating values (inclusive)
- `upper` (Optional[int | float]): Upper bound for rating values (inclusive)

## Data Splitting

### Holdout Splits 
Create train/validation/test splits:

```python
from omnirec.preprocess import UserHoldout, RandomHoldout

# User-aware split (each user appears in all sets)
user_split = UserHoldout(validation_size=0.15, test_size=0.15)
dataset = user_split.process(dataset)

# Random split (no user constraints)
random_split = RandomHoldout(validation_size=0.15, test_size=0.15)
dataset = random_split.process(dataset)
```

UserHoldout ensures that each user has interactions in all splits, while RandomHoldout randomly assigns interactions without user constraints.

**Parameters:**

- `validation_size` (float | int): Size of validation set
    - `float`: Proportion of dataset (0.0 to 1.0)
    - `int`: Absolute number of interactions
- `test_size` (float | int): Size of test set
    - `float`: Proportion of dataset (0.0 to 1.0)
    - `int`: Absolute number of interactions

### Cross-Validation
Create multiple folds for cross-validation:

```python
from omnirec.preprocess import UserCrossValidation, RandomCrossValidation

# User-aware cross-validation (each user appears in all splits)
user_cv = UserCrossValidation(num_folds=5, validation_size=0.2)
dataset = user_cv.process(dataset)

# Random cross-validation (no user constraints)
random_cv = RandomCrossValidation(num_folds=5, validation_size=0.2)
dataset = random_cv.process(dataset)
```

Cross-Validation creates multiple folds for evaluation, so different interactions are used for validation in each fold.
UserCrossValidation ensures that each user has interactions in all splits, while RandomCrossValidation randomly assigns interactions without user constraints.

**Parameters:**

- `num_folds` (int): Number of cross-validation folds
- `validation_size` (float | int): Size of validation set in each fold
    - `float`: Proportion of training data (0.0 to 1.0)
    - `int`: Absolute number of interactions

### Time-based Splits

Create splits based on timestamps.

**TimeBasedHoldout** - Splits the dataset chronologically into train, validation, and test sets:

```python
import pandas as pd
from omnirec.preprocess.split import TimeBasedHoldout

# Split using timestamp cutoffs
time_split = TimeBasedHoldout(
    validation=pd.Timestamp(year=1998, month=1, day=3),
    test=pd.Timestamp(year=1998, month=3, day=12),
)
dataset = time_split.process(dataset)

# Split using proportions (newest 15% for test, next 15% for validation)
time_split = TimeBasedHoldout(validation=0.15, test=0.15)
dataset = time_split.process(dataset)

# Split using absolute counts (newest 1000 for test, next 500 for validation)
time_split = TimeBasedHoldout(validation=500, test=1000)
dataset = time_split.process(dataset)
```

The dataset is sorted by timestamp and split, with older interactions going to training and newer ones to validation/test.

**Parameters:**

- `validation` (float | int | pd.Timestamp): Validation set specification
    - `float`: Proportion of newest interactions (0.0 to 1.0)
    - `int`: Absolute number of newest interactions
    - `pd.Timestamp`: Timestamp cutoff (interactions after this go to validation)
- `test` (float | int | pd.Timestamp): Test set specification (same type as validation)
    - `float`: Proportion of newest interactions (0.0 to 1.0)
    - `int`: Absolute number of newest interactions
    - `pd.Timestamp`: Timestamp cutoff (interactions after this go to test)

**Note:** Both parameters must be of the same type. The dataset is sorted by timestamp, and interactions are split based on the specified criteria, with older interactions in training and newer ones in validation/test.

## Random State
All operations that involve randomness (sampling, splitting) use a consistent random state for reproducibility. See [Getting Started > Reproducibility](getting_started.md#reproducibility) for details how to handle random states.

## Data Variant Transformation

The preprocessing operations transform datasets between different data variants:

- [`Subsample`](API_references.md#omnirec.preprocess.subsample.Subsample), [`MakeImplicit`](API_references.md#omnirec.preprocess.feedback_conversion.MakeImplicit), [`CorePruning`](API_references.md#omnirec.preprocess.core_pruning.CorePruning), [`TimeFilter`](API_references.md#omnirec.preprocess.filter.TimeFilter), [`RatingFilter`](API_references.md#omnirec.preprocess.filter.RatingFilter): RawData → RawData
- [`UserHoldout`](API_references.md#omnirec.preprocess.split.UserHoldout), [`RandomHoldout`](API_references.md#omnirec.preprocess.split.RandomHoldout), [`TimeBasedHoldout`](API_references.md#omnirec.preprocess.split.TimeBasedHoldout): RawData → SplitData  
- [`UserCrossValidation`](API_references.md#omnirec.preprocess.split.UserCrossValidation), [`RandomCrossValidation`](API_references.md#omnirec.preprocess.split.RandomCrossValidation): RawData → FoldedData


## Custom Preprocessing Steps

You can create custom preprocessing steps by inheriting from the [`Preprocessor`](API_references.md#omnirec.preprocess.base.Preprocessor) base class and implementing the [`process()`](API_references.md#omnirec.preprocess.base.Preprocessor.process) method.

**Implementation**

Custom preprocessors must:

1. Inherit from [`Preprocessor[T, U]`](API_references.md#omnirec.preprocess.base.Preprocessor) where `T` is the input data variant and `U` is the output data variant
2. Call `super().__init__()` in the constructor
3. Implement the [`process()`](API_references.md#omnirec.preprocess.base.Preprocessor.process) method that transforms a `RecSysDataSet[T]` to `RecSysDataSet[U]`

**Available Data Variants:**

- `RawData`: Single DataFrame with all interactions
- `SplitData`: Separate train, validation, and test DataFrames
- `FoldedData`: Multiple folds for cross-validation

**Example:**

```python
from omnirec.preprocess.base import Preprocessor
from omnirec.recsys_data_set import RawData, RecSysDataSet

class CustomPreprocessor(Preprocessor[RawData, RawData]):
    def __init__(self, param1: int, param2: float) -> None:
        """Your custom preprocessing step.
        
        Args:
            param1: Description of parameter 1
            param2: Description of parameter 2
        """
        super().__init__()
        self.param1 = param1
        self.param2 = param2
    
    def process(self, dataset: RecSysDataSet[RawData]) -> RecSysDataSet[RawData]:
        # Log what you're doing
        self.logger.info(f"Applying custom preprocessing with params: {self.param1}, {self.param2}")
        
        # Transform the data
        # For RawData: modify dataset._data.df directly
        # For SplitData: access dataset._data.train, dataset._data.val, dataset._data.test
        dataset._data.df = dataset._data.df[...]  # Your transformation logic
        
        # Return the dataset
        return dataset
```

Custom preprocessors can be used directly or within a [`Pipe`](API_references.md#omnirec.preprocess.pipe.Pipe):

```python
from omnirec.preprocess import Pipe, CorePruning

pipeline = Pipe(
    CustomPreprocessor(10, 0.5),
    CorePruning(5)
)
dataset = pipeline.process(dataset)
```

## Complete Example

```python
from omnirec import RecSysDataSet
from omnirec.data_loaders.datasets import DataSet
from omnirec.preprocess import (
    Pipe, Subsample, MakeImplicit, CorePruning, UserCrossValidation
)

# Load dataset
dataset = RecSysDataSet.use_dataloader(DataSet.MovieLens100K)

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
