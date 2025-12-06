# Dash Reproduction App (Charts + Dash AG Grid)

Modular Dash app using the OWID fertility dataset. Pages live under `pages/`, utilities under `utils/`, styling in `assets/`, and the CSV source in `data/`.

## Data source
- Fertility rate (children per woman) from Our World in Data / UN WPP
- Downloaded to `data/children-per-woman-un.csv`
- Original URL: https://ourworldindata.org/grapher/children-per-woman-un.csv

## Quick start
```bash
cd /home/brutos/Documents/work/project_dashplotly_diversity
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
The app runs at http://127.0.0.1:8050/ with two tabs (dashboard and data table / Dash AG Grid).

## Project structure
- `app.py` — multi-page Dash shell with tab navigation
- `pages/home_page.py` — charts + KPIs (Plotly)
- `pages/fertility_table_page.py` — Dash AG Grid table
- `utils/data_utils.py` — CSV loader + country list
- `utils/chart_utils.py` — figures + KPI helpers
- `utils/grid_utils.py` — AG Grid column/row helpers
- `assets/style.css` — basic styling
- `requirements.txt` — minimal deps

## Notes
- Year sliders auto-range from the CSV min/max.
- Page registration is guarded so modules can be imported outside a running Dash app.
- To update data, replace `data/children-per-woman-un.csv` with the latest from OWID.
