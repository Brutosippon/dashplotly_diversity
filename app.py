from __future__ import annotations

import dash
from dash import Dash, Input, Output, dcc, html

from utils.logging_utils import get_logger, setup_logging

logger = setup_logging()

NAV_TABS = [
    {"label": "Dashboard", "path": "/"},
    {"label": "Data table", "path": "/table"},
]

app: Dash = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
app.title = "Dash fertility app - charts & AG Grid"


def layout() -> html.Div:
    return html.Div(
        className="app-shell",
        children=[
            dcc.Location(id="url"),
            html.Div(
                className="page-container",
                children=[
                    html.H1("Reproduction / Fertility analytics"),
                    html.Div(
                        className="tabs-wrapper",
                        children=dcc.Tabs(
                            id="main-tabs",
                            value="/",
                            className="dash-tabs",
                            children=[
                                dcc.Tab(
                                    label=tab["label"],
                                    value=tab["path"],
                                    className="dash-tab",
                                    selected_className="dash-tab--selected",
                                    children=html.A(
                                        tab["label"],
                                        href=tab["path"],
                                        className="tab-link",
                                    ),
                                )
                                for tab in NAV_TABS
                            ],
                        ),
                    ),
                    dash.page_container,
                ],
            ),
        ],
    )


app.layout = layout


@app.callback(Output("main-tabs", "value"), Input("url", "pathname"))
def _url_to_tabs(pathname: str) -> str:
    if pathname not in {"/", "/table"}:
        return "/"
    return pathname


if __name__ == "__main__":
    logger.info("Starting Dash app server...")
    app.run(debug=True)
