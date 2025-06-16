# RecSysDataSet Class Documentation

## Overview

The `RecSysDataSet` class is the core component of the RecSys Framework, designed to standardize dataset loading, processing, and management for recommender system research. It supports 70+ public explicit feedback datasets and provides a unified interface for data manipulation across different ML libraries (RecBole, LensKit, RecPack).

## Class Structure

### Initialization

```python
dataset = RecSysDataSet(data_set_name)
```

**Parameters:**
- `data_set_name` (str): Name of the dataset (must be from `available_data_sets` list)

**Key Attributes:**
- `data`: pandas DataFrame containing the loaded dataset
- `data_origin`: Current data stage ("raw", "processed", "atomic", or None)
- `meta_data`: Dictionary containing calculated dataset statistics
- `data_splits`: Dictionary containing train/validation/test splits
- `feedback_type`: "explicit" or "implicit" feedback type

## Core Functionality

### 1. Data Loading Functions

#### `load_data(force_load=False)`

Loads dataset from different sources based on the current `data_origin` setting.

**Behavior by Data Origin:**

- **Raw Data (`data_origin = "raw"`)**: 
  - Dynamically imports custom data loaders from `data_loaders/` folder
  - Uses naming convention: `data_loaders.{dataset_name}` module with `{DatasetName}` class
  - Calls loader's `load_from_file()` method with standardized column names
  - Automatically sets feedback type after loading (if ratings exist: explicit, else: implicit)

- **Processed Data (`data_origin = "processed"`)**: 
  - Loads from `./data_sets/{dataset_name}/processed/interactions.csv`
  - Standard CSV format with columns: `user`, `item`, `rating`, `timestamp`

- **Atomic Data (`data_origin = "atomic"`)**: 
  - Loads from `./data_sets/{dataset_name}/atomic/{dataset_name}.inter`
  - RecBole-compatible format with columns: `user_id:token`, `item_id:token`, `rating:float`

**Parameters:**
- `force_load` (bool): If True, forces reloading even if data already loaded

### 2. Data Processing Functions

#### `process_data(force_process=False, drop_duplicates=True, normalize_identifiers=True)`

Converts data between stages with automatic state transitions.

**Raw → Processed Conversion:**
- Creates processed folder structure
- Drops duplicate interactions (keeping last occurrence)
- Normalizes user/item IDs to ascending integers
- Standardizes column order and data types
- Updates `data_origin` to "processed"

**Processed → Atomic Conversion:**
- Creates atomic folder structure  
- Renames columns to RecBole format (`user_id:token`, `item_id:token`, `rating:float`)
- Removes timestamp column
- Updates `data_origin` to "atomic"

**Parameters:**
- `force_process` (bool): Overwrite existing processed/atomic data
- `drop_duplicates` (bool): Remove duplicate user-item interactions
- `normalize_identifiers` (bool): Map IDs to sequential integers

#### `make_implicit(threshold)`

Converts explicit ratings to implicit feedback by filtering ratings above threshold.

**Parameters:**
- `threshold` (int|float): Rating cutoff value. If float (0-1), treated as percentage of rating scale

#### `core_pruning(core)`

Removes users/items with insufficient interactions using k-core decomposition.

**Parameters:**
- `core` (int): Minimum number of interactions required for users and items

#### `subsample(sample_size, random_state=42)`

Reduces dataset size by random sampling.

**Parameters:**
- `sample_size` (int): Number of interactions to keep
- `random_state` (int): Random seed for reproducibility

### 3. Data Splitting Functions

#### `split_data(num_folds=None, valid_size=None, test_size=None, random_state=None)`

Creates train/validation/test splits using different strategies:

- **`random_ho`**: Random holdout split
- **`random_cv`**: Random k-fold cross-validation  
- **`user_ho`**: User-based holdout (per-user splitting)
- **`user_cv`**: User-based k-fold cross-validation

**Parameters:**
- `num_folds` (int): Number of folds for cross-validation
- `valid_size` (float): Proportion for validation set
- `test_size` (float): Proportion for test set
- `random_state` (int): Random seed

#### `write_data_splits(force_write=False)`

Saves data splits to files:
- **Processed**: `train_split.csv`, `valid_split.csv`, `test_split.csv`
- **Atomic**: `{dataset}.train_split.inter`, `{dataset}.valid_split.inter`, `{dataset}.test_split.inter`

