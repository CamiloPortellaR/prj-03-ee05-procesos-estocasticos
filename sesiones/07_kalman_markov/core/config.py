import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

RUTA_SESION = Path(__file__).resolve().parent.parent
RUTA_DATA = RUTA_SESION / "data"
RUTA_DOCS = RUTA_SESION / "docs"
RUTA_GRAFICOS = RUTA_SESION / "graficos"
RUTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

RNG = np.random.default_rng(123456)


def _modo_interactivo() -> bool:
    if "ipykernel" in sys.modules:
        return True
    try:
        from IPython import get_ipython

        ip = get_ipython()
        return ip is not None and ip.__class__.__name__ in (
            "ZMQInteractiveShell",
            "TerminalInteractiveShell",
        )
    except ImportError:
        return False


INTERACTIVO = _modo_interactivo()

plt.style.use("ggplot")
plt.rcParams.update({"figure.figsize": (14, 8), "font.size": 12})
if INTERACTIVO:
    from IPython import get_ipython

    get_ipython().run_line_magic("matplotlib", "inline")
