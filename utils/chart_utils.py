from __future__ import annotations

from typing import Tuple

import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure


def fertility_evolution_figure(df: pd.DataFrame, country: str) -> Figure:
    fig: Figure = px.line(
        df,
        x="year",
        y="fertility_rate",
        title=f"Fertility rate over time - {country}",
        markers=True,
    )
    fig.update_layout(xaxis_title="Year", yaxis_title="Births per woman")
    return fig


def fertility_distribution_figure(df: pd.DataFrame, country: str) -> Figure:
    fig: Figure = px.histogram(
        df,
        x="fertility_rate",
        nbins=15,
        title=f"Distribution of fertility values - {country}",
    )
    fig.update_layout(xaxis_title="Births per woman", yaxis_title="Count of years")
    return fig


def fertility_kpis(df: pd.DataFrame) -> Tuple[str, str]:
    df_sorted = df.sort_values("year")
    first = df_sorted.iloc[0]
    last = df_sorted.iloc[-1]
    current = float(last["fertility_rate"])
    change = current - float(first["fertility_rate"])
    kpi_now = f"{current:.2f} births / woman"
    kpi_change = f"{change:+.2f} vs {int(first['year'])}"
    return kpi_now, kpi_change
