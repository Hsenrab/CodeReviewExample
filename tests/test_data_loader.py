"""Tests for src/data_loader.py."""

from pathlib import Path

import pandas as pd
import pytest

from src.data_loader import (
    NUMERIC_COLUMNS,
    REQUIRED_COLUMNS,
    get_season_vegetables,
    load_vegetables,
)


@pytest.fixture
def vegetables_df() -> pd.DataFrame:
    """Return the bundled vegetables dataset."""
    return load_vegetables()


def test_load_vegetables_returns_dataframe(vegetables_df: pd.DataFrame) -> None:
    """load_vegetables should return a pandas DataFrame."""
    assert isinstance(vegetables_df, pd.DataFrame)


def test_required_columns_present(vegetables_df: pd.DataFrame) -> None:
    """All required columns must exist in the dataset."""
    for col in REQUIRED_COLUMNS:
        assert col in vegetables_df.columns, f"Missing column: {col}"


def test_numeric_columns_are_numeric(vegetables_df: pd.DataFrame) -> None:
    """Numeric columns must have a numeric dtype."""
    for col in NUMERIC_COLUMNS:
        assert pd.api.types.is_numeric_dtype(
            vegetables_df[col]
        ), f"Column '{col}' is not numeric"


def test_dataset_has_minimum_rows(vegetables_df: pd.DataFrame) -> None:
    """Dataset should contain at least 8 vegetables."""
    assert len(vegetables_df) >= 8


def test_load_vegetables_raises_on_missing_file() -> None:
    """load_vegetables should raise FileNotFoundError for a non-existent path."""
    with pytest.raises(FileNotFoundError):
        load_vegetables(Path("/nonexistent/path/vegetables.csv"))


def test_load_vegetables_raises_on_missing_columns(tmp_path: Path) -> None:
    """load_vegetables should raise ValueError when required columns are absent."""
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("name,colour\nCarrot,Orange\n")
    with pytest.raises(ValueError, match="missing required columns"):
        load_vegetables(bad_csv)


def test_get_season_vegetables_filters_correctly(vegetables_df: pd.DataFrame) -> None:
    """get_season_vegetables should return only rows for the requested season."""
    summer_df = get_season_vegetables(vegetables_df, "Summer")
    assert all(summer_df["season"] == "Summer")


def test_get_season_vegetables_returns_dataframe(vegetables_df: pd.DataFrame) -> None:
    """get_season_vegetables should return a DataFrame."""
    result = get_season_vegetables(vegetables_df, "Winter")
    assert isinstance(result, pd.DataFrame)


def test_get_season_vegetables_empty_for_unknown_season(
    vegetables_df: pd.DataFrame,
) -> None:
    """get_season_vegetables should return an empty DataFrame for an unknown season."""
    result = get_season_vegetables(vegetables_df, "Monsoon")
    assert len(result) == 0
