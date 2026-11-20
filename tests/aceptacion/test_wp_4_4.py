"""WP-4.4 — Localización del destino con LIDAR (CA-4.4.1 a CA-4.4.14, CC-014, CC-019, CC-020, CC-021).

Los escaneos son sintéticos (puntos cada 1°, 0° al frente y positivo a la izquierda) y se generan
con trigonometría: un poste de 6 cm, una pared recta, una cara plana de 18 cm (de frente) o 40 cm
(de lado) y, desde CC-021, la tarima con alas (cara más dos alas rectas de 20 cm a 45° de la
prolongación de la cara, abiertas hacia el robot, trazadas por rayos contra la polilínea).
CA-4.4.8 es física (Pi con el RPLIDAR A1) y no tiene prueba aquí.
CA-4.4.7 es de inspección del repositorio.
CA-4.4.9 a CA-4.4.12 (CC-019, CC-021, EJ-035 y EJ-036) cubren `localizar_tarima` y `Tarima`.
CA-4.4.13 (CC-020, CC-021) cubre la estrictez de las alas y el ruido de ±0.5 cm; CA-4.4.14 (CC-020,
SUP-042) cubre `zona_trasera` de `localizar_poste` (actuador lineal a 25 cm y 175°). El ruido es
determinista (patrón fijo, sin aleatoriedad).
"""
import math
import re
import time
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]


# --------------------------------------------------------------------------- generadores
def _poste(distancia_cm, rumbo_grados, diametro_cm=6.0):
    """{ángulo: distancia} de un poste cilíndrico. `distancia_cm` es la distancia a la mitad de la
    profundidad visible (centro a +1.5 cm): la distancia a la superficie y al centro quedan a ±1.5."""
    radio = diametro_cm / 2
    centro = distancia_cm + radio / 2
    golpes = {}
    for a in range(-180, 180):
        fi = math.radians(a - rumbo_grados)
        perp = centro * math.sin(fi)
        if math.cos(fi) > 0 and abs(perp) <= radio:
            golpes[a] = centro * math.cos(fi) - math.sqrt(radio ** 2 - perp ** 2)
    return golpes


def _pared(distancia_cm=120.0, semiangulo=40):
    return {a: distancia_cm / math.cos(math.radians(a)) for a in range(-semiangulo, semiangulo + 1)}


def _cara_plana(distancia_cm, ancho_cm, rumbo_grados=0):
    """Cara frontal plana (perpendicular al eje del rumbo) de ancho `ancho_cm`."""
    golpes = {}
    for a in range(-90, 91):
        fi = math.radians(a - rumbo_grados)
        if abs(math.cos(fi)) < 1e-9:
            continue
        lateral = distancia_cm * math.tan(fi)
        if abs(lateral) <= ancho_cm / 2:
            golpes[a] = distancia_cm / math.cos(fi)
    return golpes


def _escaneo(*capas):
    """Une capas {ángulo: distancia}; en cada ángulo gana el punto más cercano (oclusión)."""
    union = {}
    for capa in capas:
        for a, r in capa.items():
            union[a] = min(r, union.get(a, r))
    return [(float(a), round(r, 2)) for a, r in sorted(union.items())]


# --------------------------------------------------------------------------- CA-4.4.1
def test_ca_4_4_1_poste_de_6_cm_a_100_cm_y_20_grados():
    """CA-4.4.1 / EJ-011"""
    from pi.lidar import Poste, localizar_poste
    poste = localizar_poste(_escaneo(_poste(100, 20)))
    assert isinstance(poste, Poste)
    assert poste.distancia_cm == pytest.approx(100, abs=3)
    assert poste.rumbo_grados == pytest.approx(20, abs=2)


# --------------------------------------------------------------------------- CA-4.4.2
def test_ca_4_4_2_solo_pared_devuelve_none():
    """CA-4.4.2 / EJ-012"""
    from pi.lidar import localizar_poste
    assert localizar_poste(_escaneo(_pared(120))) is None


