"""Comparison page — summary statistics and side-by-side vegetable comparisons."""

import pandas as pd
import streamlit as st

from src.data_loader import load_vegetables
from src.transforms import get_nutrient_summary

st.set_page_config(
    page_title="Comparison | Vegetable Insights Portal",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 Data Comparison")

try:
    df = load_vegetables()
except (FileNotFoundError, ValueError) as e:
    st.error(f"Could not load vegetable data: {e}")
    st.stop()

# --- Summary statistics ---
st.subheader("Nutrient Summary Statistics")
summary = get_nutrient_summary(df)
st.dataframe(summary, use_container_width=True)

# --- Filter by season ---
st.subheader("Filter by Season")
seasons = df["season"].unique().tolist()
selected = st.selectbox("Choose a season", seasons)
filtered = df[df["season"] == selected]

st.dataframe(
    filtered[
        [
            "vegetable",
            "colour",
            "calories_per_100g",
            "vitamin_c_mg_per_100g",
            "fibre_g_per_100g",
            "popularity_score",
        ]
    ],
    use_container_width=True,
)

# --- Side-by-side comparison ---
st.subheader("Side-by-Side Comparison")
st.markdown("Select two vegetables to compare their nutritional profiles directly.")

veg_options = df["vegetable"].tolist()
col1, col2 = st.columns(2)
with col1:
    veg_a = st.selectbox("Vegetable A", veg_options, index=0)
with col2:
    veg_b = st.selectbox("Vegetable B", veg_options, index=1)

row_a = df[df["vegetable"] == veg_a].iloc[0]
row_b = df[df["vegetable"] == veg_b].iloc[0]

comparison = pd.DataFrame(
    {
        "Metric": [
            "Calories (per 100g)",
            "Vitamin C mg (per 100g)",
            "Fibre g (per 100g)",
            "Popularity Score",
        ],
        veg_a: [
            row_a["calories_per_100g"],
            row_a["vitamin_c_mg_per_100g"],
            row_a["fibre_g_per_100g"],
            row_a["popularity_score"],
        ],
        veg_b: [
            row_b["calories_per_100g"],
            row_b["vitamin_c_mg_per_100g"],
            row_b["fibre_g_per_100g"],
            row_b["popularity_score"],
        ],
    }
)
st.dataframe(comparison, use_container_width=True)

st.markdown("---")
st.caption("Data is approximate and for demonstration purposes only.")
