from dataclasses import dataclass
from enum import StrEnum, auto

import pandas as pd
import pandera.pandas as pa


class ValidationFailureMode(StrEnum):
    RAISE = auto()
    WARN = auto()
    SKIP = auto()


@dataclass
class ValidationRule:
    schema: pa.DataFrameSchema | type[pa.DataFrameModel]
    on_error: ValidationFailureMode = ValidationFailureMode.RAISE
    message: str | None = None

    def is_valid(
        self,
        df: pd.DataFrame,
        df_name: str = "Unnamed",
        dataset_name: str = "UnnamedDataset",
    ) -> tuple[bool, str | None]:
        context = f"{dataset_name}/{df_name}"
        try:
            self.schema.validate(df, lazy=True)
        except pa.errors.SchemaErrors as e:
            if self.message is not None:
                msg = f"{context}: {self.message}"
            else:
                fc: pd.DataFrame = e.failure_cases

                if fc.empty:
                    msg = f"{context}: schema validation failed."
                else:
                    issues = (
                        fc.assign(
                            issue_target=fc["column"]
                            .where(fc["column"].notna(), fc["failure_case"])
                            .fillna("<schema>")
                        )
                        .groupby(
                            ["schema_context", "issue_target", "check"],
                            dropna=False,
                        )
                        .size()
                        .reset_index(name="count")
                    )

                    first = issues.iloc[0]
                    col = first["issue_target"]
                    check = first["check"]
                    count = int(first["count"])
                    more = len(issues) - 1

                    msg = f"{context}: '{col}' failed {check} ({count} failing rows)"
                    if more:
                        msg += f"\n +{more} more issue(s)"

            return False, msg

        return True, None


class PreprocessorValidationError(Exception):
    pass
