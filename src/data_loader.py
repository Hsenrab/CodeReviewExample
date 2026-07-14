"""Data loading utilities for the Vegetable Insights Portal.

All functions that read from disk or validate the dataset should live here,
keeping Streamlit pages free of I/O and validation logic.
"""

from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).parent.parent / "data" / "vegetables.csv"

REQUIRED_COLUMNS = [
    "vegetable",
    "colour",
    "calories_per_100g",
    "vitamin_c_mg_per_100g",
    "fibre_g_per_100g",
    "season",
    "popularity_score",
]

NUMERIC_COLUMNS = [
    "calories_per_100g",
    "vitamin_c_mg_per_100g",
    "fibre_g_per_100g",
    "popularity_score",
]


def load_vegetables(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the vegetable dataset from a CSV file.

    Args:
        path: Path to the CSV file. Defaults to the bundled data/vegetables.csv.

    Returns:
        DataFrame containing vegetable nutrition and metadata.

    Raises:
        FileNotFoundError: If the CSV file cannot be found at the given path.
        ValueError: If required columns are missing from the dataset.
    """
    if not path.exists():
        raise FileNotFoundError(f"Vegetable data file not found: {path}")

    df = pd.read_csv(path)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    return df


def get_season_vegetables(df: pd.DataFrame, season) -> pd.DataFrame:
    """Return rows from the dataset matching the given season.

    Args:
        df: The vegetables DataFrame.
        season: The season name to filter by (e.g. 'Summer').

    Returns:
        Filtered DataFrame containing only vegetables available in that season.
    """
    return df[df["season"] == season]
