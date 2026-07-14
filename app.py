"""Home page for the Vegetable Insights Portal."""

import streamlit as st

st.set_page_config(
    page_title="Vegetable Insights Portal",
    page_icon="🥦",
    layout="wide",
)

st.title("🥦 Vegetable Insights Portal")
st.markdown(
    """
Welcome to the **Vegetable Insights Portal** — your team's go-to analytics companion
for all things vegetable-related. 🌽🥕🧅

This internal demo tool helps the team explore vegetable nutrition data, seasonal trends,
and popularity rankings across our curated dataset. Use the sidebar to navigate between
sections.

---

### What's inside?

| Page | Description |
|---|---|
| 🥦 Nutrition | Full nutritional breakdown per vegetable |
| 📊 Insights | Charts covering calories, vitamin C, fibre, seasonality, and popularity |
| 🔍 Comparison | Summary statistics and side-by-side vegetable comparisons |

---

> **Note:** All data is approximate and for demonstration purposes only.
> Do not use it for actual dietary advice — unless you genuinely want to start
> a heated debate about whether a tomato is a fruit.
"""
)
