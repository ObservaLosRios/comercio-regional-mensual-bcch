"""Tests for validation helpers."""
from __future__ import annotations

import pandas as pd
import pytest

from comercio_regional.etl.validators import (
    DataValidationError,
    ensure_non_negative_monto,
    ensure_not_empty,
    ensure_numeric_monto,
    ensure_sorted_by_date,
)


def build_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "fecha": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "monto": [100.0, 200.0],
            "region": ["Araucania", "Biobio"],
        }
    )


def test_ensure_not_empty_allows_data():
    frame = build_frame()
    assert ensure_not_empty(frame) is frame


def test_ensure_numeric_monto_detects_non_numeric():
    frame = build_frame()
    frame["monto"] = ["a", "b"]
    with pytest.raises(DataValidationError):
        ensure_numeric_monto(frame)


def test_ensure_non_negative_monto_detects_negative_values():
    frame = build_frame()
    frame.loc[0, "monto"] = -10
    with pytest.raises(DataValidationError):
        ensure_non_negative_monto(frame)


def test_ensure_sorted_by_date_detects_disorder():
    frame = build_frame().iloc[[1, 0]].reset_index(drop=True)
    with pytest.raises(DataValidationError):
        ensure_sorted_by_date(frame)


def test_ensure_sorted_by_date_accepts_sorted_frame():
    frame = build_frame()
    assert ensure_sorted_by_date(frame) is frame
