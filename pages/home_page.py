from __future__ import annotations

from typing import Tuple

import dash
from dash import Input, Output, dcc, html, callback
from dash.exceptions import PageError

from utils.data_utils import load_fertility, list_countries
from utils.chart_utils import (
    fertility_distribution_figure,
    fertility_evolution_figure,
    fertility_kpis,
)

try:
    dash.register_page(__name__, path="/", name="Home")
except PageError:
    # Allows import without a Dash app instantiated (e.g., during linting/tests).
    pass


def layout() -> html.Div:
    df = load_fertility()
    countries = list_countries()
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    return html.Div(
        [
            html.H2("Fertility dashboard (proxy for reproduction)"),
            html.Div(
                [
                    html.Label("Country"),
                    dcc.Dropdown(
                        id="home-country-dropdown",
                        options=[{"label": c, "value": c} for c in countries],
                        value="World",
                        persistence=True,
                        persistence_type="local",
                    ),
                    html.Label("Year range"),
                    dcc.RangeSlider(
                        id="home-year-range",
                        min=min_year,
                        max=max_year,
                        value=[min_year, max_year],
                        step=1,
                        allowCross=False,
                        persistence=True,
                        persistence_type="session",
                    ),
                ],
                style={"maxWidth": "480px"},
            ),
            html.Div(
                id="home-kpi-row",
                style={"display": "flex", "gap": "16px", "marginTop": "16px"},
                children=[
                    html.Div(
                        [html.Div("Current fertility"), html.Div(id="home-kpi-now")],
                        className="kpi-card",
                    ),
                    html.Div(
                        [html.Div("Change since first year"), html.Div(id="home-kpi-change")],
                        className="kpi-card",
                    ),
                ],
            ),
            dcc.Graph(id="home-evolution-graph"),
            dcc.Graph(id="home-distribution-graph"),
        ]
    )


@callback(
    Output("home-evolution-graph", "figure"),
    Output("home-distribution-graph", "figure"),
    Output("home-kpi-now", "children"),
    Output("home-kpi-change", "children"),
    Input("home-country-dropdown", "value"),
    Input("home-year-range", "value"),
)
def update_home_page(country: str, year_range: Tuple[int, int]):
    df = load_fertility()
    df_country = df[
        (df["country"] == country)
        & (df["year"] >= year_range[0])
        & (df["year"] <= year_range[1])
    ]

    if df_country.empty:
        empty_fig = fertility_evolution_figure(df.iloc[0:0], country)
        return empty_fig, empty_fig, "No data", "No data"

    fig_evo = fertility_evolution_figure(df_country, country)
    fig_dist = fertility_distribution_figure(df_country, country)
    kpi_now, kpi_change = fertility_kpis(df_country)
    return fig_evo, fig_dist, kpi_now, kpi_change
