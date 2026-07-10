# %% Configuración de rutas del mini-proyecto
import sys
from pathlib import Path

import matplotlib.pyplot as plt

RUTA_SESION = Path(__file__).resolve().parent.parent
if str(RUTA_SESION) not in sys.path:
    sys.path.insert(0, str(RUTA_SESION))

from core.plotting import guardar_figura_script
from models.horno_cemento import simular_setpoint_constante

# %% Caso 1 — Simular setpoint constante y medición ruidosa
datos = simular_setpoint_constante()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(datos.caudal_verdadero, label="Caudal verdadero (simulado)")
ax.plot(datos.medicion, label="Medición ruidosa", alpha=0.7)
ax.axhline(datos.setpoint, color="k", linestyle="--", label="Setpoint")
ax.set_xlabel("Tiempo (k)")
ax.set_ylabel("Caudal (t/h)")
ax.set_title("Caso 1: Setpoint constante, medición ruidosa")
ax.legend()
ax.grid(True)

ruta_png = guardar_figura_script(fig, __file__)
print(f"Gráfico guardado: {ruta_png}")
