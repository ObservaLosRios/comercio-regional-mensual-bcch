# Comercio Regional ETL — Observa Los Ríos

Pipeline de datos y visualización interactiva para analizar el comercio regional mensual reportado por el Banco Central de Chile. El repositorio reúne un flujo ETL reproducible, material de apoyo analítico y un dashboard estático listo para publicar.

## Componentes clave

- **ETL modular**: paquete `comercio_regional` que estandariza extracción, limpieza, transformación, validación y carga a CSV o Parquet.
- **Dashboard estático**: sitio en `docs/` con dos gráficos Plotly (ventas mensuales y variación interanual) optimizados para compartir online.
- **Notebooks exploratorios**: cuadernos para diagnóstico y narrativa visual con estilo editorial.
- **Pruebas automatizadas**: suite Pytest que cubre limpieza, transformaciones y validaciones de dominio.

## Estructura del repositorio

```
comercio-regional-mensual-bcch/
├── config/               # pipeline.yaml con rutas y formato de salida
├── data/
│   ├── raw/              # datasets mensuales entregados por el BCCh
│   └── processed/        # export del pipeline (ventas_regionales.csv)
├── docs/                 # dashboard estático (index.html, JS y estilos)
├── notebooks/            # análisis exploratorios y material de comunicación
├── scripts/              # utilidades CLI (por ejemplo, scripts/run_etl.py)
├── src/comercio_regional # paquete Python con la lógica ETL
├── tests/                # pruebas unitarias
├── requirements.txt      # dependencias mínimas del proyecto
└── README.md
```

## Puesta en marcha rápida

```bash
python -m venv .venv
source .venv/bin/activate  # en macOS/Linux
pip install -r requirements.txt
pip install -e .            # instala el paquete en editable

python scripts/run_etl.py   # ejecuta el pipeline completo
```

La ejecución genera `data/processed/ventas_regionales.csv` con ventas agregadas por región y periodo. Ajusta la configuración en `config/pipeline.yaml` si necesitas otro directorio o formato de salida.

## Visualización

- El dashboard se encuentra en `docs/index.html` junto con `interactive.js` y `styles.css`.
- Todos los datos del gráfico están embebidos en la misma página; no requiere dependencias externas adicionales.
- Para previsualizarlo localmente:

```bash
cd docs
python -m http.server 8000
```

Visita `http://localhost:8000` y navega entre las pestañas **Ventas Mensuales** y **Variación Interanual**.

## Flujo ETL

1. **Extract** · `CSVExtractor` integra los archivos `dataset_*.csv` almacenados en `data/raw/`.
2. **Clean** · Se eliminan duplicados y observaciones con valores críticos faltantes.
3. **Transform** · Transformadores encadenados normalizan tipos, enriquecen con variables de fecha y agregan métricas mensuales.
4. **Validate** · Validadores garantizan montos numéricos, no negativos, orden temporal y ausencia de salidas vacías.
5. **Load** · `CSVLoader` o `ParquetLoader` escriben el dataset final en `data/processed/`.

La clase `RegionalSalesPipeline` orquesta cada etapa y expone el método `from_default_layout` para instancias rápidas.

## Notebooks

- `notebooks/analysis.ipynb`: exploración de ventas regionales.
- `notebooks/etl_diagnostic.ipynb`: chequeos de consistencia post-ETL.
- `notebooks/visualizacion_analysis.ipynb`: prototipos de visualización en Plotly.

Ejecuta los cuadernos con el entorno virtual activo para mantener compatibilidad de librerías.

## Calidad y pruebas

- `pytest` ejecuta la suite ubicada en `tests/`.
- Los tests cubren operaciones de limpieza, transformaciones clave y validaciones de negocio.
- Se recomienda combinar con herramientas como Ruff o Black según estándares internos (no incluidas por defecto).

## Créditos y licencia

Proyecto desarrollado por Observa Los Ríos. Para soporte o consultas escribe a `contacto@observalosrios.cl`.

<<<<<<< HEAD
## Ejecución

Proyecto concebido y mantenido por el equipo de análisis territorial de Observa Los Ríos. Cer UACh

=======
La licencia se definirá antes de la publicación oficial.
>>>>>>> 5e9c133 (Compras, ventas regional $ x mes)
