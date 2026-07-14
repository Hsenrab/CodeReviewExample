# Copilot Instructions — Vegetable Insights Portal

This repository is the **Vegetable Insights Portal**, a Python Streamlit web application
used internally as a demo and experimentation target for GitHub Copilot code review,
GitHub CLI workflows, and repository-specific review standards.

## Project context

- **Language:** Python 3.11+
- **Framework:** Streamlit (multipage app)
- **Data:** pandas DataFrames loaded from `data/vegetables.csv`
- **Charts:** Plotly Express
- **Tests:** pytest

## Architecture

```
app.py              # Streamlit home page (thin presentation only)
pages/              # Streamlit multipage pages (thin presentation only)
src/                # Business logic — data loading, filtering, transformations
data/               # CSV dataset
tests/              # pytest tests for src/ modules
docs/               # Extended engineering documentation
```

## Engineering standards to enforce during code review

When reviewing code in this repository, apply the following standards. Flag any
violation as a review comment, regardless of how minor it appears.

### Architecture standards

- Business logic (data filtering, transformations, calculations) belongs in `src/`,
  not in Streamlit page files (`app.py` or `pages/`).
- Streamlit pages should only: load data via `src/` functions, call `src/` functions,
  and render results with Streamlit widgets. No inline data manipulation.
- If a filtering or transformation pattern appears in more than one place, it must be
  extracted to `src/` as a reusable function.

### Python code standards

- All public functions must have **type hints** on every parameter and the return type.
- All public functions must have a **docstring** following Google style with `Args:`,
  `Returns:`, and `Raises:` sections where applicable.
- Variable names must be descriptive. Flag names like `res`, `d`, `tmp`, `data`, or
  single-letter names when a more specific name would improve readability.
- Data loading functions must validate inputs and raise informative exceptions.
- Streamlit pages must handle data loading errors with `st.error()` and `st.stop()`.

### Streamlit page structure standard

Every page (`app.py` and files in `pages/`) must follow this exact structure:

1. `st.set_page_config(...)` — at the top
2. `st.title(...)` — page heading
3. `st.markdown(...)` — introductory description of what the page shows
4. Data loading inside a `try/except` block
5. Page content (tables, charts, controls)
6. `st.markdown("---")` and `st.caption(...)` footer

Flag any page that is missing the introductory `st.markdown(...)` description after
the title.

### Chart standards

- Every chart must have a descriptive **title**.
- Axes must be **labelled** (using `labels=` in Plotly, or equivalent).
- Every chart must be **preceded by a short `st.markdown(...)` explanation** describing
  what the chart shows and what to look for. A chart title alone is not sufficient.
  Flag any chart block that lacks a preceding `st.markdown()` explanation.

### Test standards

- Every public function in `src/` must have at least one test in `tests/`.
- Tests use pytest with fixtures named using vegetable-related data.
- Edge cases (empty results, missing files, boundary values) must be covered.

### Documentation standards

- `README.md` must be kept current with any changes to setup, structure, or behaviour.
- Inline comments should explain *why*, not *what*, unless the logic is non-obvious.

## Domain conventions

- Sample data, test fixtures, and examples should use vegetable names and values.
- User-facing copy may use light vegetable humour; internal code should not use
  forced vegetable metaphors that reduce clarity.
- Do not invent unrealistic naming conventions (e.g., naming every variable after
  a vegetable) that would make the project look like a toy exercise.

## Known intentional issues

This repository contains a small number of intentional standards violations embedded
naturally in the code. They are placed there for Copilot review experimentation and
do not break the application or fail tests. A thorough code review applying the
standards above should surface them.
