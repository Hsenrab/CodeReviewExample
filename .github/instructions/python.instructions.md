---
applyTo: "**/*.py"
---

# Python standards — Vegetable Insights Portal

Apply these rules when generating, completing, or reviewing any Python file in
this repository.

## Type hints

All function parameters and return types must be annotated.

```python
# Correct
def get_season_vegetables(df: pd.DataFrame, season: str) -> pd.DataFrame:
    ...

# Incorrect — missing type hints
def get_season_vegetables(df, season):
    ...
```

## Docstrings

All public functions must have a Google-style docstring.

```python
def load_vegetables(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the vegetable dataset from a CSV file.

    Args:
        path: Path to the CSV file.

    Returns:
        DataFrame containing vegetable nutrition and metadata.

    Raises:
        FileNotFoundError: If the file cannot be found.
    """
```

Private helpers (prefixed with `_`) should have docstrings where the logic is
non-obvious.

## Variable naming

- Use descriptive names. Avoid `res`, `d`, `tmp`, `data`, or single-letter names.
- Prefer `filtered_df` over `filtered`, `top_df` over `res`.
- Boolean variables should read as propositions: `is_valid`, `has_missing_columns`.

## Architecture

- `src/` contains pure business logic only — no `import streamlit` in `src/`.
- `pages/` and `app.py` contain presentation only — no data transformation logic.
- Data loading and validation belong in `src/data_loader.py`.
- DataFrame transformations belong in `src/transforms.py`.
- When a filtering or calculation pattern appears in more than one place, extract
  it to `src/` as a named function.

## Error handling

- Functions in `src/data_loader.py` that perform I/O must raise informative
  exceptions (`FileNotFoundError`, `ValueError`) with descriptive messages.
- Streamlit page files must wrap data loading in `try/except` and call
  `st.error()` followed by `st.stop()` on failure.

## Streamlit pages

Each page must follow this order:
1. `st.set_page_config(...)`
2. `st.title(...)`
3. `st.markdown(...)` — introductory description
4. Data loading in `try/except`
5. Content (tables, charts, controls)
6. Footer: `st.markdown("---")` then `st.caption(...)`

Each chart block must include a `st.markdown(...)` explanation immediately before
the chart. A chart title alone is not sufficient.

## Tests

- All public `src/` functions need at least one test in `tests/`.
- Use `pytest` with type-annotated fixture functions.
- Test fixtures should use vegetable names and values.
- Cover edge cases: missing files, unknown filter values, boundary conditions.
