from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List

import pandas as pd

BASE_DIR: Path = Path(__file__).resolve().parents[1]
DATA_PATH: Path = BASE_DIR / "data" / "children-per-woman-un.csv"


@lru_cache(maxsize=1)
def load_fertility() -> pd.DataFrame:
    """Load fertility rate data from CSV."""
    df: pd.DataFrame = pd.read_csv(DATA_PATH)
    df = df.rename(
        columns={
            "Entity": "country",
            "Code": "iso_code",
            "Year": "year",
            "Fertility rate - Sex: all - Age: all - Variant: estimates": "fertility_rate",
        }
    )
    df = df[["country", "iso_code", "year", "fertility_rate"]]
    return df


def list_countries() -> List[str]:
    df = load_fertility()
    return sorted(df["country"].unique().tolist())
