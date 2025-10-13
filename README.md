# Comercio Regional ETL — Observa Los Ríos

Proyecto desarrollado por Observa Los Ríos para profesionalizar el análisis mensual de compraventas regionales del Banco Central de Chile. El repositorio ofrece un flujo ETL escalable, probado y documentado, listo para integrarse en procesos de inteligencia territorial.

## Panorama general

- **Dominio**: comercio regional, series temporales mensuales.
- **Stack**: Python 3.13, pandas, pyjanitor, scikit-learn, Plotly, Ruff, Pytest.
- **Principios**: arquitectura SOLID, separación de responsabilidades, reproducibilidad y trazabilidad end-to-end.
- **Entrega**: dataset limpio en CSV, notebooks interactivos y documentación operativa.

## Mapa del repositorio

```
comercio-regional-mensual-bcch/
├── config/               # Definiciones declarativas del pipeline
├── data/
│   ├── raw/              # CSV mensuales provistos por el BCCh
│   └── processed/        # Salidas limpias listas para análisis
├── docs/                 # Diseño técnico y decisiones de arquitectura
├── notebooks/            # Reportes exploratorios y estilo The Economist
├── scripts/              # Utilidades CLI orientadas a operación
├── src/comercio_regional # Paquete ETL modular
├── tests/                # Suite Pytest con fixtures sintéticos
├── Makefile              # Comandos de desarrollo y automatización
└── README.md
```

## Puesta en marcha

```bash
make setup           # crea .venv, actualiza pip e instala dependencias
source .venv/bin/activate
make run             # ejecuta el pipeline con la configuración por defecto
```

El resultado principal se publica en `data/processed/ventas_regionales.csv`, con métricas agregadas por región y periodo. Los logs detallan el volumen de registros en cada fase.

## Flujo ETL

1. **Extract** · `CSVExtractor` unifica el ingreso de archivos `dataset_*.csv` desde `data/raw/`, aplicando reglas comunes de parseo (fechas `dayfirst`, separadores de miles y encoding consistente).
2. **Clean** · Funciones idempotentes remueven duplicados y registros críticos con nulos.
3. **Transform** · Composición de transformadores para normalizar tipos, enriquecer calendarios y agregar KPIs mensuales.
4. **Validate** · Contratos en `validators.py` aseguran dominios válidos, magnitudes no negativas y continuidad temporal.
5. **Load** · `CSVLoader` persiste la versión dorada en formato CSV, lista para ingesta en BI o notebooks.

Cada etapa se orquesta mediante `RegionalSalesPipeline`, lo que facilita pruebas unitarias aisladas y extensiones personalizadas.

## Notebooks curados

- `notebooks/etl_diagnostic.ipynb`: Diagnóstico rápido del pipeline y comprobaciones de calidad.
- `notebooks/economist_style_analysis.ipynb`: Narrativa visual con estética inspirada en The Economist.
- `notebooks/economist_style_analysis copy.ipynb`: Variante con ajustes cromáticos, anotaciones editoriales y dot plot tipo Cleveland.

Ejecuta los cuadernos con el entorno virtual activo para garantizar versiones compatibles de Plotly y pandas.

## Criterios de calidad

- `make test`: verifica transformaciones y validadores con Pytest.
- `make lint`: aplica Ruff para estilo, errores comunes y type hints.
- `make format`: formatea el código conforme a la guía del proyecto.

## Automatización y despliegue

- El pipeline puede integrarse en crons, Airflow u orquestadores similares ejecutando `make run`.
- Si se requiere Parquet u otro formato, ajusta `config/pipeline.yaml` sin modificar la lógica central.
- Los scripts en `scripts/` incluyen tareas operacionales como recargas históricas y generación de reportes ad-hoc.

## Créditos

Proyecto concebido y mantenido por el equipo de análisis territorial de Observa Los Ríos. Para consultas o contribuciones escribe a `contacto@observalosrios.cl`.

## Licencia

Define aquí la licencia definitiva al momento de la publicación.
