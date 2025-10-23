# Welcome to OmniRec

# Overview

Welcome to the OmniRec documentation! OmniRec is an open-source Python library designed to be an all-in-one solution for reproducible and interoperable recommender systems experimentation. You can download the full demo paper <a href="assets/OmniRec_Demo_.pdf">here</a> and access the source code at our <a href="https://github.com/ISG-Siegen/OmniRec">GitHub repository</a>.

Recommender systems research often faces challenges like fragmented data handling, inconsistent preprocessing, and poor interoperability between different toolkits. These issues can make it difficult to compare results and reproduce studies, slowing down scientific progress. OmniRec tackles these problems by providing a unified, transparent, and easy-to-use workflow for the entire experimentation process.

## Key Features

* **Massive Dataset Collection**: Get standardized access to over 230 datasets right out of the box.
* **Unified Preprocessing**: Define your data cleaning, filtering, and splitting pipeline just once and apply it consistently across different models and frameworks.
* **Seamless Integration**: OmniRec works with multiple state-of-the-art recommender system frameworks, including **RecPack**, **RecBole**, **Lenskit**, and **Elliot**.
* **Extensible by Design**: Its modular architecture allows you to easily add new datasets, custom preprocessing steps, or interfaces to other frameworks.

---

## Architecture

OmniRec's power comes from its simple yet flexible architecture, which is organized into four interconnected modules. This design enables a smooth end-to-end workflow from loading data to evaluating model performance.

<img src="assets/Flowchart_OmniRec.png" width="100%" height="600px" title="Diagram showing the OmniRec architecture" alt="Diagram showing the OmniRec architecture" />

<p>Click <a href="assets/Flowchart_OmniRec.pdf">here</a> to download the PDF.</p>

*The OmniRec architecture, showing its four main components and the experimental workflow.*

Here’s a brief look at each component:

### 1. Data Loader

The **Data Loader** is your starting point. It provides a simple way to load any of the registered datasets or even your own custom data. To ensure consistency, it performs initial preparations like removing duplicate interactions and normalizing user and item identifiers. It also exposes key dataset statistics, which are crucial for analysis and reproducible reporting.

### 2. Preprocessing Pipeline

Once your data is loaded, the **Preprocessing Pipeline** applies all the transformations you need. You can easily perform common operations such as:
* Subsampling and k-core filtering
* Converting explicit feedback (e.g., ratings) to implicit feedback (e.g., clicks)
* Splitting data into training and testing sets using various strategies like random holdout, time-based holdout, or cross-validation.

The best part is that this pipeline is completely customizable, so you can add your own functions with minimal effort.

### 3. Recommender Interface

This is where the magic of interoperability happens. The **Recommender Interface** takes your preprocessed data and seamlessly exports it to widely-used recommender frameworks like Lenskit, RecPack, RecBole, and Elliot. This allows you to train models and generate predictions using the specific tools you need, all without having to rewrite your data preparation code. OmniRec even handles the Python environments for each library to solve dependency conflicts.

### 4. Evaluator

Finally, the **Evaluator** module provides a standardized way to assess your model's performance. It computes common ranking and rating-based metrics like nDCG@k, Recall@k, and RMSE. By centralizing the evaluation logic, OmniRec ensures that results are always comparable, no matter which underlying framework you used to train the model. All results can be stored with complete metadata, guaranteeing traceability and long-term reproducibility.