from __future__ import annotations

from typing import List, Dict, Any

import pandas as pd


def fertility_column_defs() -> List[Dict[str, Any]]:
    """Column definitions for Dash AG Grid."""
    return [
        {"field": "country", "headerName": "Country", "sortable": True, "filter": True},
        {"field": "iso_code", "headerName": "ISO", "maxWidth": 100},
        {"field": "year", "headerName": "Year", "sortable": True, "filter": "agNumberColumnFilter"},
        {
            "field": "fertility_rate",
            "headerName": "Births / woman",
            "type": "rightAligned",
            "valueFormatter": {"function": "d3.format('.2f')(params.value)"},
        },
    ]


def fertility_row_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Convert DF to list-of-dicts for AG Grid."""
    return df.to_dict(orient="records")
