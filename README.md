# 🥦 Vegetable Insights Portal

A small Python Streamlit web application used as a demo and experimentation target for
**GitHub Copilot code review**, GitHub CLI workflows, and repository-specific review
standards.

The project is deliberately light-hearted — it's a fictional internal analytics portal
for exploring vegetable nutrition, seasonality, popularity, and simple data insights —
but the codebase uses realistic software engineering practices to make it a credible
review target.

---

## Why this repository exists

This repository exists as a **demo target** for workflows where a user or script:

1. Clones the repository using GitHub CLI.
2. Inspects the codebase locally.
3. Uses GitHub Copilot to review the repository or a pull request.
4. Checks whether Copilot applies the repository's documented engineering standards.
5. Evaluates whether Copilot identifies realistic issues, standards violations, and
   maintainability concerns.

The repository includes intentional standards violations embedded naturally in the code.
They do not break the application or fail tests, but a thorough AI code review should
surface them.

---

## Quick start with GitHub CLI

```bash
# Clone the repository
gh repo clone Hsenrab/CodeReviewExample
cd CodeReviewExample

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py

# Run the tests
pytest
```

---

## Project structure

```
.
├── app.py                          # Home page (Streamlit entry point)
├── requirements.txt
├── README.md
│
├── pages/                          # Streamlit multipage pages
│   ├── 1_🥦_Nutrition.py           # Nutritional breakdown table
│   ├── 2_📊_Insights.py            # Charts and visualisations
│   └── 3_🔍_Comparison.py          # Summary stats and side-by-side comparison
│
├── src/                            # Business logic (no Streamlit imports)
│   ├── __init__.py
│   ├── data_loader.py              # CSV loading, validation, filtering
│   └── transforms.py               # DataFrame transformations and formatting
│
├── data/
│   └── vegetables.csv              # Demo dataset (12 vegetables)
│
├── tests/
│   ├── test_data_loader.py
│   └── test_transforms.py
│
├── docs/
│   └── engineering-standards.md   # Extended engineering standards reference
│
└── .github/
    ├── copilot-instructions.md     # Repository-wide Copilot instructions
    └── instructions/
        └── python.instructions.md  # Python-specific path-scoped instructions
```

---

## Installation

Requires Python 3.11 or later.

```bash
pip install -r requirements.txt
```

**Dependencies:**

| Package | Purpose |
|---|---|
| `streamlit` | Web application framework |
| `pandas` | Data loading and manipulation |
| `plotly` | Interactive charts |
| `pytest` | Test runner |

---

## Running the app

```bash
streamlit run app.py
```

Streamlit will open the app in your browser at `http://localhost:8501`.

The sidebar provides navigation between the three pages:

- **🥦 Nutrition** — tabular nutritional data per vegetable.
- **📊 Insights** — bar charts and a pie chart covering calories, vitamin C, fibre,
  seasonality, and popularity.
- **🔍 Comparison** — summary statistics, seasonal filtering, and a side-by-side
  comparison tool.

---

## Running tests

```bash
pytest
```

Or with verbose output:

```bash
pytest -v
```

Tests cover:

- Loading the vegetable CSV and validating required columns.
- Numeric columns having numeric dtypes.
- Error handling for missing files and missing columns.
- Seasonal filtering behaviour.
- Nutrient summary statistics.
- Popularity formatting at boundary values.
- Top-n ranking utility.

---

## Dataset

`data/vegetables.csv` contains 12 vegetables with the following columns:

| Column | Description |
|---|---|
| `vegetable` | Vegetable name |
| `colour` | Primary colour |
| `calories_per_100g` | Approximate calories per 100g |
| `vitamin_c_mg_per_100g` | Vitamin C content in mg per 100g |
| `fibre_g_per_100g` | Dietary fibre in g per 100g |
| `season` | Peak availability season |
| `popularity_score` | Demo popularity score (1–10) |

> All values are approximate and intended for software demonstration only.

---

## Engineering standards

Full standards are documented in [`docs/engineering-standards.md`](docs/engineering-standards.md).

Key principles:

- Business logic belongs in `src/`, not in Streamlit page files.
- Streamlit pages are thin presentation layers only.
- All public functions must have type hints and docstrings.
- Data loading must include error handling.
- Repeated logic must be centralised in `src/`.
- Every chart must have a title, labelled axes, and a preceding markdown explanation.
- Every Streamlit page must follow a consistent structure (title → intro → data → content → footer).
- Tests must cover all reusable `src/` functions.

---

## Copilot Review Strategy

