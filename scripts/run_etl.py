"""CLI helper to execute the ETL pipeline."""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

from comercio_regional.pipeline import RegionalSalesPipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ejecuta el pipeline ETL de ventas regionales")
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path.cwd(),
        help="Directorio base del proyecto (por defecto cwd)",
    )
    return parser.parse_args()


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def main() -> None:
    configure_logging()
    args = parse_args()
    pipeline = RegionalSalesPipeline.from_default_layout(base_dir=args.base_dir)
    logging.info("Iniciando pipeline en %s", args.base_dir)
    pipeline.run()
    logging.info("Pipeline finalizado. Salida: %s", pipeline.output_path)


if __name__ == "__main__":
    main()
