# %% Configuración de rutas del mini-proyecto
import sys
from pathlib import Path

import matplotlib.pyplot as plt

RUTA_SESION = Path(__file__).resolve().parent.parent
if str(RUTA_SESION) not in sys.path:
    sys.path.insert(0, str(RUTA_SESION))

from core.plotting import guardar_figura_script
from models.horno_cemento import (
    filtro_kalman_con_reinicio_setpoint,
    simular_setpoint_variable,
)

# %% Caso 2 — Filtro de Kalman con reinicialización al cambiar setpoint
datos = simular_setpoint_variable()
resultado = filtro_kalman_con_reinicio_setpoint(
    datos.medicion,
    datos.setpoint,
    sigma_medicion=datos.sigma_medicion,
)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(datos.medicion, label="Medición ruidosa", alpha=0.5)
ax.plot(datos.caudal_verdadero, label="Caudal verdadero (simulado)", linewidth=2)
ax.plot(resultado.estimacion, label="Estimación Kalman", linewidth=2)
ax.plot(datos.setpoint, label="Setpoint", linestyle="--", color="k")
ax.set_xlabel("Tiempo (k)")
ax.set_ylabel("Caudal (t/h)")
ax.set_title("Caso 2: Filtro de Kalman con cambios de setpoint")
ax.legend()
ax.grid(True)

ruta_png = guardar_figura_script(fig, __file__)
print(f"Gráfico guardado: {ruta_png}")
