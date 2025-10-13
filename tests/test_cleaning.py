"""Tests for cleaning helpers."""
from __future__ import annotations

import pandas as pd

from comercio_regional.etl.cleaning import drop_missing_critical_values, remove_duplicates


def test_drop_missing_critical_values_removes_null_rows():
    frame = pd.DataFrame(
        {
            "fecha": ["2024-01-01", None],
            "monto": [100, 200],
            "region": ["Araucania", "Biobio"],
        }
    )
    cleaned = drop_missing_critical_values(frame)
    assert len(cleaned) == 1


def test_remove_duplicates_keeps_unique_rows():
    frame = pd.DataFrame(
        {
            "fecha": ["2024-01-01", "2024-01-01"],
            "monto": [100, 100],
            "region": ["Araucania", "Araucania"],
        }
    )
    cleaned = remove_duplicates(frame)
    assert len(cleaned) == 1
