"""ETL pipeline orchestration."""
from __future__ import annotations

import logging
from pathlib import Path

from .config import PipelineConfig
from .etl.contracts import Loader, Pipeline
from .etl.cleaning import drop_missing_critical_values, remove_duplicates
from .etl.extractors import CSVExtractor
from .etl.loaders import CSVLoader, ParquetLoader
from .etl.transformers import (
    CompositeTransformer,
    aggregate_by_period,
    enrich_time_features,
    ensure_schema,
    normalize_dtypes,
)
from .etl.validators import (
    ensure_non_negative_monto,
    ensure_not_empty,
    ensure_numeric_monto,
    ensure_sorted_by_date,
)


class RegionalSalesPipeline(Pipeline):
    """Concrete pipeline implementation for regional sales data."""

    def __init__(self, config: PipelineConfig) -> None:
        self._config = config
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def output_path(self) -> Path:
        """Return the configured output path."""
        return self._config.load.output_path

    def steps(self):  # type: ignore[override]
        return (
            ensure_schema,
            drop_missing_critical_values,
            remove_duplicates,
            normalize_dtypes,
            ensure_numeric_monto,
            ensure_non_negative_monto,
            enrich_time_features,
            ensure_sorted_by_date,
            aggregate_by_period,
            ensure_not_empty,
        )

    def run(self) -> None:  # type: ignore[override]
        extractor = CSVExtractor((src.name, src.path) for src in self._config.sources)
        transformer = CompositeTransformer(self.steps())
        loader = self._build_loader()

        raw_data = extractor.extract()
        self._logger.info("Filas extraidas: %s", len(raw_data))

        transformed = transformer.transform(raw_data)
        self._logger.info("Filas transformadas: %s", len(transformed))

        loader.load(transformed)
        self._logger.info("Datos cargados en %s", self.output_path)

    @classmethod
    def from_default_layout(cls, base_dir: Path | None = None) -> "RegionalSalesPipeline":
        config = PipelineConfig.default(base_dir=base_dir)
        return cls(config)

    def _build_loader(self) -> Loader:
        fmt = self._config.load.format.lower()
        if fmt == "csv":
            return CSVLoader(self.output_path)
        if fmt == "parquet":
            return ParquetLoader(self.output_path)
        raise ValueError(f"Formato de carga no soportado: {self._config.load.format}")
