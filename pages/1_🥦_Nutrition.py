"""Nutrition page — full nutritional breakdown per vegetable."""

import streamlit as st

from src.data_loader import load_vegetables
from src.transforms import format_popularity

st.set_page_config(
    page_title="Nutrition | Vegetable Insights Portal",
    page_icon="🥦",
    layout="wide",
)

st.title("🥦 Nutrition Data")
st.markdown(
    """
Browse the full nutritional profile for each vegetable in our dataset.
Columns include calories, vitamin C, and dietary fibre per 100g, along with
seasonal availability and a crowd-sourced popularity score.
"""
)

try:
    df = load_vegetables()
except (FileNotFoundError, ValueError) as e:
    st.error(f"Could not load vegetable data: {e}")
    st.stop()

display_df = df.copy()
display_df["popularity"] = display_df["popularity_score"].apply(format_popularity)
display_df = display_df.drop(columns=["popularity_score"])
display_df = display_df.rename(
    columns={
        "vegetable": "Vegetable",
        "colour": "Colour",
        "calories_per_100g": "Calories (per 100g)",
        "vitamin_c_mg_per_100g": "Vitamin C mg (per 100g)",
        "fibre_g_per_100g": "Fibre g (per 100g)",
        "season": "Season",
        "popularity": "Popularity",
    }
)

st.dataframe(display_df, use_container_width=True)

st.markdown("---")
st.caption("Data is approximate and for demonstration purposes only.")
