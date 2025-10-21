# Loading Datasets
This section explains how to load and save datasets, what datasets are available and how to register and implement your own data loader.

## RecSysDataSet Class

The core of the framework's data model is the [`RecSysDataSet`](API_references.md#omnirec.recsys_data_set.RecSysDataSet) class. This generic class provides a unified interface for handling different types of recommendation system datasets.

The [`RecSysDataSet`](API_references.md#omnirec.recsys_data_set.RecSysDataSet) can contain one of three different variants of data:

- **RawData**: Contains a single pandas DataFrame with all interactions
- **SplitData**: Contains train, validation, and test DataFrames 
- **FoldedData**: Contains multiple folds, each with their own train/validation/test splits

### Data Structure

All datasets follow a standardized column structure:

- `user`: User identifier (normalized to integers starting from 0)
- `item`: Item identifier (normalized to integers starting from 0)
- `rating`: Rating value (explicit feedback) or 1 (implicit feedback)
- `timestamp`: Unix timestamp of the interaction

## Using Built-in Data Loaders

The recommended way to load datasets is using the [`use_dataloader`](API_references.md#omnirec.recsys_data_set.RecSysDataSet.use_dataloader) method with registered data loaders:

```python
from omnirec import RecSysDataSet

# Load MovieLens 100K dataset
dataset = RecSysDataSet.use_dataloader("MovieLens100K")

# Force re-download and re-canonicalization
dataset = RecSysDataSet.use_dataloader(
    "MovieLens100K", 
    force_download=True, 
    force_canonicalize=True
)

# Specify custom paths
dataset = RecSysDataSet.use_dataloader(
    "MovieLens100K",
    raw_dir="/path/to/raw/data",
    canon_path="/path/to/canonicalized/data.csv"
)
```

The data loading process includes:
1. **Download**: Raw data is downloaded if not already present
2. **Canonicalization**: Data is cleaned and standardized:
   - Duplicate interactions are removed (keeping the latest)
   - User and item identifiers are normalized to consecutive integers
   - Data is saved in a standardized CSV format

### Dataset Statistics

You can get basic statistics about loaded datasets:

```python
# Get number of interactions
num_interactions = dataset.num_interactions()

# Get rating range (for explicit feedback datasets)
min_rating = dataset.min_rating()
max_rating = dataset.max_rating()
```

### Saving and Loading Datasets

Save any [`RecSysDataSet`](API_references.md#omnirec.recsys_data_set.RecSysDataSet) object to a compressed `.rsds` file with the [`save()`](API_references.md#omnirec.recsys_data_set.RecSysDataSet.save) function:

```python
# Save to file (extension .rsds will be added automatically)
dataset.save("my_dataset")

# Or specify full path
dataset.save("/path/to/my_dataset.rsds")
```

The save format preserves:
- All data variants (Raw, Split, or Folded)
- Metadata about the dataset
- Version information for compatibility

You can load previously saved datasets with the [`load()`](API_references.md#omnirec.recsys_data_set.RecSysDataSet.load) function:

```python
# Load from .rsds file
dataset = RecSysDataSet.load("my_dataset.rsds")
```

## Data Variants

**RawData**

Contains all interactions in a single DataFrame:

```python
# Access the DataFrame
df = dataset._data.df
print(f"Dataset has {len(df)} interactions")
```

**SplitData**

Contains separate train, validation, and test sets:

```python
# Access individual splits
train_df = dataset._data.get("train")
val_df = dataset._data.get("val")
test_df = dataset._data.get("test")
```

**FoldedData**

Contains multiple folds for cross-validation:

```python
# Access folds
for fold_idx, split_data in dataset._data.folds.items():
    print(f"Fold {fold_idx}:")
    print(f"  Train: {len(split_data.train)} interactions")
    print(f"  Val: {len(split_data.val)} interactions") 
    print(f"  Test: {len(split_data.test)} interactions")
```

## Loading Custom Datasets

**Creating Custom Data Loaders**

To implement a custom data loader, create a class that inherits from [`Loader`](API_references.md#omnirec.data_loaders.base.Loader) and implement the [`info()`](API_references.md#omnirec.data_loaders.base.Loader.info) and [`load()`](API_references.md#omnirec.data_loaders.base.Loader.load) function:

```python
from pathlib import Path
import pandas as pd
from omnirec.data_loaders.base import Loader, DatasetInfo
from omnirec.data_loaders.registry import register_dataloader

class MyCustomLoader(Loader):
    @staticmethod
    def info(name: str) -> DatasetInfo:
        return DatasetInfo(
            download_urls="https://example.com/dataset.zip",
            checksum="sha256_checksum_here"  # Optional but recommended
        )
    
    @staticmethod
    def load(source_dir: Path, name: str) -> pd.DataFrame:
        # Implement your loading logic here
        # Must return DataFrame with columns: user, item, rating, timestamp
        df = pd.read_csv(source_dir / "data.csv")
        # Process and return standardized DataFrame
        return df

# Register the loader
register_dataloader("MyDataset", MyCustomLoader)

# Now you can use it
dataset = RecSysDataSet.use_dataloader("MyDataset")
```

**Loader Registration**

You can register loaders under multiple names using [`register_dataloader()`](API_references.md#omnirec.data_loaders.registry.register_dataloader):

```python
# Register under multiple names
register_dataloader(["Dataset1", "Dataset2", "AliasName"], MyCustomLoader)
```

**DatasetInfo**

The [`DatasetInfo`](API_references.md#omnirec.data_loaders.base.DatasetInfo) class provides metadata about your dataset:

- `download_urls`: URL(s) to download the dataset (string or list of strings)
- `checksum`: Optional SHA256 checksum for integrity verification

If multiple URLs are provided, they are tried in order until one succeeds.
