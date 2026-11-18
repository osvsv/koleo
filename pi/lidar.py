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


def _agrupar(escaneo, alcance_max_cm, distancia_min_cm, zona_trasera=None):
    """Agrupa los puntos consecutivos (separados menos de SEPARACION_GRUPO_CM) dentro del rango.

    zona_trasera = (ángulo absoluto mínimo, distancia máxima): los puntos dentro de ella se ignoran.
    """
    puntos = sorted(
        (_normalizar(a), float(d))
        for a, d in escaneo
        if distancia_min_cm <= float(d) <= alcance_max_cm
    )
    if zona_trasera is not None:
        angulo_min, distancia_max = zona_trasera
        puntos = [p for p in puntos if not (abs(p[0]) >= angulo_min and p[1] <= distancia_max)]
    grupos = []
    for punto in puntos:
        if grupos and math.dist(_xy(*grupos[-1][-1]), _xy(*punto)) < SEPARACION_GRUPO_CM:
            grupos[-1].append(punto)
        else:
            grupos.append([punto])
    return grupos


def _cuerda(grupo):
    return math.dist(_xy(*grupo[0]), _xy(*grupo[-1]))


def _desviacion_max(grupo):
    """Mayor distancia de un punto a la recta que une los extremos del grupo."""
    (x1, y1), (x2, y2) = _xy(*grupo[0]), _xy(*grupo[-1])
    largo = math.hypot(x2 - x1, y2 - y1)
    if largo == 0:
        return 0.0
    return max(abs((x2 - x1) * (y1 - y) - (x1 - x) * (y2 - y1)) / largo
               for x, y in (_xy(*p) for p in grupo))


def _centro(grupo):
    """(distancia media, rumbo medio) del grupo."""
    return (sum(d for _, d in grupo) / len(grupo), sum(a for a, _ in grupo) / len(grupo))


def localizar_poste(escaneo, ancho_max_cm=12, min_puntos=2, alcance_max_cm=200, distancia_min_cm=15,
                   zona_trasera=(150, 40)):
    """Devuelve el grupo de puntos más cercano que parezca un poste, o None.

    zona_trasera ignora el actuador trasero; None desactiva el filtro (CC-020).
    """
    candidatos = []
    for grupo in _agrupar(escaneo, alcance_max_cm, distancia_min_cm, zona_trasera):
        if len(grupo) < min_puntos or _cuerda(grupo) > ancho_max_cm:
            continue
        distancia, rumbo = _centro(grupo)
        candidatos.append(Poste(distancia_cm=distancia, rumbo_grados=rumbo))
    if not candidatos:
        return None
    return min(candidatos, key=lambda p: p.distancia_cm)


def localizar_tarima(escaneo, ancho_min_cm=12, ancho_max_cm=50, ancho_lado_cm=29, min_puntos=4,
                     alcance_max_cm=200, distancia_min_cm=15, desviacion_max_cm=1.5):
    """Devuelve la tarima más cercana y el lado con que la ve el LIDAR, o None (CC-019).

    Descarta los grupos con algún punto a más de desviacion_max_cm de la recta de sus extremos (CC-020).
    """
    candidatos = []
    for grupo in _agrupar(escaneo, alcance_max_cm, distancia_min_cm):
        cuerda = _cuerda(grupo)
        if len(grupo) < min_puntos or cuerda <= ancho_min_cm or cuerda > ancho_max_cm:
            continue
        if _desviacion_max(grupo) > desviacion_max_cm:
            continue
        distancia, rumbo = _centro(grupo)
        lado = "FRENTE" if cuerda < ancho_lado_cm else "LADO"
        candidatos.append(Tarima(distancia_cm=distancia, rumbo_grados=rumbo, lado=lado, ancho_cm=cuerda))
    if not candidatos:
        return None
    return min(candidatos, key=lambda t: t.distancia_cm)
