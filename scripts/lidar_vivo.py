"""Ventana en tiempo real: lee vueltas del LIDAR por stdin (una lista JSON por línea) y marca lo que
detectan `localizar_tarima` y `localizar_poste` de pi/lidar.py (se ejecuta en la laptop).

Uso: ... | python scripts/lidar_vivo.py [--max N] [--png salida.png]
  --max N        termina tras N vueltas (para pruebas); --png guarda la última imagen (sin ventana).
Cierra la ventana o pulsa Ctrl+C para salir.
"""
import argparse
import json
import math
import queue
import sys
import threading
from pathlib import Path

import matplotlib

sys.stdout.reconfigure(encoding="utf-8")

ap = argparse.ArgumentParser()
ap.add_argument("--max", type=int, default=0)
ap.add_argument("--png")
args = ap.parse_args()
matplotlib.use("Agg" if args.png else "TkAgg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pi.lidar import localizar_poste, localizar_tarima  # noqa: E402

cola = queue.Queue(maxsize=2)


def lector():
    for linea in sys.stdin:
        try:
            vuelta = json.loads(linea)
        except ValueError:
            continue
        if cola.full():  # siempre la vuelta más reciente
            try:
                cola.get_nowait()
            except queue.Empty:
                pass
        cola.put(vuelta)
    cola.put(None)


threading.Thread(target=lector, daemon=True).start()


def xy(a, d):  # x a la izquierda de la imagen = ángulo positivo; arriba = frente
    r = math.radians(a)
    return -d * math.sin(r), d * math.cos(r)


fig, ax = plt.subplots(figsize=(7.5, 7.5))
ax.set_aspect("equal")
ax.set_xlim(-250, 250)
ax.set_ylim(-250, 250)
ax.grid(alpha=0.3)
ax.plot(0, 0, "k^", ms=12)
puntos = ax.scatter([], [], s=8, c="#555")
aro_t = ax.scatter([], [], s=450, facecolors="none", edgecolors="tab:orange", lw=3)
aro_p = ax.scatter([], [], s=450, facecolors="none", edgecolors="tab:green", lw=3)
txt_t = ax.text(0.02, 0.97, "", transform=ax.transAxes, va="top", color="tab:orange", weight="bold")
txt_p = ax.text(0.02, 0.91, "", transform=ax.transAxes, va="top", color="tab:green", weight="bold")
ax.set_title("RPLIDAR en vivo (arriba = frente, izquierda = +ángulo), cm")
n = 0
while plt.fignum_exists(fig.number):
    try:
        v = cola.get(timeout=0.2)
    except queue.Empty:
        plt.pause(0.01)
        continue
    if v is None:
        break
    n += 1
    t, p = localizar_tarima(v), localizar_poste(v)
    puntos.set_offsets([xy(a, d) for a, d in v])
    aro_t.set_offsets([xy(t.rumbo_grados, t.distancia_cm)] if t else [[1e6, 1e6]])
    aro_p.set_offsets([xy(p.rumbo_grados, p.distancia_cm)] if p else [[1e6, 1e6]])
    txt_t.set_text(f"TARIMA {t.lado} {t.ancho_cm:.0f} cm a {t.distancia_cm:.0f} cm, {t.rumbo_grados:.0f}°" if t else "TARIMA: no detectada")
    txt_p.set_text(f"POSTE a {p.distancia_cm:.0f} cm, {p.rumbo_grados:.0f}°" if p else "POSTE: no detectado")
    print(f"vuelta {n:4d} | puntos {len(v):3d} | {txt_t.get_text()} | {txt_p.get_text()}", flush=True)
    if args.png:
        fig.savefig(args.png, dpi=80)
    else:
        fig.canvas.draw_idle()
        plt.pause(0.01)
    if args.max and n >= args.max:
        break
