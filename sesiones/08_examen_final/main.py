# %% Configuración de rutas del mini-proyecto
import sys
from pathlib import Path

RUTA_SESION = Path(__file__).resolve().parent
if str(RUTA_SESION) not in sys.path:
    sys.path.insert(0, str(RUTA_SESION))

from core.config import RUTA_DATA, RUTA_DOCS, RUTA_GRAFICOS

# %% Sesión 08 — Examen final
print("Sesión 08: Examen final")
print(f"Datos (DVC) en:            {RUTA_DATA}")
print(f"PDFs de investigación en:  {RUTA_DOCS}")
print(f"Gráficos generados en:     {RUTA_GRAFICOS}")
