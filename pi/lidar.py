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


def _douglas_peucker(xy, tolerancia, i=0, j=None):
    """Índices de los vértices de la polilínea simplificada entre i y j (ambos incluidos)."""
    if j is None:
        j = len(xy) - 1
    (x1, y1), (x2, y2) = xy[i], xy[j]
    largo = math.hypot(x2 - x1, y2 - y1)
    mejor, k = -1.0, None
    for n in range(i + 1, j):
        x, y = xy[n]
        if largo == 0:
            d = math.hypot(x - x1, y - y1)
        else:
            d = abs((x2 - x1) * (y1 - y) - (x1 - x) * (y2 - y1)) / largo
        if d > mejor:
            mejor, k = d, n
    if k is None or mejor <= tolerancia:
        return [i, j]
    izq = _douglas_peucker(xy, tolerancia, i, k)
    der = _douglas_peucker(xy, tolerancia, k, j)
    return izq[:-1] + der


def _desviacion_tramo(xy, i, j):
    (x1, y1), (x2, y2) = xy[i], xy[j]
    largo = math.hypot(x2 - x1, y2 - y1)
    if largo == 0:
        return max(math.hypot(x - x1, y - y1) for x, y in xy[i:j + 1])
    return max(abs((x2 - x1) * (y1 - y) - (x1 - x) * (y2 - y1)) / largo for x, y in xy[i:j + 1])


def _vertices(xy, tolerancia):
    """Douglas-Peucker y después se quitan los vértices que sobran: DP corta primero en el punto más
    lejano de la cuerda, que no siempre es una esquina, y deja cortes espurios dentro de un tramo recto."""
    vertices = _douglas_peucker(xy, tolerancia)
    while len(vertices) > 2:
        mejor, k = None, None
        for n in range(1, len(vertices) - 1):
            d = _desviacion_tramo(xy, vertices[n - 1], vertices[n + 1])
            if d <= tolerancia and (mejor is None or d < mejor):
                mejor, k = d, n
        if k is None:
            break
        del vertices[k]
    return vertices


def _recta(puntos):
    """(centroide, dirección unitaria) del ajuste por mínimos cuadrados totales, de primero a último punto."""
    n = len(puntos)
    cx = sum(p[0] for p in puntos) / n
    cy = sum(p[1] for p in puntos) / n
    sxx = sum((p[0] - cx) ** 2 for p in puntos)
    syy = sum((p[1] - cy) ** 2 for p in puntos)
    sxy = sum((p[0] - cx) * (p[1] - cy) for p in puntos)
    theta = 0.5 * math.atan2(2 * sxy, sxx - syy)
    d = (math.cos(theta), math.sin(theta))
    if d[0] * (puntos[-1][0] - puntos[0][0]) + d[1] * (puntos[-1][1] - puntos[0][1]) < 0:
        d = (-d[0], -d[1])
    return (cx, cy), d


def _interseccion(r1, r2):
    (x1, y1), (dx1, dy1) = r1
    (x2, y2), (dx2, dy2) = r2
    den = dx1 * dy2 - dy1 * dx2
    if abs(den) < 1e-9:
        return None
    t = ((x2 - x1) * dy2 - (y2 - y1) * dx2) / den
    return x1 + t * dx1, y1 + t * dy1


def _angulo_entre(a, b):
    c = max(-1.0, min(1.0, a[0] * b[0] + a[1] * b[1]))
    return math.degrees(math.acos(c))


def _evaluar_tarima(grupo, p):
    """Devuelve una Tarima si el grupo es ala-cara-ala, o None."""
    xy = [_xy(*q) for q in grupo]
    vertices = _vertices(xy, p["desviacion_max_cm"])
    if len(vertices) != 4:
        return None
    tramos = [xy[vertices[k]:vertices[k + 1] + 1] for k in range(3)]
    if any(len(t) < p["min_puntos_tramo"] for t in tramos):
        return None
    rectas = [_recta(t) for t in tramos]
    esq1 = _interseccion(rectas[0], rectas[1])
    esq2 = _interseccion(rectas[1], rectas[2])
    if esq1 is None or esq2 is None:
        return None
    cara = math.dist(esq1, esq2)
    if not (p["ancho_min_cm"] < cara <= p["ancho_max_cm"]):
        return None
    dc = rectas[1][1]
    libre1, libre2 = tramos[0][0], tramos[2][-1]
    largo1, largo2 = math.dist(libre1, esq1), math.dist(libre2, esq2)
    ang1 = _angulo_entre(rectas[0][1], dc)
    ang2 = _angulo_entre(rectas[2][1], dc)
    for largo, ang in ((largo1, ang1), (largo2, ang2)):
        if (abs(largo - p["ala_cm"]) > p["ala_tol_cm"]
                or abs(ang - p["angulo_ala_grados"]) > p["angulo_tol_grados"]):
            return None
    if abs(largo1 - largo2) > p["ala_tol_cm"] or abs(ang1 - ang2) > p["angulo_tol_grados"]:
        return None
    # normal a la cara hacia el LIDAR (el origen); los dos extremos libres deben quedar de ese lado
    n = (-dc[1], dc[0])
    if n[0] * (0 - esq1[0]) + n[1] * (0 - esq1[1]) < 0:
        n = (-n[0], -n[1])
    for libre, esq in ((libre1, esq1), (libre2, esq2)):
        if (libre[0] - esq[0]) * n[0] + (libre[1] - esq[1]) * n[1] <= 0:
            return None
    cx, cy = (esq1[0] + esq2[0]) / 2, (esq1[1] + esq2[1]) / 2
    lado = "FRENTE" if cara < p["ancho_lado_cm"] else "LADO"
    return Tarima(distancia_cm=math.hypot(cx, cy), rumbo_grados=math.degrees(math.atan2(cy, cx)),
                  lado=lado, ancho_cm=cara)


def localizar_tarima(escaneo, ancho_min_cm=12, ancho_max_cm=50, ancho_lado_cm=29, ala_cm=20, ala_tol_cm=5,
                     angulo_ala_grados=45, angulo_tol_grados=10, min_puntos_tramo=3, alcance_max_cm=200,
                     distancia_min_cm=15, desviacion_max_cm=1.5):
    """Devuelve la tarima con alas más cercana y el lado con que la ve el LIDAR, o None (CC-019, CC-021).

    Cada grupo se parte con Douglas-Peucker (tolerancia desviacion_max_cm); es tarima solo si resultan
    exactamente tres tramos rectos (ala, cara, ala) que cumplen los largos y ángulos pedidos.
    """
    parametros = dict(ancho_min_cm=ancho_min_cm, ancho_max_cm=ancho_max_cm, ancho_lado_cm=ancho_lado_cm,
                      ala_cm=ala_cm, ala_tol_cm=ala_tol_cm, angulo_ala_grados=angulo_ala_grados,
                      angulo_tol_grados=angulo_tol_grados, min_puntos_tramo=min_puntos_tramo,
                      desviacion_max_cm=desviacion_max_cm)
    candidatos = []
    for grupo in _agrupar(escaneo, alcance_max_cm, distancia_min_cm):
        tarima = _evaluar_tarima(grupo, parametros)
        if tarima is not None:
            candidatos.append(tarima)
    if not candidatos:
        return None
    return min(candidatos, key=lambda t: t.distancia_cm)