def test_ca_4_4_2_escaneo_vacio_devuelve_none():
    """CA-4.4.2"""
    from pi.lidar import localizar_poste
    assert localizar_poste([]) is None


def test_ca_4_4_2_puntos_sueltos_de_uno_en_uno_devuelven_none():
    """CA-4.4.2"""
    from pi.lidar import localizar_poste
    sueltos = [(-60.0, 100.0), (-20.0, 100.0), (20.0, 100.0), (60.0, 100.0)]
    assert localizar_poste(sueltos) is None


# --------------------------------------------------------------------------- CA-4.4.3
@pytest.mark.parametrize("ancho", [18, 40])
def test_ca_4_4_3_tarima_no_es_poste(ancho):
    """CA-4.4.3 / EJ-012: tarima de frente (18 cm) y de lado (40 cm) a 100 cm."""
    from pi.lidar import localizar_poste
    assert localizar_poste(_escaneo(_cara_plana(100, ancho))) is None


# --------------------------------------------------------------------------- CA-4.4.4
def test_ca_4_4_4_poste_frente_a_pared_devuelve_el_poste():
    """CA-4.4.4"""
    from pi.lidar import localizar_poste
    poste = localizar_poste(_escaneo(_pared(120), _poste(100, 0)))
    assert poste is not None
    assert poste.distancia_cm == pytest.approx(100, abs=3)
    assert poste.rumbo_grados == pytest.approx(0, abs=2)


def test_ca_4_4_4_poste_frente_a_pared_fuera_del_eje():
    """CA-4.4.4"""
    from pi.lidar import localizar_poste
    poste = localizar_poste(_escaneo(_pared(120), _poste(100, 20)))
    assert poste is not None
    assert poste.distancia_cm == pytest.approx(100, abs=3)
    assert poste.rumbo_grados == pytest.approx(20, abs=2)


def test_ca_4_4_4_con_dos_postes_devuelve_el_mas_cercano():
    """CA-4.4.4"""
    from pi.lidar import localizar_poste
    poste = localizar_poste(_escaneo(_poste(150, -30), _poste(100, 20)))
    assert poste is not None
    assert poste.distancia_cm == pytest.approx(100, abs=3)
    assert poste.rumbo_grados == pytest.approx(20, abs=2)


# --------------------------------------------------------------------------- CA-4.4.5
def test_ca_4_4_5_puntos_a_menos_de_distancia_min_se_ignoran():
    """CA-4.4.5: grupo del tamaño de un poste a 10 cm (el propio robot) no cuenta."""
    from pi.lidar import localizar_poste
    cuerpo = [(0.0, 10.0), (1.0, 10.0), (2.0, 10.0)]
    assert localizar_poste(cuerpo) is None


def test_ca_4_4_5_el_robot_no_tapa_al_poste_real():
    """CA-4.4.5: con el poste a 100 cm y puntos del robot a 10 cm, devuelve el poste a 100 cm."""
    from pi.lidar import localizar_poste
    cuerpo = [(100.0, 10.0), (101.0, 10.0), (102.0, 10.0)]
    poste = localizar_poste(_escaneo(_poste(100, 20)) + cuerpo)
    assert poste is not None
    assert poste.distancia_cm == pytest.approx(100, abs=3)


def test_ca_4_4_5_puntos_a_mas_de_alcance_max_se_ignoran():
    """CA-4.4.5: grupo del tamaño de un poste a 250 cm (más allá de 200 cm) no cuenta."""
    from pi.lidar import localizar_poste
    lejano = [(0.0, 250.0), (1.0, 250.0), (2.0, 250.0)]
    assert localizar_poste(lejano) is None


def test_ca_4_4_5_el_poste_lejano_no_tapa_al_poste_real():
    """CA-4.4.5"""
    from pi.lidar import localizar_poste
    lejano = [(-80.0, 250.0), (-79.0, 250.0), (-78.0, 250.0)]
    poste = localizar_poste(_escaneo(_poste(150, 0)) + lejano)
    assert poste is not None
    assert poste.distancia_cm == pytest.approx(150, abs=3)


