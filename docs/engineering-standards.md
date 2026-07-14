# Vegetable Insights Portal — Engineering Standards

This document defines the engineering standards for the Vegetable Insights Portal.
All contributors (human and AI) are expected to follow these standards when writing,
reviewing, or modifying code in this repository.

---

## Architecture

### Separation of concerns

- **Business logic** belongs in `src/`, not directly in Streamlit page files.
- **Streamlit pages** (`pages/`, `app.py`) should be thin presentation layers. They load
  data, call `src/` functions, and render results. They must not contain data-transformation
  or filtering logic that could be reused elsewhere.
- **Data loading** lives in `src/data_loader.py`. I/O, validation, and column checking all
  belong here.
- **Transformations** live in `src/transforms.py`. Pure functions that operate on DataFrames
  and produce results for display.

---

## Python code style

### Type hints

- **All public functions must use type hints** for parameters and return values.
- Internal helpers should use type hints where it adds clarity.

```python
# Correct
def get_season_vegetables(df: pd.DataFrame, season: str) -> pd.DataFrame:
    ...

# Incorrect — missing type hints
def get_season_vegetables(df, season):
    ...
```

### Docstrings

- **All public functions must have a docstring** following the Google style.
- Include a one-line summary, an `Args:` block, and a `Returns:` block.
- `Raises:` should be documented where exceptions are explicitly raised.

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

### Variable names

- Use descriptive variable names. Avoid single-letter names or generic names like `d`,
  `res`, `tmp`, or `data` when a more specific name is available.
- Boolean variables should read like propositions: `is_numeric`, `has_missing_columns`.

### Error handling

- Data loading functions must validate inputs and raise informative exceptions.
- Streamlit pages must handle exceptions from data loading with `st.error()` and `st.stop()`.

---

## Streamlit page structure

Every page must follow this structure in order:

1. `st.set_page_config(...)` — page title, icon, and layout.
2. `st.title(...)` — the page heading.
3. `st.markdown(...)` — a short introductory description of what the page shows.
4. Data loading in a `try/except` block.
5. Page content (tables, charts, controls).
6. `st.markdown("---")` and `st.caption(...)` footer.

### Charts

- Every chart must have a clear, descriptive **title**.
- Axes must be **labelled** using the `labels=` parameter in Plotly, or equivalent.
- Each chart must be preceded by a short `st.markdown(...)` explanation telling the user
  what the chart shows and what to look for. Do not rely on the chart title alone.

---

## Reuse and DRY

- **Do not duplicate logic** that already exists in `src/`. For example, if
  `get_season_vegetables()` exists in `src/data_loader`, pages must call it rather than
  re-implementing the filter inline.
- If the same pattern appears in two or more places, extract it into `src/`.

---

## Tests

- Tests live in `tests/` and use `pytest`.
- Every public function in `src/` must have at least one test.
- Test fixtures should use vegetable-related names and data consistent with the project
  domain (e.g., `sample_df` containing carrots, broccoli, etc.).
- Tests must pass with `pytest` from the project root.
- Tests should cover edge cases such as unknown seasons, missing files, and boundary values
  in formatting functions.

---

## Documentation

- `README.md` must be kept up to date when behaviour, setup steps, or structure changes.
- Inline comments should explain *why*, not *what*, unless the code is genuinely non-obvious.
- The `docs/` directory contains extended guidance that supplements the README.

---

## Domain conventions

- The demo domain must remain **vegetable-themed**.
- Sample data, test fixtures, and examples should use vegetable names and vegetable-related
  values where clarity permits.
- User-facing copy may use light vegetable humour. Internal engineering code should not
  be artificially constrained to vegetable metaphors when that would reduce clarity.
- Do not force unrealistic naming conventions (e.g., naming every variable after a vegetable)
  that would make the project look like a toy.

---

## Intentional review issues

This repository contains a small number of **intentional standards violations** for use in
GitHub Copilot review experiments. They are realistic issues that a code reviewer should
be able to identify when applying these standards. They do not break the application or
cause tests to fail.

Reviewers and contributors should be able to identify and fix these issues by applying the
standards above. Do not look for obvious `# INTENTIONAL ISSUE` annotations — the issues
are embedded naturally in the code.
