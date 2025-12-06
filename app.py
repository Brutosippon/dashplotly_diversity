from __future__ import annotations

import dash
from dash import Dash, Input, Output, dcc, html

from utils.logging_utils import get_logger, setup_logging

logger = setup_logging()

NAV_LINKS = [
    {"label": "Dashboard", "path": "/"},
    {"label": "Data table", "path": "/table"},
]

app: Dash = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
server = app.server
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
                        id="main-nav",
                        className="tabs-wrapper",
                        children=[
                            dcc.Link(
                                link["label"],
                                href=link["path"],
                                id=f"nav-{link['path'].strip('/') or 'home'}",
                                className="nav-link",
                            )
                            for link in NAV_LINKS
                        ],
                    ),
                    dash.page_container,
                ],
            ),
        ],
    )


app.layout = layout


@app.callback(
    Output("nav-home", "className"),
    Output("nav-table", "className"),
    Input("url", "pathname"),
)
def _highlight_nav(pathname: str) -> tuple[str, str]:
    active = "nav-link nav-link--active"
    inactive = "nav-link"
    if pathname == "/table":
        return inactive, active
    return active, inactive


if __name__ == "__main__":
    logger.info("Starting Dash app server...")
    #app.run(debug=True)
    app.run_server(host="0.0.0.0", port=7860, debug=True)
