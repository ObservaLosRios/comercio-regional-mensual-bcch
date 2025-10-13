"""Transformation steps for the regional commerce dataset."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd

from .contracts import PipelineStep, Transformer


@dataclass(frozen=True)
class CompositeTransformer(Transformer):
    """Composes multiple `PipelineStep` callables into a single transformer."""

    steps: Iterable[PipelineStep]

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        result = data.copy()
        for step in self.steps:
            result = step(result)
        return result


def ensure_schema(data: pd.DataFrame) -> pd.DataFrame:
    """Validate the expected columns exist."""
    expected = {"fecha", "monto", "region"}
    missing = expected - set(data.columns)
    if missing:
        raise ValueError(f"Columnas faltantes en los datos extraídos: {missing}")
    return data


def normalize_dtypes(data: pd.DataFrame) -> pd.DataFrame:
    """Ensure date and numeric columns have the proper dtype."""
    frame = data.copy()
    frame["fecha"] = pd.to_datetime(frame["fecha"], errors="raise")
    frame["monto"] = pd.to_numeric(frame["monto"], errors="raise")
    frame["region"] = (
        frame["region"].astype(str).str.strip().str.replace("-", " ", regex=False).str.title()
    )
    return frame


def enrich_time_features(data: pd.DataFrame) -> pd.DataFrame:
    """Add year, month and quarter derived features."""
    frame = data.copy()
    frame["anio"] = frame["fecha"].dt.year
    frame["mes"] = frame["fecha"].dt.month
    frame["trimestre"] = frame["fecha"].dt.to_period("Q").astype(str)
    frame = frame.sort_values(["fecha", "region"]).reset_index(drop=True)
    return frame


def aggregate_by_period(data: pd.DataFrame) -> pd.DataFrame:
    """Compute aggregated metrics per region and year-month."""
    frame = data.copy()
    frame["periodo"] = frame["fecha"].dt.to_period("M").astype(str)
    aggregated = (
        frame.groupby(
            ["region", "periodo", "anio", "mes", "trimestre"],
            as_index=False,
        )
        .agg(
            monto_total=("monto", "sum"),
            monto_promedio=("monto", "mean"),
            observaciones=("monto", "size"),
        )
    )
    aggregated = aggregated.sort_values(["region", "periodo"]).reset_index(drop=True)
    return aggregated
