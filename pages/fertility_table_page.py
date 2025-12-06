from __future__ import annotations

from typing import Tuple

import dash
from dash import Input, Output, dcc, html, callback
from dash.exceptions import PageError
import dash_ag_grid as dag

from utils.data_utils import load_fertility, list_countries
from utils.grid_utils import fertility_column_defs, fertility_row_data

try:
    dash.register_page(__name__, path="/table", name="Fertility table")
except PageError:
    pass


def layout() -> html.Div:
    df = load_fertility()
    countries = list_countries()
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    return html.Div(
        [
            html.H2("Fertility data table (Dash AG Grid)"),
            html.Div(
                [
                    html.Label("Country"),
                    dcc.Dropdown(
                        id="table-country-dropdown",
                        options=[{"label": c, "value": c} for c in countries],
                        value="World",
                        persistence=True,
                        persistence_type="local",
                        style={"width": "260px"},
                    ),
                    html.Label("Year range"),
                    dcc.RangeSlider(
                        id="table-year-range",
                        min=min_year,
                        max=max_year,
                        value=[min_year, max_year],
                        step=1,
                        allowCross=False,
                        persistence=True,
                        persistence_type="session",
                    ),
                ],
                style={"maxWidth": "520px"},
            ),
            dag.AgGrid(
                id="fertility-ag-grid",
                columnDefs=fertility_column_defs(),
                rowData=[],
                className="ag-theme-alpine",
                style={"height": 500, "width": "100%", "marginTop": "16px"},
                defaultColDef={"resizable": True, "sortable": True, "filter": True},
            ),
        ]
    )


@callback(
    Output("fertility-ag-grid", "rowData"),
    Input("table-country-dropdown", "value"),
    Input("table-year-range", "value"),
)
def update_ag_grid(country: str, year_range: Tuple[int, int]):
    df = load_fertility()
    df_country = df[
        (df["country"] == country)
        & (df["year"] >= year_range[0])
        & (df["year"] <= year_range[1])
    ]
    return fertility_row_data(df_country)
