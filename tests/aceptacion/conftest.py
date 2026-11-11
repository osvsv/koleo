"""Configuración común de las pruebas de aceptación (el repositorio raíz va en sys.path)."""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
for ruta in (str(RAIZ), str(Path(__file__).resolve().parent)):
    if ruta not in sys.path:
        sys.path.insert(0, ruta)
