---
title: ReproDash – Fertility Analytics
emoji: 📊
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "0.0.0"
app_file: app.py
pinned: false
---

# Dash Reproduction App (Charts + Dash AG Grid)

This README is a short tutorial / checklist for building a polished, modular Dash app (dark mode, Plotly + Dash AG Grid) like this project. Use it as a TODO to replicate or extend the setup with your own data.

Live Space: https://huggingface.co/spaces/brutos/reprodash

## Data source
- Fertility rate (children per woman) from Our World in Data / UN WPP
- Downloaded to `data/children-per-woman-un.csv`
- Original URL: https://ourworldindata.org/grapher/children-per-woman-un.csv

## Quick start
```bash
cd work/project_dashplotly_diversity
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
The app runs at http://127.0.0.1:8050/ with two tabs (dashboard and data table / Dash AG Grid).

## Tutorial / TODO checklist
- [ ] Design: pick a theme (dark), define colors, spacing, and responsive breakpoints.
- [ ] Data: place your CSV/Parquet under `data/`; adapt `utils/data_utils.py` to rename columns and expose helper lists (e.g., countries).
- [ ] Layout shell: `app.py` handles routing (`dash.page_container` + `dcc.Location`) and a simple nav bar (`dcc.Link`), no circular callbacks.
- [ ] Pages: put views in `pages/` (`home_page.py` for charts/KPIs, `fertility_table_page.py` for AG Grid). Register pages defensively so imports work in tests.
- [ ] Charts: use Plotly helpers in `utils/chart_utils.py`, set `pio.templates.default = "plotly_dark"`, and harmonize axis/grid colors with the theme.
- [ ] Grid: configure columns/row data in `utils/grid_utils.py` (sorting, filtering, right alignment, valueFormatters). Use `ag-theme-alpine-dark`.
- [ ] Styling: keep all look-and-feel in `assets/style.css` (full-width responsive containers, dropdowns/sliders readable in dark mode, KPI cards wrap on mobile, nav hover/active states).
- [ ] Controls: ensure dropdowns/sliders are 100% width, with sensible marks (e.g., years every 10y + first/last) to avoid clutter.
- [ ] Logging: set up `utils/logging_utils.py` to log to `logs/app.log` + console; decorate callbacks to catch/log exceptions.
- [ ] Accessibility/readability: high-contrast text for labels/options, focused/selected states visible, avoid washed-out whites.

## Project structure (reference)
- `app.py` — multi-page Dash shell + nav links (URL is source of truth)
- `pages/home_page.py` — charts + KPIs
- `pages/fertility_table_page.py` — Dash AG Grid table
- `utils/data_utils.py` — CSV loader + country list
- `utils/chart_utils.py` — figures + KPI helpers (dark template)
- `utils/grid_utils.py` — AG Grid column/row helpers
- `utils/logging_utils.py` — logging setup + callback exception helper
- `assets/style.css` — theme, responsive layout, controls, nav, AG Grid, sliders
- `requirements.txt` — minimal deps

## Deployment notes
- Hugging Face Space uses the `Dockerfile` in the repo; the app listens on port 7860 by default.
- For other platforms: build the image with `docker build -t reprodash .` and run `docker run -p 7860:7860 reprodash`.

## Update data
- Replace `data/children-per-woman-un.csv` with the latest OWID export (same column names) and restart. For DB sources, swap the loader in `utils/data_utils.py`.
