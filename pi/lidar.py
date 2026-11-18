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


@dataclass
class Tarima:
    distancia_cm: float
    rumbo_grados: float
    lado: str
    ancho_cm: float


def _normalizar(angulo):
    return (float(angulo) + 180.0) % 360.0 - 180.0


def _xy(angulo, distancia):
    a = math.radians(angulo)
    return distancia * math.cos(a), distancia * math.sin(a)


def _agrupar(escaneo, alcance_max_cm, distancia_min_cm):
    """Agrupa los puntos consecutivos (separados menos de SEPARACION_GRUPO_CM) dentro del rango."""
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
    return grupos


def _cuerda(grupo):
    return math.dist(_xy(*grupo[0]), _xy(*grupo[-1]))


def _centro(grupo):
    """(distancia media, rumbo medio) del grupo."""
    return (sum(d for _, d in grupo) / len(grupo), sum(a for a, _ in grupo) / len(grupo))


def localizar_poste(escaneo, ancho_max_cm=12, min_puntos=2, alcance_max_cm=200, distancia_min_cm=15):
    """Devuelve el grupo de puntos más cercano que parezca un poste, o None."""
    candidatos = []
    for grupo in _agrupar(escaneo, alcance_max_cm, distancia_min_cm):
        if len(grupo) < min_puntos or _cuerda(grupo) > ancho_max_cm:
            continue
        distancia, rumbo = _centro(grupo)
        candidatos.append(Poste(distancia_cm=distancia, rumbo_grados=rumbo))
    if not candidatos:
        return None
    return min(candidatos, key=lambda p: p.distancia_cm)


def localizar_tarima(escaneo, ancho_min_cm=12, ancho_max_cm=50, ancho_lado_cm=29, min_puntos=4,
                     alcance_max_cm=200, distancia_min_cm=15):
    """Devuelve la tarima más cercana y el lado con que la ve el LIDAR, o None (CC-019)."""
    candidatos = []
    for grupo in _agrupar(escaneo, alcance_max_cm, distancia_min_cm):
        cuerda = _cuerda(grupo)
        if len(grupo) < min_puntos or cuerda <= ancho_min_cm or cuerda > ancho_max_cm:
            continue
        distancia, rumbo = _centro(grupo)
        lado = "FRENTE" if cuerda < ancho_lado_cm else "LADO"
        candidatos.append(Tarima(distancia_cm=distancia, rumbo_grados=rumbo, lado=lado, ancho_cm=cuerda))
    if not candidatos:
        return None
    return min(candidatos, key=lambda t: t.distancia_cm)
