
"""
Visualizador de parámetros y estados verdaderos de una bomba
=============================================================

Este script:
1. Lee los datos de mediciones simuladas.
2. Lee los estados verdaderos generados por el simulador.
3. Selecciona una bomba mediante su `pump_id`.
4. Grafica los parámetros medidos en subplots.
5. Sombrea el fondo según el estado verdadero S0...S6.
6. Dibuja líneas verticales en cada cambio de estado.

Dependencias
------------
pip install numpy pandas matplotlib

Archivos de entrada esperados
-----------------------------
salida_bombas/datos_bombas_mediciones.csv
salida_bombas/datos_bombas_estados.csv

Uso
---
1. Cambie BOMBA_ID por la bomba que desea visualizar.
2. Ejecute:

   python visualizar_bomba_estados.py

Salida
------
Se muestra la figura en pantalla y, opcionalmente, se guarda como PNG.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import pandas as pd


# ============================================================
# 1. CONFIGURACIÓN
# ============================================================

ARCHIVO_MEDICIONES = Path(
    "salida_bombas/datos_bombas_mediciones.csv"
)

ARCHIVO_ESTADOS = Path(
    "salida_bombas/datos_bombas_estados.csv"
)

# Identificador de la bomba que se desea visualizar.
BOMBA_ID = 1

# Rango opcional de días.
# Use None para mostrar toda la trayectoria.
DIA_INICIAL = None
DIA_FINAL = None

# Guardar la figura además de mostrarla.
GUARDAR_FIGURA = True

CARPETA_SALIDA = Path("salida_graficos")

# Resolución de la imagen guardada.
DPI_SALIDA = 180

# Transparencia de las áreas de estado.
ALPHA_ESTADOS = 0.18

# Mostrar líneas verticales donde cambia el estado.
MOSTRAR_LINEAS_CAMBIO = True

# Mostrar etiquetas de estado en la parte superior.
MOSTRAR_ETIQUETAS_ESTADO = True


# ============================================================
# 2. ESTADOS
# ============================================================

DESCRIPCIONES_ESTADOS: Dict[str, str] = {
    "S0": "Sin defectos",
    "S1": "Obstrucción leve",
    "S2": "Obstrucción severa",
    "S3": "Impulsor roto",
    "S4": "Falla media de rodamiento",
    "S5": "Falla alta de rodamiento",
    "S6": "Falla total",
}

# Colores de fondo para cada estado.
# Se pueden modificar libremente.
COLORES_ESTADOS: Dict[str, str] = {
    "S0": "#B7E4C7",
    "S1": "#FFF3B0",
    "S2": "#FFD166",
    "S3": "#F4A261",
    "S4": "#A8DADC",
    "S5": "#9D4EDD",
    "S6": "#E63946",
}


# ============================================================
# 3. VARIABLES A GRAFICAR
# ============================================================

VARIABLES_GRAFICO: List[Tuple[str, str, str]] = [
    (
        "vibration_rms_mm_s",
        "Vibración RMS",
        "mm/s",
    ),
    (
        "vibration_kurtosis",
        "Curtosis de vibración",
        "-",
    ),
    (
        "bearing_temperature_c",
        "Temperatura de rodamiento",
        "°C",
    ),
    (
        "suction_pressure_bar",
        "Presión de succión",
        "bar",
    ),
    (
        "discharge_pressure_bar",
        "Presión de descarga",
        "bar",
    ),
    (
        "delta_pressure_bar",
        "Diferencial de presión",
        "bar",
    ),
    (
        "flow_rate_m3_h",
        "Caudal",
        "m³/h",
    ),
    (
        "motor_power_kw",
        "Potencia del motor",
        "kW",
    ),
    (
        "rpm",
        "Velocidad",
        "rpm",
    ),
]


# ============================================================
# 4. LECTURA DE DATOS
# ============================================================

def leer_archivo(
    ruta: Path,
    columnas: List[str] | None = None,
) -> pd.DataFrame:
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo:\n{ruta}\n\n"
            "Verifique que el script esté en la carpeta correcta "
            "o modifique las rutas de entrada."
        )

    extension = ruta.suffix.lower()

    if extension == ".csv":
        return pd.read_csv(ruta, usecols=columnas)

    if extension in {".pkl", ".pickle"}:
        objeto = pd.read_pickle(ruta)

        if isinstance(objeto, pd.DataFrame):
            df = objeto.copy()

        elif isinstance(objeto, list):
            registros = []
            for elemento in objeto:
                if isinstance(elemento, list):
                    registros.extend(elemento)
                elif isinstance(elemento, dict):
                    registros.append(elemento)
                else:
                    raise TypeError(
                        "El Pickle contiene elementos no reconocidos."
                    )
            df = pd.DataFrame(registros)

        else:
            raise TypeError(
                "El archivo Pickle no contiene un DataFrame "
                "ni una lista de registros."
            )

        if columnas is not None:
            return df[columnas]

        return df

    raise ValueError(
        f"Formato no compatible para {ruta}. Use CSV o Pickle."
    )


def cargar_datos_bomba(
    bomba_id: int,
) -> pd.DataFrame:
    columnas_mediciones = [
        "pump_id",
        "day",
        *[variable[0] for variable in VARIABLES_GRAFICO],
    ]

    columnas_estados = [
        "pump_id",
        "day",
        "true_state",
    ]

    mediciones = leer_archivo(
        ARCHIVO_MEDICIONES,
        columnas_mediciones,
    )

    estados = leer_archivo(
        ARCHIVO_ESTADOS,
        columnas_estados,
    )

    mediciones_bomba = mediciones.loc[
        mediciones["pump_id"] == bomba_id
    ].copy()

    estados_bomba = estados.loc[
        estados["pump_id"] == bomba_id
    ].copy()

    if mediciones_bomba.empty:
        raise ValueError(
            f"No se encontraron mediciones para pump_id={bomba_id}."
        )

    if estados_bomba.empty:
        raise ValueError(
            f"No se encontraron estados para pump_id={bomba_id}."
        )

    datos = mediciones_bomba.merge(
        estados_bomba,
        on=["pump_id", "day"],
        how="inner",
        validate="one_to_one",
    )

    datos = datos.sort_values("day").reset_index(drop=True)

    if DIA_INICIAL is not None:
        datos = datos.loc[
            datos["day"] >= DIA_INICIAL
        ].copy()

    if DIA_FINAL is not None:
        datos = datos.loc[
            datos["day"] <= DIA_FINAL
        ].copy()

    if datos.empty:
        raise ValueError(
            "El rango de días seleccionado no contiene registros."
        )

    return datos


# ============================================================
# 5. SEGMENTOS DE ESTADO
# ============================================================

def obtener_segmentos_estado(
    datos: pd.DataFrame,
) -> List[Tuple[int, int, str]]:
    """
    Devuelve una lista:
        (día inicial, día final, estado)

    El intervalo se sombrea desde día inicial - 0.5
    hasta día final + 0.5.
    """
    dias = datos["day"].to_numpy(dtype=int)
    estados = datos["true_state"].astype(str).to_numpy()

    segmentos: List[Tuple[int, int, str]] = []

    inicio = dias[0]
    estado_actual = estados[0]

    for i in range(1, len(datos)):
        if estados[i] != estado_actual:
            fin = dias[i - 1]
            segmentos.append(
                (inicio, fin, estado_actual)
            )

            inicio = dias[i]
            estado_actual = estados[i]

    segmentos.append(
        (inicio, dias[-1], estado_actual)
    )

    return segmentos


# ============================================================
# 6. SOMBREADO DE ESTADOS
# ============================================================

def sombrear_estados(
    eje: plt.Axes,
    segmentos: List[Tuple[int, int, str]],
) -> None:
    for dia_inicio, dia_fin, estado in segmentos:
        color = COLORES_ESTADOS.get(
            estado,
            "#D3D3D3",
        )

        eje.axvspan(
            dia_inicio - 0.5,
            dia_fin + 0.5,
            facecolor=color,
            alpha=ALPHA_ESTADOS,
            edgecolor="none",
            zorder=0,
        )

        if MOSTRAR_LINEAS_CAMBIO and dia_inicio != segmentos[0][0]:
            eje.axvline(
                dia_inicio - 0.5,
                linewidth=0.8,
                linestyle="--",
                alpha=0.65,
                zorder=2,
            )


def agregar_etiquetas_estados(
    eje_superior: plt.Axes,
    segmentos: List[Tuple[int, int, str]],
) -> None:
    if not MOSTRAR_ETIQUETAS_ESTADO:
        return

    limite_inferior, limite_superior = eje_superior.get_ylim()
    altura = limite_superior - limite_inferior

    for dia_inicio, dia_fin, estado in segmentos:
        centro = (dia_inicio + dia_fin) / 2.0
        ancho = dia_fin - dia_inicio + 1

        # Evitar superposición excesiva en segmentos muy cortos.
        etiqueta = estado

        if ancho >= 8:
            etiqueta = (
                f"{estado}\n"
                f"{DESCRIPCIONES_ESTADOS.get(estado, '')}"
            )

        eje_superior.text(
            centro,
            limite_superior - 0.04 * altura,
            etiqueta,
            ha="center",
            va="top",
            fontsize=8,
            fontweight="bold",
            clip_on=True,
        )


# ============================================================
# 7. GRÁFICO
# ============================================================

def graficar_bomba(
    datos: pd.DataFrame,
    bomba_id: int,
) -> None:
    segmentos = obtener_segmentos_estado(datos)

    numero_graficos = len(VARIABLES_GRAFICO)

    figura, ejes = plt.subplots(
        numero_graficos,
        1,
        figsize=(15, 2.15 * numero_graficos),
        sharex=True,
        constrained_layout=True,
    )

    if numero_graficos == 1:
        ejes = np.array([ejes])

    dias = datos["day"].to_numpy()

    for eje, (columna, titulo, unidad) in zip(
        ejes,
        VARIABLES_GRAFICO,
    ):
        sombrear_estados(
            eje,
            segmentos,
        )

        eje.plot(
            dias,
            datos[columna].to_numpy(),
            linewidth=1.15,
            zorder=3,
        )

        etiqueta_y = titulo

        if unidad != "-":
            etiqueta_y += f"\n[{unidad}]"

        eje.set_ylabel(
            etiqueta_y,
            fontsize=9,
        )

        eje.grid(
            True,
            alpha=0.25,
            linewidth=0.6,
        )

        eje.margins(x=0)

    agregar_etiquetas_estados(
        ejes[0],
        segmentos,
    )

    ejes[-1].set_xlabel(
        "Día de simulación",
        fontsize=10,
    )

    figura.suptitle(
        f"Evolución de parámetros y estados verdaderos — Bomba {bomba_id}",
        fontsize=14,
        fontweight="bold",
    )

    # Leyenda única para los estados presentes.
    estados_presentes = []
    for _, _, estado in segmentos:
        if estado not in estados_presentes:
            estados_presentes.append(estado)

    elementos_leyenda = [
        Patch(
            facecolor=COLORES_ESTADOS.get(
                estado,
                "#D3D3D3",
            ),
            alpha=0.45,
            label=(
                f"{estado}: "
                f"{DESCRIPCIONES_ESTADOS.get(estado, estado)}"
            ),
        )
        for estado in estados_presentes
    ]

    figura.legend(
        handles=elementos_leyenda,
        loc="outside upper center",
        ncol=min(4, len(elementos_leyenda)),
        frameon=True,
        fontsize=8,
    )

    if GUARDAR_FIGURA:
        CARPETA_SALIDA.mkdir(
            parents=True,
            exist_ok=True,
        )

        ruta_salida = (
            CARPETA_SALIDA
            / f"bomba_{bomba_id}_parametros_estados.png"
        )

        figura.savefig(
            ruta_salida,
            dpi=DPI_SALIDA,
            bbox_inches="tight",
        )

        print(
            f"Figura guardada en:\n{ruta_salida.resolve()}"
        )

    plt.show()


# ============================================================
# 8. RESUMEN DE LA BOMBA
# ============================================================

def mostrar_resumen(
    datos: pd.DataFrame,
    bomba_id: int,
) -> None:
    segmentos = obtener_segmentos_estado(datos)

    print(f"\nBomba seleccionada: {bomba_id}")
    print(
        f"Rango de días: "
        f"{datos['day'].min()} a {datos['day'].max()}"
    )

    print("\nEstados observados:")

    for dia_inicio, dia_fin, estado in segmentos:
        duracion = dia_fin - dia_inicio + 1

        print(
            f"- {estado}: "
            f"{DESCRIPCIONES_ESTADOS.get(estado, '')} | "
            f"días {dia_inicio}-{dia_fin} | "
            f"duración {duracion} días"
        )


# ============================================================
# 9. PROGRAMA PRINCIPAL
# ============================================================

def main() -> None:
    print("Leyendo datos de la bomba...")

    datos = cargar_datos_bomba(
        BOMBA_ID
    )

    mostrar_resumen(
        datos,
        BOMBA_ID,
    )

    print("\nGenerando gráfico...")

    graficar_bomba(
        datos,
        BOMBA_ID,
    )


if __name__ == "__main__":
    main()