# --------------------------------------------------------------------------- CA-4.4.6
class DriverFalso:
    """Imita la biblioteca `rplidar` (PyPI): iter_scans -> listas de (calidad, ángulo, mm);
    iter_measures -> (nueva_vuelta, calidad, ángulo, mm). Cualquier otro método es un no-op."""

    def __init__(self, vueltas, espera_s=0.0):
        self.vueltas = vueltas
        self.espera_s = espera_s

    def iter_scans(self, *args, **kwargs):
        if self.espera_s:
            time.sleep(self.espera_s)
        for vuelta in self.vueltas:
            yield list(vuelta)

    def iter_measures(self, *args, **kwargs):
        if self.espera_s:
            time.sleep(self.espera_s)
        for vuelta in self.vueltas:
            for i, (calidad, angulo, mm) in enumerate(vuelta):
                yield (i == 0, calidad, angulo, mm)
        if self.vueltas:
            yield (True, 0, 0.0, 0.0)  # cierre de la vuelta siguiente

    def __getattr__(self, nombre):
        return lambda *a, **k: None


def test_ca_4_4_6_escanear_devuelve_pares_angulo_distancia_en_cm():
    """CA-4.4.6"""
    from pi.rplidar import RPLidarA1
    vuelta = [(15, 0.0, 1000.0), (15, 1.0, 1000.0), (15, 2.0, 1010.0)]
    lidar = RPLidarA1("/puerto/falso", driver=DriverFalso([vuelta]))
    pares = lidar.escanear(timeout_s=1.0)
    assert len(pares) == 3
    assert all(len(p) == 2 for p in pares)
    distancias = sorted(round(float(d), 1) for _, d in pares)
    assert distancias == [100.0, 100.0, 101.0]  # mm -> cm
    angulo_cero = [a for a, d in pares if abs(float(d) - 100.0) < 0.05 and abs(float(a) % 360) < 1e-6]
    assert angulo_cero, "el punto a 0° debe seguir a 0°"


def test_ca_4_4_6_sin_vuelta_lanza_lidar_sin_datos():
    """CA-4.4.6"""
    from pi.rplidar import LidarSinDatos, RPLidarA1
    lidar = RPLidarA1("/puerto/falso", driver=DriverFalso([], espera_s=0.05))
    t0 = time.monotonic()
    with pytest.raises(LidarSinDatos):
        lidar.escanear(timeout_s=0.3)
    assert time.monotonic() - t0 < 5


def test_ca_4_4_6_el_puerto_sale_de_la_variable_de_entorno_y_no_hay_valores_fijos():
    """CA-4.4.6: KOLEO_LIDAR_PUERTO se usa en pi/rplidar.py y no hay puertos fijos en pi/."""
    codigo = (RAIZ / "pi" / "rplidar.py").read_text(encoding="utf-8")
    assert "KOLEO_LIDAR_PUERTO" in codigo
    fijo = re.compile(r"""["'](/dev/tty|COM\d)""")
    for archivo in (RAIZ / "pi").rglob("*.py"):
        assert not fijo.search(archivo.read_text(encoding="utf-8")), f"puerto fijo en {archivo}"


# --------------------------------------------------------------------------- CA-4.4.7
def test_ca_4_4_7_se_eliminaron_qr_y_camara():
    """CA-4.4.7 (inspección del repositorio, CC-014)"""
    assert not (RAIZ / "pi" / "qr.py").exists()
    assert not (RAIZ / "pi" / "camara.py").exists()


def test_ca_4_4_7_requirements_sin_opencv():
    """CA-4.4.7 (inspección del repositorio, CC-014)"""
    requisitos = RAIZ / "requirements.txt"
    assert requisitos.exists()
    assert "opencv" not in requisitos.read_text(encoding="utf-8").lower()


