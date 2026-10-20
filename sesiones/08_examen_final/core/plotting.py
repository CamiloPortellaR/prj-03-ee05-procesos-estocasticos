from pathlib import Path

import matplotlib.pyplot as plt

from .config import INTERACTIVO, RUTA_GRAFICOS


def guardar_figura(fig, nombre: str) -> Path:
    """Guarda figura en graficos/; en modo interactivo también la muestra inline."""
    ruta = RUTA_GRAFICOS / nombre
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    if INTERACTIVO:
        plt.show()
    else:
        plt.close(fig)
    return ruta
