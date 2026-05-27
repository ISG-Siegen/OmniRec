import logging

import pandera.pandas as pa
import pytest
from pandera.typing import Series

from omnirec.data_variants import RawData, SplitData
from omnirec.preprocess.base import Preprocessor
from omnirec.preprocess.validation import (
    PreprocessorValidationError,
    ValidationFailureMode,
    ValidationRule,
)
from omnirec.recsys_data_set import RecSysDataSet
from tests.conftest import MakeDataset


class RecordingRawPreprocessor(Preprocessor[RawData, RawData]):
    def __init__(self, rules: list[ValidationRule]) -> None:
        self._rules = rules
        self.process_called = False
        super().__init__()

    def validation_rules(self) -> list[ValidationRule]:
        return self._rules

    def _process(self, dataset: RecSysDataSet[RawData]) -> RecSysDataSet[RawData]:
        self.process_called = True
        return dataset


class RecordingSplitPreprocessor(Preprocessor[SplitData, SplitData]):
    def __init__(self, rules: list[ValidationRule]) -> None:
        self._rules = rules
        self.process_called = False
        super().__init__()

    def validation_rules(self) -> list[ValidationRule]:
        return self._rules

    def _process(self, dataset: RecSysDataSet[SplitData]) -> RecSysDataSet[SplitData]:
        self.process_called = True
        return dataset


class ValidRawModel(pa.DataFrameModel):
    user: Series[int]
    item: Series[int]
    rating: Series[float] = pa.Field(gt=0)
    timestamp: Series[int]


def make_valid_rule() -> ValidationRule:
    return ValidationRule(
        pa.DataFrameSchema(
            {
                "user": pa.Column(int),
                "item": pa.Column(int),
                "rating": pa.Column(float, pa.Check.ge(1)),
                "timestamp": pa.Column(int),
            }
        )
    )


def make_missing_column_rule(
    on_error: ValidationFailureMode,
    message: str | None = None,
) -> ValidationRule:
    return ValidationRule(
        pa.DataFrameSchema({"another": pa.Column(str)}),
        on_error=on_error,
        message=message,
    )


def make_multi_issue_rule() -> ValidationRule:
    return ValidationRule(
        pa.DataFrameSchema(
            {
                "rating": pa.Column(float, pa.Check.gt(10)),
                "another": pa.Column(str),
                "another1": pa.Column(str),
                "another2": pa.Column(str),
                "another3": pa.Column(str),
            }
        )
    )


def test_process_runs_when_validation_succeeds(make_dataset: MakeDataset[RawData]):
    ds = make_dataset(RawData)
    preprocessor = RecordingRawPreprocessor([make_valid_rule()])

    result = preprocessor.process(ds)

    assert result is ds
    assert preprocessor.process_called
    assert len(result.lineage) == 1
    assert result.lineage[0].component == "RecordingRawPreprocessor"


def test_validation_rule_generates_concise_message_and_counts_issues_separately(
    make_dataset: MakeDataset[RawData],
):
    ds = make_dataset(RawData)
    is_valid, msg = make_multi_issue_rule().is_valid(ds._data.df, "raw", ds._meta.name)

    assert not is_valid
    assert msg is not None
    assert msg.startswith("TestDataset/raw: ")
    assert "+4 more issue(s)" in msg
    assert "failure cases:" not in msg


def test_validation_rule_custom_message_takes_precedence(
    make_dataset: MakeDataset[RawData],
):
    ds = make_dataset(RawData)
    rule = ValidationRule(
        make_multi_issue_rule().schema,
        message="custom validation message",
    )

    is_valid, msg = rule.is_valid(ds._data.df, "raw", ds._meta.name)

    assert not is_valid
    assert msg == "TestDataset/raw: custom validation message"


def test_raise_mode_raises_validation_error(make_dataset: MakeDataset[RawData]):
    ds = make_dataset(RawData)
    preprocessor = RecordingRawPreprocessor(
        [
            make_missing_column_rule(
                ValidationFailureMode.RAISE,
                message="required column 'another' is missing",
            )
        ]
    )

    with pytest.raises(PreprocessorValidationError) as exc_info:
        preprocessor.process(ds)

    assert (
        str(exc_info.value) == "TestDataset/raw: required column 'another' is missing"
    )
    assert not preprocessor.process_called
    assert len(ds.lineage) == 0


def test_warn_mode_logs_and_continues(
    make_dataset: MakeDataset[RawData], caplog: pytest.LogCaptureFixture
):
    ds = make_dataset(RawData)
    preprocessor = RecordingRawPreprocessor(
        [
            make_missing_column_rule(
                ValidationFailureMode.WARN,
                message="required column 'another' is missing",
            )
        ]
    )
    caplog.set_level(logging.WARNING, logger="omnirec.preprocess")

    result = preprocessor.process(ds)

    assert result is ds
    assert preprocessor.process_called
    assert len(result.lineage) == 1
    assert len(caplog.records) == 1
    assert "TestDataset/raw: required column 'another' is missing" in caplog.text
    assert "Continuing anyway." in caplog.text


def test_skip_mode_logs_and_returns_without_processing(
    make_dataset: MakeDataset[RawData], caplog: pytest.LogCaptureFixture
):
    ds = make_dataset(RawData)
    preprocessor = RecordingRawPreprocessor(
        [
            make_missing_column_rule(
                ValidationFailureMode.SKIP,
                message="required column 'another' is missing",
            )
        ]
    )
    caplog.set_level(logging.WARNING, logger="omnirec.preprocess")

    result = preprocessor.process(ds)

    assert result is ds
    assert not preprocessor.process_called
    assert len(result.lineage) == 0
    assert len(caplog.records) == 1
    assert "TestDataset/raw: required column 'another' is missing" in caplog.text
    assert "Skipping RecordingRawPreprocessor" in caplog.text


def test_validation_runs_on_each_split_dataframe(
    make_dataset: MakeDataset[SplitData], caplog: pytest.LogCaptureFixture
):
    ds = make_dataset(SplitData)
    preprocessor = RecordingSplitPreprocessor(
        [
            make_missing_column_rule(
                ValidationFailureMode.WARN,
                message="required column 'another' is missing",
            )
        ]
    )
    caplog.set_level(logging.WARNING, logger="omnirec.preprocess")

    result = preprocessor.process(ds)

    assert result is ds
    assert preprocessor.process_called
    assert len(result.lineage) == 1
    assert len(caplog.records) == 3
    for split_name in ("train", "validation", "test"):
        assert f"TestDataset/{split_name}: required column 'another' is missing" in (
            caplog.text
        )


def test_validation_rule_supports_dataframe_model(
    make_dataset: MakeDataset[RawData],
):
    ds = make_dataset(RawData)
    preprocessor = RecordingRawPreprocessor([ValidationRule(ValidRawModel)])

    result = preprocessor.process(ds)

    assert result is ds
    assert preprocessor.process_called
    assert len(result.lineage) == 1