# --------------------------------------------------------------------------- generadores de CC-021
def _trazar(vertices_uv, rumbo_grados):
    """{ángulo: distancia} de una polilínea, con rayos cada 1° (gana el impacto más cercano). Los vértices
    están en el marco local de la tarima: u = a lo largo del rumbo, v = lateral (positivo a la izquierda)."""
    rho = math.radians(rumbo_grados)
    pts = [(u * math.cos(rho) - v * math.sin(rho), u * math.sin(rho) + v * math.cos(rho))
           for u, v in vertices_uv]
    golpes = {}
    for a in range(-180, 180):
        dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
        mejor = None
        for (px, py), (qx, qy) in zip(pts, pts[1:]):
            ex, ey = qx - px, qy - py
            den = dx * ey - dy * ex
            if abs(den) < 1e-12:
                continue
            t = (px * ey - py * ex) / den   # distancia sobre el rayo
            s = (px * dy - py * dx) / den   # posición sobre el segmento (0..1)
            if t > 0 and -1e-9 <= s <= 1 + 1e-9 and (mejor is None or t < mejor):
                mejor = t
        if mejor is not None:
            golpes[a] = mejor
    return golpes


def _ala(extremo, signo_v, largo, angulo, hacia=True, abombamiento=0.0):
    """Puntos del ala desde `extremo` (u, v) de la cara hasta su extremo libre, a `angulo` grados de la
    prolongación de la cara. `hacia`: el extremo libre queda más cerca del robot (u menor)."""
    u0, v0 = extremo
    a = math.radians(angulo)
    du = (-1 if hacia else 1) * math.sin(a) * largo
    dv = signo_v * math.cos(a) * largo
    if not abombamiento:
        return [(u0, v0), (u0 + du, v0 + dv)]
    nu, nv = dv / largo, -du / largo  # normal unitaria al ala
    n = 12
    return [(u0 + du * i / n + nu * 4 * abombamiento * (i / n) * (1 - i / n),
             v0 + dv * i / n + nv * 4 * abombamiento * (i / n) * (1 - i / n)) for i in range(n + 1)]


def _tarima(distancia_cm, rumbo_grados, lado="FRENTE", ancho_cm=None, ala_cm=20.0, ang_izq=45.0, ang_der=45.0,
            hacia=True, ala_izq=True, ala_der=True, abombamiento_izq=0.0):
    """Tarima con alas: cara plana de 18 cm (FRENTE) o 40 cm (LADO) con su centro a `distancia_cm` y
    `rumbo_grados`, y dos alas rectas de `ala_cm` a 45° de la prolongación de la cara, abiertas hacia el
    robot (extremos libres más cerca del LIDAR)."""
    ancho = ancho_cm if ancho_cm is not None else (18.0 if lado == "FRENTE" else 40.0)
    d, m = distancia_cm, ancho / 2
    cadena = []
    if ala_izq:
        cadena += list(reversed(_ala((d, -m), -1, ala_cm, ang_izq, hacia, abombamiento_izq)))
    else:
        cadena.append((d, -m))
    if ala_der:
        cadena += _ala((d, m), +1, ala_cm, ang_der, hacia)
    else:
        cadena.append((d, m))
    return _trazar(cadena, rumbo_grados)


def _v_de_dos_tramos(distancia_cm, rumbo_grados):
    """"V" abierta hacia el robot: dos tramos de 20 cm a 45°, sin cara."""
    k = 20 * math.sin(math.radians(45))
    return _trazar([(distancia_cm - k, -k), (distancia_cm, 0.0), (distancia_cm - k, k)], rumbo_grados)


