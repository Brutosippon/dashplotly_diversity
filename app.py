from __future__ import annotations

import dash
from dash import Dash, Input, Output, dcc, html


app: Dash = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
app.title = "Dash fertility app - charts & AG Grid"


def layout() -> html.Div:
    return html.Div(
        [
            dcc.Location(id="url"),
            html.H1("Reproduction / Fertility analytics", style={"marginLeft": "16px"}),
            dcc.Tabs(
                id="main-tabs",
                value="/",
                children=[
                    dcc.Tab(label="Dashboard", value="/"),
                    dcc.Tab(label="Data table", value="/table"),
                ],
            ),
            dash.page_container,
        ]
    )


app.layout = layout


@app.callback(Output("url", "pathname"), Input("main-tabs", "value"), prevent_initial_call=True)
def _tabs_to_url(tab_value: str) -> str:
    return tab_value


@app.callback(Output("main-tabs", "value"), Input("url", "pathname"))
def _url_to_tabs(pathname: str) -> str:
    if pathname not in {"/", "/table"}:
        return "/"
    return pathname


if __name__ == "__main__":
    app.run(debug=True)
