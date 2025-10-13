"""Loader implementations for persisting transformed data."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .contracts import Loader


class CSVLoader(Loader):
    """Persist DataFrames to CSV format."""

    def __init__(self, destination: Path) -> None:
        self._destination = destination

    def load(self, data: pd.DataFrame) -> None:
        self._destination.parent.mkdir(parents=True, exist_ok=True)
        data.to_csv(self._destination, index=False)


class ParquetLoader(Loader):
    """Persist DataFrames to Apache Parquet format."""

    def __init__(self, destination: Path) -> None:
        self._destination = destination

    def load(self, data: pd.DataFrame) -> None:
        self._destination.parent.mkdir(parents=True, exist_ok=True)
        data.to_parquet(self._destination, index=False)