def _objeto_curvo(distancia_cm, ancho_cm=40.0, abombamiento_cm=5.0, rumbo_grados=0):
    """Arco circular de cuerda `ancho_cm` y flecha `abombamiento_cm` (como el torso de una persona).
    `distancia_cm` es la distancia al punto más cercano (el centro del arco)."""
    mitad = ancho_cm / 2
    radio = (mitad ** 2 + abombamiento_cm ** 2) / (2 * abombamiento_cm)
    cx = distancia_cm + radio  # centro del círculo sobre el eje del rumbo
    golpes = {}
    for a in range(-90, 91):
        fi = math.radians(a - rumbo_grados)
        b = cx * math.cos(fi)
        disc = b ** 2 - (cx ** 2 - radio ** 2)
        if b <= 0 or disc < 0:
            continue
        r = b - math.sqrt(disc)  # intersección más cercana
        if abs(r * math.sin(fi)) <= mitad:
            golpes[a] = r
    return golpes


_RUIDO_CM = (0.5, -0.5, 0.3, -0.4, 0.5, -0.2, 0.0, -0.5)  # patrón fijo, |ruido| <= 0.5 cm


def _con_ruido(capa):
    """Suma a cada distancia un ruido determinista de ±0.5 cm (patrón fijo por orden de ángulo)."""
    return {a: r + _RUIDO_CM[i % len(_RUIDO_CM)] for i, (a, r) in enumerate(sorted(capa.items()))}


# --------------------------------------------------------------------------- CA-4.4.9 a CA-4.4.12 (CC-019, CC-021)
def test_ca_4_4_9_tarima_con_alas_de_frente_a_100_cm_y_20_grados():
    """CA-4.4.9 / EJ-035: tarima con alas, cara de 18 cm, a 100 cm y 20° sobre fondo vacío."""
    from pi.lidar import Tarima, localizar_tarima
    tarima = localizar_tarima(_escaneo(_tarima(100, 20, "FRENTE")))
    assert isinstance(tarima, Tarima)
    assert tarima.distancia_cm == pytest.approx(100, abs=3)
    assert tarima.rumbo_grados == pytest.approx(20, abs=2)
    assert tarima.ancho_cm == pytest.approx(18, abs=2)
    assert tarima.lado == "FRENTE"


def test_ca_4_4_10_tarima_con_alas_de_lado_a_100_cm_y_menos_30_grados():
    """CA-4.4.10 / EJ-035: tarima con alas, cara de 40 cm, a 100 cm y -30°."""
    from pi.lidar import localizar_tarima
    tarima = localizar_tarima(_escaneo(_tarima(100, -30, "LADO")))
    assert tarima is not None
    assert tarima.lado == "LADO"
    assert tarima.distancia_cm == pytest.approx(100, abs=3)
    assert tarima.rumbo_grados == pytest.approx(-30, abs=2)


def _escena_sin_tarima(nombre):
    return {
        "vacio": [],
        "pared": _escaneo(_pared(120)),
        "poste": _escaneo(_poste(100, 20)),
        "recta_18": _escaneo(_cara_plana(100, 18)),
        "recta_40": _escaneo(_cara_plana(100, 40)),
        "una_sola_ala": _escaneo(_tarima(100, 0, "FRENTE", ala_der=False)),
        "una_sola_ala_en_cara_de_40": _escaneo(_tarima(100, 0, "LADO", ala_izq=False)),
        "v_de_dos_tramos": _escaneo(_v_de_dos_tramos(100, 0)),
        "torso_curvo": _escaneo(_objeto_curvo(100)),
    }[nombre]


@pytest.mark.parametrize("escena", ["vacio", "pared", "poste", "recta_18", "recta_40", "una_sola_ala",
                                    "una_sola_ala_en_cara_de_40", "v_de_dos_tramos", "torso_curvo"])
def test_ca_4_4_11_sin_tarima_con_alas_devuelve_none(escena):
    """CA-4.4.11 / EJ-036: vacío, pared, poste de 6 cm, recta sola de 18 o 40 cm, cara con una sola ala,
    "V" de dos tramos y torso curvo de 40 cm con 5 cm de abombamiento."""
    from pi.lidar import localizar_tarima
    assert localizar_tarima(_escena_sin_tarima(escena)) is None