### Guidance consulted

This repository was designed using the following GitHub Copilot customisation mechanisms
identified from the latest GitHub documentation (2025):

1. **`.github/copilot-instructions.md`** — repository-wide instructions read
   automatically by GitHub Copilot for Chat, code completions, code review, and
   Copilot agent sessions.
2. **`.github/instructions/*.instructions.md`** — path-scoped instruction files with
   YAML frontmatter (`applyTo: "**/*.py"`) that apply targeted guidance to specific
   file types or directories.

### Mechanisms selected and why

| Mechanism | File | Why chosen |
|---|---|---|
| Repository-wide instructions | `.github/copilot-instructions.md` | Provides global context — project architecture, all engineering standards, and the list of standards to enforce during review. Applies to every Copilot interaction in the repository. |
| Python-scoped instructions | `.github/instructions/python.instructions.md` | Applies Python-specific conventions only to `.py` files, providing more targeted guidance than a single global file would allow. |

A third mechanism — **`AGENTS.md`** — was considered but not added, as it is primarily
intended for Copilot agent mode task execution rather than code review, and the existing
two files cover the review use case sufficiently.

Organisation-level instructions were not used because this is a standalone demo repository
with no organisation-wide policy requirement.

### How the instructions influence code review behaviour

When Copilot reviews a pull request or inspects a file in this repository, it reads
`.github/copilot-instructions.md` automatically. The file:

- Describes the project architecture so Copilot understands where logic should live.
- Lists each engineering standard explicitly (type hints, docstrings, page structure,
  chart explanations, DRY principle, test coverage).
- Instructs Copilot to flag specific patterns (e.g., missing `st.markdown()` before
  charts, inline filtering that should use `get_season_vegetables()`).
- Notes that intentional violations exist, prompting Copilot to look carefully for
  subtle issues rather than only obvious syntax errors.

The path-scoped `.github/instructions/python.instructions.md` reinforces the Python
conventions with concrete code examples, making it easier for Copilot to recognise
compliant vs. non-compliant patterns.

### How to test whether Copilot applies the instructions

1. **Open Copilot Chat** in VS Code or GitHub.com with this repository open.
2. Ask: _"Review this repository against the engineering standards."_
   Copilot should cite standards from `.github/copilot-instructions.md`.
3. **Open a pull request** that modifies `src/` or `pages/`. Copilot code review
   should apply the standards automatically.
4. **Ask specifically:** _"Does `pages/3_🔍_Comparison.py` follow the page structure
   standard?"_ — Copilot should identify the missing introductory description.
5. **Ask:** _"Review `src/transforms.py` for docstring and type hint compliance."_ —
   Copilot should identify `format_popularity` as missing a docstring.
6. **Ask:** _"Is there any duplicated logic between pages and `src/`?"_ — Copilot
   should identify the inline season filtering in `pages/3_🔍_Comparison.py`.

### Limitations and caveats

- Instructions are advisory. Copilot applies them heuristically; it does not enforce
  them as a compiler or linter would.
- The effectiveness of instructions varies between Copilot features (Chat, code review,
  completions). Code review on pull requests typically applies instructions most
  consistently.
- Very long instruction files may dilute Copilot's attention. The instruction files in
  this repository are deliberately concise and focused.
- Instructions are only applied when Copilot has access to the repository context.
  They do not apply to Copilot interactions in unrelated repositories.
- Path-scoped instructions (`applyTo:`) require a Copilot client that supports the
  `.github/instructions/` feature (VS Code with the GitHub Copilot extension, or
  GitHub.com). Check the GitHub Copilot changelog for the latest feature availability.

---

## Using this repository with GitHub CLI and Copilot

```bash
# Clone
gh repo clone Hsenrab/CodeReviewExample
cd CodeReviewExample

# Install and run
pip install -r requirements.txt
streamlit run app.py

# Run tests
pytest

# Create a branch and open a PR for Copilot review experimentation
git checkout -b experiment/my-change
# ... make a change ...
git add .
git commit -m "Experiment: introduce a standards violation"
gh pr create --title "Experiment: standards violation" --body "Testing Copilot review."

# Ask Copilot to review the PR
gh copilot suggest "Review my open pull request for engineering standards violations"
```

---

## Contributing

1. Follow the engineering standards in [`docs/engineering-standards.md`](docs/engineering-standards.md).
2. Run `pytest` before pushing.
3. Keep `README.md` up to date if you change setup steps or project structure.
4. The Copilot instructions files (`.github/`) should be updated if the standards change.