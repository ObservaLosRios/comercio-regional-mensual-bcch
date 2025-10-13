# Arquitectura del Pipeline

## Objetivo

Consolidar mensualmente las ventas regionales del comercio, entregando un dataset limpio, validado y listo para analitica.

## Componentes

- **Extractores** (`etl/extractors.py`): leen las fuentes CSV raw.
- **Cleaning** (`etl/cleaning.py`): eliminan registros incompletos o duplicados.
- **Transformers** (`etl/transformers.py`): normalizan tipos, enriquecen con features temporales y agregan metricas.
- **Validators** (`etl/validators.py`): aplican reglas de calidad antes de persistir los datos.
- **Loaders** (`etl/loaders.py`): escriben el resultado final en CSV (y soportan Parquet opcional).
- **Pipeline** (`pipeline.py`): orquesta cada paso y expone metodos para ejecutar la corrida completa.

## Principios de diseño

- **SOLID**: cada modulo cubre una responsabilidad clara.
- **Pureza**: las funciones de transformacion devuelven nuevos DataFrames, evitando efectos colaterales.
- **Extensibilidad**: nuevos pasos pueden agregarse al pipeline componiendo `PipelineStep` adicionales.

## Datos

- `data/raw/`: datasets mensuales por region.
- `data/processed/ventas_regionales.csv`: resultado agregado por region/mes, con metricas basicas listo para BI.

## Operacion

- `scripts/run_etl.py`: CLI para agendar ejecuciones.
- `main.py`: entry point minimalista.
- `demo.py`: ejemplo end-to-end para analistas.
