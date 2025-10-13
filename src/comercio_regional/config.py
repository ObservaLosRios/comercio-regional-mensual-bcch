"""Configuration objects for the ETL pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class DataSourceConfig:
    """Settings describing the raw data sources."""

    name: str
    path: Path


@dataclass(frozen=True)
class LoadConfig:
    """Settings describing the load destination."""

    output_path: Path
    format: str = "parquet"


@dataclass(frozen=True)
class PipelineConfig:
    """Aggregates the configuration required to run the ETL pipeline."""

    sources: Sequence[DataSourceConfig]
    load: LoadConfig

    @staticmethod
    def default(base_dir: Path | None = None) -> "PipelineConfig":
        """Create a default configuration using the repository layout."""
        root = base_dir or Path.cwd()
        data_dir = root / "data"
        raw_dir = data_dir / "raw"
        processed_dir = data_dir / "processed"

        raw_dir.mkdir(parents=True, exist_ok=True)
        processed_dir.mkdir(parents=True, exist_ok=True)

        sources = [
            DataSourceConfig(name=path.stem.replace("dataset_", ""), path=path)
            for path in sorted(raw_dir.glob("dataset_*.csv"))
        ]
        load_format = "csv"
        load_filename = f"ventas_regionales.{load_format}"
        load_cfg = LoadConfig(
            output_path=processed_dir / load_filename,
            format=load_format,
        )
        return PipelineConfig(sources=sources, load=load_cfg)