def test_ca_4_4_11_tarima_y_poste_en_la_misma_escena_cada_detector_devuelve_el_suyo():
    """CA-4.4.11 / EJ-036: tarima con alas a 150 cm y -30°, poste a 100 cm y 20° (el poste es el más cercano)."""
    from pi.lidar import localizar_poste, localizar_tarima
    escaneo = _escaneo(_tarima(150, -30, "FRENTE"), _poste(100, 20))
    tarima = localizar_tarima(escaneo)
    assert tarima is not None
    assert tarima.distancia_cm == pytest.approx(150, abs=3)
    assert tarima.rumbo_grados == pytest.approx(-30, abs=2)
    assert tarima.lado == "FRENTE"
    poste = localizar_poste(escaneo)
    assert poste is not None
    assert poste.distancia_cm == pytest.approx(100, abs=3)
    assert poste.rumbo_grados == pytest.approx(20, abs=2)


def test_ca_4_4_12_con_dos_tarimas_devuelve_la_mas_cercana():
    """CA-4.4.12 / EJ-035: tarimas con alas a 150 cm y -30° y a 100 cm y 20°."""
    from pi.lidar import localizar_tarima
    tarima = localizar_tarima(_escaneo(_tarima(150, -30, "FRENTE"), _tarima(100, 20, "FRENTE")))
    assert tarima is not None
    assert tarima.distancia_cm == pytest.approx(100, abs=3)
    assert tarima.rumbo_grados == pytest.approx(20, abs=2)


def _perfil_del_robot():
    """Perfil de tarima con alas (válido en forma) reducido para caber a menos de 15 cm: el propio robot."""
    return _tarima(10, -60, ancho_cm=5.4, ala_cm=6.0)


def test_ca_4_4_12_puntos_a_menos_de_distancia_min_se_ignoran():
    """CA-4.4.12 / EJ-035: un perfil de tarima con alas a 10 cm (el propio robot) no cuenta."""
    from pi.lidar import localizar_tarima
    capa = _perfil_del_robot()
    assert max(capa.values()) < 15
    assert localizar_tarima(_escaneo(capa)) is None


def test_ca_4_4_12_el_robot_no_tapa_a_la_tarima_real():
    """CA-4.4.12 / EJ-035: con la tarima a 100 cm y 20° y el perfil del robot a 10 cm, devuelve la tarima."""
    from pi.lidar import localizar_tarima
    tarima = localizar_tarima(_escaneo(_tarima(100, 20, "FRENTE"), _perfil_del_robot()))
    assert tarima is not None
    assert tarima.distancia_cm == pytest.approx(100, abs=3)
    assert tarima.rumbo_grados == pytest.approx(20, abs=2)


def test_ca_4_4_12_puntos_a_mas_de_alcance_max_se_ignoran():
    """CA-4.4.12 / EJ-035: tarima con alas a 250 cm (más allá de 200 cm) no cuenta."""
    from pi.lidar import localizar_tarima
    capa = _tarima(250, 0, "FRENTE")
    assert min(capa.values()) > 200
    assert localizar_tarima(_escaneo(capa)) is None


def test_ca_4_4_12_la_tarima_lejana_no_tapa_a_la_tarima_real():
    """CA-4.4.12 / EJ-035: tarima real a 150 cm y otra a 250 cm."""
    from pi.lidar import localizar_tarima
    tarima = localizar_tarima(_escaneo(_tarima(150, 0, "FRENTE"), _tarima(250, -60, "FRENTE")))
    assert tarima is not None
    assert tarima.distancia_cm == pytest.approx(150, abs=3)
    assert tarima.rumbo_grados == pytest.approx(0, abs=2)


# --------------------------------------------------------------------------- CA-4.4.13 (CC-020, CC-021)
_ESTRICTOS_NONE = {
    "alas_a_20_grados": dict(ang_izq=20, ang_der=20),
    "alas_a_70_grados": dict(ang_izq=70, ang_der=70),
    "alas_de_8_cm": dict(ala_cm=8),
    "alas_de_35_cm": dict(ala_cm=35),
    "alas_abiertas_alejandose": dict(hacia=False),
    "ala_curva_de_5_cm": dict(abombamiento_izq=5.0),
    "alas_asimetricas_35_y_55": dict(ang_izq=35, ang_der=55),
}


