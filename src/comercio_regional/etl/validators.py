"""Data validation utilities for the ETL pipeline."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class DataValidationError(ValueError):
    """Raised when a validation rule detects a data quality issue."""

    message: str

    def __str__(self) -> str:  # pragma: no cover
        return self.message


def ensure_not_empty(data: pd.DataFrame) -> pd.DataFrame:
    """Ensure the dataset is not empty."""
    if data.empty:
        raise DataValidationError("No se encontraron filas luego del proceso de limpieza.")
    return data


def ensure_numeric_monto(data: pd.DataFrame) -> pd.DataFrame:
    """Check that monto column is numeric and contains no nulls."""
    if not pd.api.types.is_numeric_dtype(data["monto"]):
        raise DataValidationError("La columna 'monto' debe ser numerica.")
    if data["monto"].isna().any():
        raise DataValidationError("La columna 'monto' contiene valores nulos.")
    return data


def ensure_non_negative_monto(data: pd.DataFrame) -> pd.DataFrame:
    """Reject negative monto values."""
    if (data["monto"] < 0).any():
        raise DataValidationError("Se detectaron montos negativos en los datos.")
    return data


def ensure_sorted_by_date(data: pd.DataFrame) -> pd.DataFrame:
    """Guarantee the dataset is sorted by fecha."""
    if not data["fecha"].is_monotonic_increasing:
        raise DataValidationError("Las filas deben estar ordenadas ascendentemente por fecha.")
    return data
