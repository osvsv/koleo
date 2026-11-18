"""Localización del poste de destino en un escaneo del LIDAR (WP-4.4, REQ-F-006).

El escaneo son pares (ángulo en grados, distancia en cm) con 0° al frente y positivo a la izquierda.
"""
import math
from dataclasses import dataclass

SEPARACION_GRUPO_CM = 5.0


@dataclass
class Poste:
    distancia_cm: float
    rumbo_grados: float


def _normalizar(angulo):
    return (float(angulo) + 180.0) % 360.0 - 180.0


def _xy(angulo, distancia):
    a = math.radians(angulo)
    return distancia * math.cos(a), distancia * math.sin(a)


def localizar_poste(escaneo, ancho_max_cm=12, min_puntos=2, alcance_max_cm=200, distancia_min_cm=15):
    """Devuelve el grupo de puntos más cercano que parezca un poste, o None."""
    puntos = sorted(
        (_normalizar(a), float(d))
        for a, d in escaneo
        if distancia_min_cm <= float(d) <= alcance_max_cm
    )
    grupos = []
    for punto in puntos:
        if grupos and math.dist(_xy(*grupos[-1][-1]), _xy(*punto)) < SEPARACION_GRUPO_CM:
            grupos[-1].append(punto)
        else:
            grupos.append([punto])

    candidatos = []
    for grupo in grupos:
        if len(grupo) < min_puntos:
            continue
        cuerda = math.dist(_xy(*grupo[0]), _xy(*grupo[-1]))
        if cuerda > ancho_max_cm:
            continue
        distancia = sum(d for _, d in grupo) / len(grupo)
        rumbo = sum(a for a, _ in grupo) / len(grupo)
        candidatos.append(Poste(distancia_cm=distancia, rumbo_grados=rumbo))
    if not candidatos:
        return None
    return min(candidatos, key=lambda p: p.distancia_cm)
