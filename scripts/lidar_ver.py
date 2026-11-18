"""Dibuja escaneos del LIDAR con las detecciones de tarima y poste (se ejecuta en la laptop).

Uso: python scripts/lidar_ver.py vueltas.json [salida.png]
"""
import json
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pi.lidar import localizar_poste, localizar_tarima  # noqa: E402

entrada = sys.argv[1]
salida = sys.argv[2] if len(sys.argv) > 2 else "escaneo.png"
vueltas = json.load(open(entrada))
indices = sorted({0, len(vueltas) - 1})
fig, axs = plt.subplots(1, len(indices), figsize=(6.5 * len(indices), 6.5), squeeze=False)
for i, ax in zip(indices, axs[0]):
    e = vueltas[i]
    # x al frente (arriba), y a la izquierda (izquierda de la imagen)
    ax.scatter([-d * math.sin(math.radians(a)) for a, d in e], [d * math.cos(math.radians(a)) for a, d in e], s=8, c="#555")
    ax.plot(0, 0, "k^", ms=12)
    t, p = localizar_tarima(e), localizar_poste(e)
    for obj, col, nom in ((t, "tab:orange", "TARIMA"), (p, "tab:green", "POSTE")):
        if obj:
            r = math.radians(obj.rumbo_grados)
            x, y = -obj.distancia_cm * math.sin(r), obj.distancia_cm * math.cos(r)
            ax.scatter([x], [y], s=400, facecolors="none", edgecolors=col, lw=3)
            extra = f" {obj.lado} {obj.ancho_cm:.0f}cm" if nom == "TARIMA" else ""
            ax.annotate(f"{nom}{extra}\n{obj.distancia_cm:.0f} cm, {obj.rumbo_grados:.0f}°", (x, y),
                        xytext=(12, 12), textcoords="offset points", color=col, weight="bold")
    print(f"vuelta {i + 1}: puntos={len(e)} tarima={t} poste={p}")
    ax.set_aspect("equal")
    ax.set_xlim(-250, 250)
    ax.set_ylim(-250, 250)
    ax.grid(alpha=0.3)
    ax.set_title(f"vuelta {i + 1}: tarima={'sí' if t else 'no'}, poste={'sí' if p else 'no'}")
fig.suptitle("RPLIDAR real (arriba = frente, izquierda = +ángulo), cm")
fig.savefig(salida, dpi=80)
