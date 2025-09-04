# Getting Started

In this guide we will present how to install OmniRec and to design and implement your first experiments with it.

## Installation

<!-- TODO: Fill in python version and install command -->
First you need to setup a python environment at least python <\version> and install the OmniRec libary by running <\command>.

## Loading datasets

Central part of the recsyslib library is the [`RecSysDataSet`](API_references.md#recsyslib.RecSysDataSet) class. It loads the data in an object of this class by calling the static [`use_dataloader()`](API_references.md#recsyslib.RecSysDataSet.use_dataloader) function that return a [`RecSysDataSet`](API_references.md#recsyslib.RecSysDataSet) object. If provided a registered data set name [`use_dataloader()`](API_references.md#recsyslib.RecSysDataSet.use_dataloader) downloads the data set, removes duplicates and normalizes the identifiers:

```python
from OmniRec import RedSysDataSet
data = RecSysDataSet.use_dataloader(data_set_name="MovieLens100K")
```
We provide a more detailed documentation [here](loading_datasets.md).

## Preprocessing Datasets

We can now apply the desired preprocessing steps to the data. The easiest way is to define a preprocessing pipeline:

<!-- TODO: Change imports according to final project structure -->

```python
from recsyslib.preprocess.core_pruning import CorePruning
from recsyslib.preprocess.feedback_conversion import MakeImplicit
from recsyslib.preprocess.pipe import Pipe
from recsyslib.preprocess.split import UseCrossValidation

pipe = Pipe[FoldedData](
    Subsample(sample_size=0.1),
    MakeImplicit(threshold=3),
    CorePruning(core=5),
    UserCrossValidation(num_folds=5, validation_size=0.1),
)
data = pipe.process(data)
```

<!-- TODO: Add links to API reference when avaliable -->

The `pipe.process()` function interatively executes the preprocessing steps. 

Alternatively, this can be done step by step by creating a single preprocessing step and calling `process()` on it:

```python
step = Subsample(sample_size=0.1)
data = step.process(dataset=data)
```

More details about the available preprocessing steps can be found [here](preprocessing.md).