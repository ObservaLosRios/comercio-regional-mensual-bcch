"""Extractor implementations for reading regional commerce data."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from .contracts import Extractor


class CSVExtractor(Extractor):
    """Extracts data from a collection of CSV files."""

    def __init__(self, files: Iterable[tuple[str, Path]]) -> None:
        self._files = list(files)

    def extract(self) -> pd.DataFrame:
        """Load and concatenate all configured CSV files."""
        frames: list[pd.DataFrame] = []
        for region, path in self._files:
            frame = self._read_single(path)
            frame["region"] = region
            frames.append(frame)
        if not frames:
            raise FileNotFoundError("No se encontraron archivos CSV para extraer datos.")
        return pd.concat(frames, ignore_index=True)

    @staticmethod
    def _read_single(path: Path) -> pd.DataFrame:
        """Read a single CSV file using consistent parsing rules."""
        if not path.exists():
            raise FileNotFoundError(f"El archivo {path} no existe.")
        frame = pd.read_csv(
            path,
            parse_dates=["Fecha"],
            dayfirst=True,
            thousands=".",
            decimal=",",
        )
        # Enforce canonical column names to simplify downstream steps.
        frame = frame.rename(columns={"Compraventas, Venta regional, monto": "monto"})
        frame = frame.rename(columns={"Fecha": "fecha"})
        return frame
