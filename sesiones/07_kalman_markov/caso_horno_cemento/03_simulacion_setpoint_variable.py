# %% Configuración de rutas del mini-proyecto
import sys
from pathlib import Path

import matplotlib.pyplot as plt

RUTA_SESION = Path(__file__).resolve().parent.parent
if str(RUTA_SESION) not in sys.path:
    sys.path.insert(0, str(RUTA_SESION))

from core.plotting import guardar_figura_script
from models.horno_cemento import simular_setpoint_variable

# %% Caso 2 — Simular setpoint escalonado y medición ruidosa
datos = simular_setpoint_variable()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(datos.medicion, label="Medición ruidosa", alpha=0.6)
ax.plot(datos.caudal_verdadero, label="Caudal verdadero (simulado)", linewidth=2)
ax.plot(datos.setpoint, label="Setpoint", linestyle="--", color="k")
ax.set_xlabel("Tiempo (k)")
ax.set_ylabel("Caudal (t/h)")
ax.set_title("Caso 2: Setpoint variable y medición ruidosa")
ax.legend()
ax.grid(True)

ruta_png = guardar_figura_script(fig, __file__)
print(f"Gráfico guardado: {ruta_png}")
