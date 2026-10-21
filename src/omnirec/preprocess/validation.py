from dataclasses import dataclass
from enum import StrEnum, auto

import pandas as pd
import pandera.pandas as pa


class ValidationFailureMode(StrEnum):
    """Action taken by a preprocessor when an input validation rule fails.

    Attributes:
        RAISE: Raise PreprocessorValidationError and stop processing.
        WARN: Log a warning and continue validation and processing.
        SKIP: Log a warning and return the original dataset without processing
            or adding a lineage entry.
    """

    RAISE = auto()
    WARN = auto()
    SKIP = auto()


@dataclass
class ValidationRule:
    """A Pandera input schema and its failure policy.

    Args:
        schema: A Pandera DataFrameSchema instance or DataFrameModel class.
        on_error: How the preprocessor handles a failed check. Defaults to RAISE.
        message: Optional replacement for the generated failure summary.
            The dataset and DataFrame names are still included for context.
    """

    schema: pa.DataFrameSchema | type[pa.DataFrameModel]
    on_error: ValidationFailureMode = ValidationFailureMode.RAISE
    message: str | None = None

    def is_valid(
        self,
        df: pd.DataFrame,
        df_name: str = "Unnamed",
        dataset_name: str = "UnnamedDataset",
    ) -> tuple[bool, str | None]:
        """Check a DataFrame without replacing it with Pandera's validated output.

        Args:
            df: Input DataFrame to check using lazy validation.
            df_name: Frame name, such as raw, train, or fold_0/test.
            dataset_name: Dataset name used in error messages.

        Returns:
            tuple[bool, str | None]: True and None on success, or False and a
                failure summary on a Pandera SchemaErrors exception. This method
                does not apply the failure policy; the preprocessor does that.
        """
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
    """Raised when a preprocessing input fails a rule with RAISE mode."""
