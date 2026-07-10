# %% Configuración de rutas del mini-proyecto
import sys
from pathlib import Path

RUTA_SESION = Path(__file__).resolve().parent
if str(RUTA_SESION) not in sys.path:
    sys.path.insert(0, str(RUTA_SESION))

from core.config import RUTA_GRAFICOS

# %% Sesión 07 — Filtro de Kalman y cadenas de Markov
RUTA_CASO_HORNO = RUTA_SESION / "caso_horno_cemento"

print("Sesión 07: Kalman / Markov")
print(f"Gráficos generales en: {RUTA_GRAFICOS}")
print(f"Caso horno de cemento (scripts + PNG): {RUTA_CASO_HORNO}")
print("\nEjecutar en orden:")
for script in sorted(RUTA_CASO_HORNO.glob("*.py")):
    print(f"  - {script.name}")
