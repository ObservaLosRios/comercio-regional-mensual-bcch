"""Unit tests for transformer utilities."""
from __future__ import annotations

import pandas as pd

from comercio_regional.etl.transformers import (
    aggregate_by_period,
    enrich_time_features,
    ensure_schema,
    normalize_dtypes,
)


def build_sample_frame() -> pd.DataFrame:
    data = {
        "fecha": ["01/01/2024", "01/01/2024", "01/02/2024"],
        "monto": ["1.000", "2.000", "3.000"],
        "region": ["araucania", "araucania", "biobio"],
    }
    frame = pd.DataFrame(data)
    frame["fecha"] = pd.to_datetime(frame["fecha"], dayfirst=True)
    frame["monto"] = pd.to_numeric(frame["monto"].str.replace(".", "", regex=False))
    return frame


def test_ensure_schema_accepts_expected_columns():
    frame = build_sample_frame()
    result = ensure_schema(frame)
    assert result.equals(frame)


def test_normalize_dtypes_formats_region_names():
    frame = build_sample_frame()
    normalized = normalize_dtypes(frame)
    assert normalized["region"].tolist() == ["Araucania", "Araucania", "Biobio"]


def test_enrich_time_features_adds_calendar_columns():
    frame = normalize_dtypes(build_sample_frame())
    enriched = enrich_time_features(frame)
    assert {"anio", "mes", "trimestre"}.issubset(enriched.columns)
    assert enriched.loc[0, "anio"] == 2024
    assert enriched.loc[0, "mes"] == 1


def test_aggregate_by_period_groups_expected_rows():
    frame = enrich_time_features(normalize_dtypes(build_sample_frame()))
    aggregated = aggregate_by_period(frame)
    assert list(aggregated.columns) == [
        "region",
        "periodo",
        "anio",
        "mes",
        "trimestre",
        "monto_total",
        "monto_promedio",
        "observaciones",
    ]
    assert aggregated.loc[aggregated["region"] == "Araucania", "observaciones"].item() == 2
