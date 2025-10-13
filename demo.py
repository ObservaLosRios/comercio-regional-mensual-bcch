"""Quick demonstration of the ETL package API."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from comercio_regional.pipeline import RegionalSalesPipeline


def main() -> None:
    base_dir = Path(__file__).parent
    pipeline = RegionalSalesPipeline.from_default_layout(base_dir=base_dir)
    pipeline.run()

    output_path = pipeline.output_path
    aggregated = pd.read_csv(output_path)
    print("Primeras filas del dataset agregado:")
    print(aggregated.head())


if __name__ == "__main__":
    main()