@pytest.mark.parametrize("caso", sorted(_ESTRICTOS_NONE))
def test_ca_4_4_13_alas_fuera_de_tolerancia_no_son_tarima(caso):
    """CA-4.4.13: alas a 20° o 70°, de 8 o 35 cm, que abren alejándose, curva o asimétricas dan None."""
    from pi.lidar import localizar_tarima
    assert localizar_tarima(_escaneo(_tarima(100, 0, "FRENTE", **_ESTRICTOS_NONE[caso]))) is None


def test_ca_4_4_13_alas_de_40_y_50_grados_se_aceptan():
    """CA-4.4.13: alas a 40° y 50° (dentro de 45° ± 10° y con diferencia de 10°) se aceptan."""
    from pi.lidar import Tarima, localizar_tarima
    tarima = localizar_tarima(_escaneo(_tarima(100, 0, "FRENTE", ang_izq=40, ang_der=50)))
    assert isinstance(tarima, Tarima)
    assert tarima.lado == "FRENTE"
    assert tarima.distancia_cm == pytest.approx(100, abs=3)
    assert tarima.rumbo_grados == pytest.approx(0, abs=2)


@pytest.mark.parametrize("lado", ["FRENTE", "LADO"])
def test_ca_4_4_13_tarima_con_alas_y_ruido_de_medio_cm_se_detecta_con_su_lado(lado):
    """CA-4.4.13: tarima con alas a 100 cm con ruido de ±0.5 cm por punto."""
    from pi.lidar import Tarima, localizar_tarima
    tarima = localizar_tarima(_escaneo(_con_ruido(_tarima(100, 0, lado))))
    assert isinstance(tarima, Tarima)
    assert tarima.lado == lado
    assert tarima.distancia_cm == pytest.approx(100, abs=3)
    assert tarima.rumbo_grados == pytest.approx(0, abs=2)


# --------------------------------------------------------------------------- CA-4.4.14 (CC-020)
def test_ca_4_4_14_punto_del_actuador_a_25_cm_y_175_grados_no_es_poste():
    """CA-4.4.14 (CC-020 / SUP-042): dos puntos adyacentes a 25 cm y 174°/176° con la zona_trasera por defecto."""
    from pi.lidar import localizar_poste
    actuador = [(174.0, 25.0), (176.0, 25.0)]
    assert localizar_poste(actuador) is None


@pytest.mark.parametrize("distancia,rumbo", [(25, 0), (100, 20)])
def test_ca_4_4_14_poste_al_frente_o_a_100_cm_se_sigue_encontrando(distancia, rumbo):
    """CA-4.4.14 (CC-020 / SUP-042): poste a 25 cm y 0°, y a 100 cm y 20°, con el actuador a 175° en la escena."""
    from pi.lidar import localizar_poste
    actuador = [(174.0, 25.0), (176.0, 25.0)]
    poste = localizar_poste(_escaneo(_poste(distancia, rumbo)) + actuador)
    assert poste is not None
    assert poste.distancia_cm == pytest.approx(distancia, abs=3)
    assert poste.rumbo_grados == pytest.approx(rumbo, abs=2)


def test_ca_4_4_14_con_zona_trasera_none_el_punto_trasero_si_se_reporta():
    """CA-4.4.14 (CC-020 / SUP-042): sin zona trasera el punto a 25 cm y 175° sí se reporta."""
    from pi.lidar import Poste, localizar_poste
    actuador = [(174.0, 25.0), (176.0, 25.0)]
    poste = localizar_poste(actuador, zona_trasera=None)
    assert isinstance(poste, Poste)
    assert poste.distancia_cm == pytest.approx(25, abs=3)
    assert poste.rumbo_grados == pytest.approx(175, abs=2)
