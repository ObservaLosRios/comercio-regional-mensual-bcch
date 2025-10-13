"""Data cleaning helpers for the ETL pipeline."""
from __future__ import annotations

import pandas as pd


def drop_missing_critical_values(data: pd.DataFrame) -> pd.DataFrame:
    """Remove records missing critical columns."""
    frame = data.copy()
    frame = frame.dropna(subset=["fecha", "monto", "region"])
    return frame


def remove_duplicates(data: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicate rows keeping the first occurrence."""
    frame = data.copy()
    frame = frame.drop_duplicates()
    return frame.reset_index(drop=True)
