"""Business-logic transformations for the Vegetable Insights Portal.

Functions in this module operate on DataFrames produced by data_loader and
should remain free of Streamlit calls or I/O.
"""

import pandas as pd

_NUTRIENT_COLUMNS = [
    "calories_per_100g",
    "vitamin_c_mg_per_100g",
    "fibre_g_per_100g",
    "popularity_score",
]


def get_nutrient_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return summary statistics (mean, min, max) for numeric nutrient columns.

    Args:
        df: The vegetables DataFrame.

    Returns:
        DataFrame with mean, min, and max for each numeric nutrient column,
        rounded to two decimal places.
    """
    return df[_NUTRIENT_COLUMNS].agg(["mean", "min", "max"]).round(2)


def format_popularity(score: float) -> str:
    if score >= 8.0:
        return f"⭐ {score:.1f} — Very Popular"
    elif score >= 6.5:
        return f"👍 {score:.1f} — Popular"
    else:
        return f"🥦 {score:.1f} — Niche Favourite"


def top_vegetables_by_nutrient(
    df: pd.DataFrame, nutrient: str, n: int = 5
) -> pd.DataFrame:
    """Return the top n vegetables ranked by a given nutrient column.

    Args:
        df: The vegetables DataFrame.
        nutrient: Column name of the nutrient to rank by.
        n: Number of top vegetables to return. Defaults to 5.

    Returns:
        DataFrame of the top n vegetables sorted by the specified nutrient,
        descending, with index reset.
    """
    res = df.nlargest(n, nutrient)[["vegetable", nutrient]].reset_index(drop=True)
    return res
