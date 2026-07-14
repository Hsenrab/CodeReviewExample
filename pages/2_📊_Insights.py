"""Insights page — charts covering key vegetable metrics."""

import plotly.express as px
import streamlit as st

from src.data_loader import load_vegetables

st.set_page_config(
    page_title="Insights | Vegetable Insights Portal",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Vegetable Insights")
st.markdown(
    """
Explore visual insights across our vegetable dataset. The charts below cover calorie
content, vitamin C levels, dietary fibre, seasonal availability, and popularity rankings.
"""
)

try:
    df = load_vegetables()
except (FileNotFoundError, ValueError) as e:
    st.error(f"Could not load vegetable data: {e}")
    st.stop()

# --- Calories ---
st.subheader("Calories per 100g")
st.markdown(
    "Which vegetables are the most calorie-dense? Starchy vegetables like sweetcorn "
    "and parsnip tend to rank higher than leafy greens."
)
fig_cal = px.bar(
    df.sort_values("calories_per_100g", ascending=False),
    x="vegetable",
    y="calories_per_100g",
    color="colour",
    title="Calories per 100g by Vegetable",
    labels={"vegetable": "Vegetable", "calories_per_100g": "Calories (per 100g)"},
)
st.plotly_chart(fig_cal, use_container_width=True)

# --- Vitamin C ---
st.subheader("Vitamin C per 100g")
fig_vitc = px.bar(
    df.sort_values("vitamin_c_mg_per_100g", ascending=False),
    x="vegetable",
    y="vitamin_c_mg_per_100g",
    color="colour",
    title="Vitamin C (mg) per 100g by Vegetable",
    labels={"vegetable": "Vegetable", "vitamin_c_mg_per_100g": "Vitamin C (mg per 100g)"},
)
st.plotly_chart(fig_vitc, use_container_width=True)

# --- Fibre ---
st.subheader("Fibre per 100g")
st.markdown(
    "Dietary fibre content per 100g. High-fibre vegetables support digestive health "
    "and help maintain satiety."
)
fig_fibre = px.bar(
    df.sort_values("fibre_g_per_100g", ascending=False),
    x="vegetable",
    y="fibre_g_per_100g",
    color="colour",
    title="Fibre (g) per 100g by Vegetable",
    labels={"vegetable": "Vegetable", "fibre_g_per_100g": "Fibre (g per 100g)"},
)
st.plotly_chart(fig_fibre, use_container_width=True)

# --- Seasonal availability ---
st.subheader("Seasonal Availability")
st.markdown(
    "How many vegetables from our dataset are available in each season? "
    "This chart shows the seasonal distribution across the year."
)
season_counts = df.groupby("season").size().reset_index(name="count")
fig_season = px.pie(
    season_counts,
    names="season",
    values="count",
    title="Vegetable Count by Season",
)
st.plotly_chart(fig_season, use_container_width=True)

# --- Popularity ---
st.subheader("Popularity Scores")
st.markdown(
    "Popularity scores reflect how well-known and widely enjoyed each vegetable is "
    "in everyday cooking. Higher scores indicate broader appeal."
)
fig_pop = px.bar(
    df.sort_values("popularity_score", ascending=False),
    x="vegetable",
    y="popularity_score",
    color="colour",
    title="Popularity Score by Vegetable",
    labels={"vegetable": "Vegetable", "popularity_score": "Popularity Score"},
)
st.plotly_chart(fig_pop, use_container_width=True)

st.markdown("---")
st.caption("Data is approximate and for demonstration purposes only.")
