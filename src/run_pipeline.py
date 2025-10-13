"""Command-line entry point for the regional commerce ETL pipeline."""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

from comercio_regional.pipeline import RegionalSalesPipeline


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ETL para consolidar ventas regionales del comercio"  # noqa: D401
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path.cwd(),
        help="Ruta base del repositorio (por defecto el directorio actual).",
    )
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()

    pipeline = RegionalSalesPipeline.from_default_layout(base_dir=args.base_dir)
    logging.info("Iniciando pipeline con base_dir=%s", args.base_dir)
    pipeline.run()
    logging.info("Pipeline finalizado. Archivo generado en %s", pipeline.output_path)


if __name__ == "__main__":
    main()
