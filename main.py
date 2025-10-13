"""Entry point to execute the ETL pipeline programmatically."""
from __future__ import annotations

from pathlib import Path

from comercio_regional.pipeline import RegionalSalesPipeline


def run_pipeline(base_dir: Path | None = None) -> None:
    """Build and run the regional sales pipeline."""
    pipeline = RegionalSalesPipeline.from_default_layout(base_dir=base_dir)
    pipeline.run()


if __name__ == "__main__":
    run_pipeline(Path.cwd())
