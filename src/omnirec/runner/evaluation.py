import json
import sys
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd
from pandas import DataFrame
from rich.table import Table

from omnirec.metrics.base import Metric
from omnirec.util import util

logger = util._root_logger.getChild("eval")


EvaluationColumns = ["algorithm", "fold", "name", "k", "value"]
ColumnStyles = {"algorithm": "cyan", "fold": "magenta"}


class Evaluator:
    def __init__(self, *metrics: Metric) -> None:
        """Initialize the Evaluator with metrics to compute on predictions.
        The Evaluator computes specified metrics on algorithm predictions and accumulates
        results across experiments. Use `get_tables()` to retrieve formatted result tables.

        Args:
            *metrics (Metric): One or more metric instances to compute. Common metrics include
                NDCG, HR (Hit Rate), and Recall. Each metric can be configured with multiple
                k values (e.g., `NDCG([5, 10, 20])`).
        """
        if not isinstance(metrics, Iterable):
            metrics = [metrics]
        self._metrics = metrics
        self._results: dict[str, DataFrame] = {}

    def run_evaluation(
        self,
        dataset: str,
        algorithm: str,
        predictions: DataFrame,
        test: DataFrame,
        fold: Optional[int] = None,
    ):
        old_df = self._results.get(dataset)
        if old_df is not None:
            if algorithm in old_df["algorithm"].values:
                logger.warning(
                    f"{algorithm} already evaluated on {dataset}! Skipping..."
                )

        new_rows = []

        for m in self._metrics:
            mr = m.calculate(predictions, test)
            name = mr.name
            value = mr.result
            if isinstance(value, dict):
                for k, v in value.items():
                    new_rows.append((algorithm, fold, name, k, v))
            elif isinstance(value, float):
                new_rows.append((algorithm, fold, name, None, value))
            else:
                logger.critical(f"Invalid result type: {type(value)}")
                sys.exit(1)

        new_df = DataFrame(new_rows, columns=EvaluationColumns)
        if old_df is None:
            self._results[dataset] = new_df
        else:
            self._results[dataset] = pd.concat((old_df, new_df))

    def get_tables(self) -> list[Table]:
        tables: list[Table] = []

        for dataset, results_df in self._results.items():
            df = results_df.copy()
            # Combine name and k only if k is not None
            df["name"] = df.apply(
                lambda r: f"{r['name']}@{r['k']}" if pd.notna(r["k"]) else r["name"],
                axis=1,
            )

            # Only keep fold if it actually varies
            if df["fold"].nunique() > 1:
                index_cols = ["algorithm", "fold"]
            else:
                index_cols = ["algorithm"]

            df_pivot = (
                df.pivot(index=index_cols, columns="name", values="value")
                .reset_index()
                .sort_values(index_cols)
            )

            table = Table(title=f"{dataset}: Evaluation Results")
            for col in df_pivot.columns:
                col_str = str(col)
                if col_str in ["algorithm", "fold"]:
                    col_str = col_str.capitalize()
                table.add_column(
                    col_str, style=ColumnStyles.get(col), footer="test footer"
                )

            prev_alg, prev_fold = None, None
            for _, row in df_pivot.iterrows():
                alg = row["algorithm"] if row["algorithm"] != prev_alg else ""
                row_values = [alg]
                if "fold" in row:
                    fold = (
                        str(row["fold"])
                        if row["fold"] != prev_fold or alg != ""
                        else ""
                    )
                    row_values.append(fold)
                    prev_fold = row["fold"]
                    start_col = 2
                else:
                    start_col = 1
                prev_alg = row["algorithm"]
                row_values.extend(
                    [str(row[col]) for col in df_pivot.columns[start_col:]]
                )
                table.add_row(*row_values)

            tables.append(table)

        return tables

    def save_results(self, path: Path):
        data = {k: v.to_dict("records") for k, v in self._results.items()}
        path.write_text(json.dumps(data))

    def load_results(self, path: Path):
        js = json.loads(path.read_text())
        self._results = {k: pd.DataFrame(v) for k, v in js.items()}
