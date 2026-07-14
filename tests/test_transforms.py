"""Tests for src/transforms.py."""

import pandas as pd
import pytest

from src.transforms import format_popularity, get_nutrient_summary, top_vegetables_by_nutrient


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Return a small representative vegetable DataFrame for testing."""
    return pd.DataFrame(
        {
            "vegetable": ["Carrot", "Broccoli", "Pea", "Tomato", "Kale"],
            "colour": ["Orange", "Green", "Green", "Red", "Green"],
            "calories_per_100g": [41, 34, 81, 18, 49],
            "vitamin_c_mg_per_100g": [5.9, 89.2, 40.0, 13.7, 120.0],
            "fibre_g_per_100g": [2.8, 2.6, 5.1, 1.2, 3.6],
            "season": ["Autumn", "Winter", "Spring", "Summer", "Winter"],
            "popularity_score": [8.2, 7.8, 7.9, 9.1, 6.2],
        }
    )


class TestGetNutrientSummary:
    def test_returns_dataframe(self, sample_df: pd.DataFrame) -> None:
        result = get_nutrient_summary(sample_df)
        assert isinstance(result, pd.DataFrame)

    def test_has_expected_index(self, sample_df: pd.DataFrame) -> None:
        result = get_nutrient_summary(sample_df)
        assert set(result.index) == {"mean", "min", "max"}

    def test_mean_calories_correct(self, sample_df: pd.DataFrame) -> None:
        result = get_nutrient_summary(sample_df)
        expected = round((41 + 34 + 81 + 18 + 49) / 5, 2)
        assert result.loc["mean", "calories_per_100g"] == expected

    def test_min_and_max_calories(self, sample_df: pd.DataFrame) -> None:
        result = get_nutrient_summary(sample_df)
        assert result.loc["min", "calories_per_100g"] == 18
        assert result.loc["max", "calories_per_100g"] == 81


class TestFormatPopularity:
    def test_very_popular_boundary(self) -> None:
        assert "Very Popular" in format_popularity(8.0)

    def test_very_popular_above_boundary(self) -> None:
        assert "Very Popular" in format_popularity(9.5)

    def test_popular_range(self) -> None:
        assert "Popular" in format_popularity(7.0)

    def test_popular_lower_boundary(self) -> None:
        assert "Popular" in format_popularity(6.5)

    def test_niche_favourite(self) -> None:
        assert "Niche Favourite" in format_popularity(5.5)

    def test_returns_string(self) -> None:
        assert isinstance(format_popularity(7.5), str)

    def test_score_appears_in_output(self) -> None:
        result = format_popularity(7.3)
        assert "7.3" in result


class TestTopVegetablesByNutrient:
    def test_returns_correct_count(self, sample_df: pd.DataFrame) -> None:
        result = top_vegetables_by_nutrient(sample_df, "vitamin_c_mg_per_100g", n=3)
        assert len(result) == 3

    def test_sorted_descending(self, sample_df: pd.DataFrame) -> None:
        result = top_vegetables_by_nutrient(sample_df, "calories_per_100g")
        assert result["calories_per_100g"].is_monotonic_decreasing

    def test_default_n_is_five(self, sample_df: pd.DataFrame) -> None:
        result = top_vegetables_by_nutrient(sample_df, "calories_per_100g")
        assert len(result) == 5

    def test_returns_dataframe(self, sample_df: pd.DataFrame) -> None:
        result = top_vegetables_by_nutrient(sample_df, "fibre_g_per_100g", n=2)
        assert isinstance(result, pd.DataFrame)

    def test_contains_vegetable_and_nutrient_columns(
        self, sample_df: pd.DataFrame
    ) -> None:
        result = top_vegetables_by_nutrient(sample_df, "fibre_g_per_100g", n=2)
        assert "vegetable" in result.columns
        assert "fibre_g_per_100g" in result.columns