#### `load_data_splits(force_load=False)`

Loads previously saved data splits from files.

### 4. Metadata Functions

#### `calculate_metadata(force_calculate=False)`

Computes comprehensive dataset statistics:

```python
{
    "num_users": int,
    "num_items": int, 
    "num_interactions": int,
    "density": float,
    "feedback_type": str,
    "user_item_ratio": float,
    "item_user_ratio": float,
    "highest_num_rating_by_single_user": int,
    "lowest_num_rating_by_single_user": int,
    "highest_num_rating_on_single_item": int,
    "lowest_num_rating_on_single_item": int,
    "mean_num_ratings_by_user": float,
    "mean_num_ratings_on_item": float
}
```

#### `write_metadata(force_write=False)` / `load_metadata(force_load=False)`

Saves/loads metadata to/from JSON files in respective data folders.

### 5. File Management Functions

#### `write_data(force_write=False)`

Saves current dataset to appropriate file based on `data_origin`:
- Processed: `./data_sets/{dataset}/processed/interactions.csv`
- Atomic: `./data_sets/{dataset}/atomic/{dataset}.inter`

#### Path Checking Functions

- `processed_data_exists()` / `atomic_data_exists()`: Check if data files exist
- `processed_folder_exists()` / `atomic_folder_exists()`: Check if folders exist  
- `check_data_loaded()` / `check_data_splits_loaded()`: Check if data is loaded in memory

### 6. Utility Functions

#### `unload_data()`

Clears all loaded data from memory and resets state variables.

#### `clear_data(safety_flag=False)`

**WARNING**: Permanently deletes processed/atomic data files and folders.

- `safety_flag` (bool): 

#### `clear_splits()`

Removes all data split files.

## Usage Examples

### Basic Data Processing Pipeline

```python
# Step 1: Raw to Processed
dataset = RecSysDataSet("MovieLens-100K")
dataset.data_origin = "raw"           # Manual setting required
dataset.process_data()                # Loads, cleans, processes data
dataset.write_data()                  # Saves processed data
dataset.calculate_metadata()          # Computes statistics
dataset.write_metadata()              # Saves metadata

# Step 2: Processed to Atomic  
dataset.data_origin = "processed"     # Manual setting required
dataset.process_data()                # Converts to atomic format
dataset.write_data()                  # Saves atomic data

# Step 3: Create data splits
dataset.data_split_type = "random_cv"
dataset.split_data(num_folds=5, valid_size=0.1, random_state=42)
dataset.write_data_splits()
```

### Data Preprocessing

```python
dataset = RecSysDataSet("MovieLens-100K")
dataset.data_origin = "processed"
dataset.load_data()

# Convert to implicit feedback (ratings >= 4)
dataset.make_implicit(threshold=4)

# Apply 5-core pruning
dataset.core_pruning(core=5)

# Subsample to 10K interactions
dataset.subsample(sample_size=10000)

dataset.write_data()
```

## Supported Datasets

The framework supports 70+ public datasets including:
- **MovieLens**: 100K, 1M, 10M, 20M, 25M, Latest
- **Amazon**: 2014/2018 product categories (Books, Electronics, etc.)
- **Yelp**: 2018-2023 versions
- **Netflix**, **Goodreads**, **Last.FM**, and many more

See [`available_data_sets`](recsys_data_set.py#L15) list for complete catalog.

## File Structure

```
data_sets/
├── {dataset_name}/
│   ├── source/files/          # Raw data files
│   ├── processed/             # Cleaned, standardized data
│   │   ├── interactions.csv
│   │   ├── metadata.json
│   │   ├── processing_log.txt
│   │   └── *_split*.csv       # Data splits
│   └── atomic/                # Algorithm-ready format
│       ├── {dataset}.inter
│       ├── metadata.json
│       ├── processing_log.txt
│       └── *_split*.inter     # Data splits
```

## Integration with ML Libraries

The atomic format is specifically designed for compatibility with:
- **RecBole**: Direct loading of `.inter` files
- **LensKit**: CSV format with proper column naming
- **RecPack**: Standard user-item interaction format

This enables seamless algorithm execution across multiple recommender system libraries.