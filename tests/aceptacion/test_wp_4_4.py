"""WP-4.4 — Localización del destino con LIDAR (CA-4.4.1 a CA-4.4.12, CC-014, CC-019).

Los escaneos son sintéticos (resolución de 1°, 0° al frente y positivo a la izquierda) y se generan
con trigonometría: un poste de 6 cm, una pared recta, y una tarima de 18 cm (de frente) y 40 cm
(de lado). CA-4.4.8 es física (Pi con el RPLIDAR A1) y no tiene prueba aquí.
CA-4.4.7 es de inspección del repositorio.
CA-4.4.9 a CA-4.4.12 (CC-019, EJ-035 y EJ-036) cubren `localizar_tarima` y `Tarima`.
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


# --------------------------------------------------------------------------- CA-4.4.9 a CA-4.4.12 (CC-019)
def _tarima(distancia_cm, rumbo_grados, lado):
    """Tarima vista por el LIDAR: cara plana de 18 cm (FRENTE) o de 40 cm (LADO) a `rumbo_grados`."""
    return _cara_plana(distancia_cm, 18 if lado == "FRENTE" else 40, rumbo_grados)


def test_ca_4_4_9_tarima_de_frente_a_100_cm_y_20_grados():
    """CA-4.4.9 / EJ-035: tarima de 18 cm de frente a 100 cm y 20° sobre fondo vacío."""
    from pi.lidar import Tarima, localizar_tarima
    tarima = localizar_tarima(_escaneo(_tarima(100, 20, "FRENTE")))
    assert isinstance(tarima, Tarima)
    assert tarima.distancia_cm == pytest.approx(100, abs=3)
    assert tarima.rumbo_grados == pytest.approx(20, abs=2)
    assert tarima.lado == "FRENTE"


def test_ca_4_4_10_tarima_de_lado_a_100_cm_y_menos_30_grados():
    """CA-4.4.10 / EJ-035: tarima de 40 cm de lado a 100 cm y -30°."""
    from pi.lidar import localizar_tarima
    tarima = localizar_tarima(_escaneo(_tarima(100, -30, "LADO")))
    assert tarima is not None
    assert tarima.lado == "LADO"
    assert tarima.distancia_cm == pytest.approx(100, abs=3)
    assert tarima.rumbo_grados == pytest.approx(-30, abs=2)


@pytest.mark.parametrize("escena", ["vacio", "pared", "poste"])
def test_ca_4_4_11_sin_tarima_devuelve_none(escena):
    """CA-4.4.11 / EJ-036: escaneo vacío, solo una pared recta o solo un poste de 6 cm."""
    from pi.lidar import localizar_tarima
    escaneo = {"vacio": [], "pared": _escaneo(_pared(120)), "poste": _escaneo(_poste(100, 20))}[escena]
    assert localizar_tarima(escaneo) is None


def test_ca_4_4_11_tarima_y_poste_en_la_misma_escena_cada_detector_devuelve_el_suyo():
    """CA-4.4.11 / EJ-036: tarima a 150 cm y -30°, poste a 100 cm y 20° (el poste es el más cercano)."""
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
    """CA-4.4.12 / EJ-035: tarimas a 150 cm y -30° y a 100 cm y 20°."""
    from pi.lidar import localizar_tarima
    tarima = localizar_tarima(_escaneo(_tarima(150, -30, "FRENTE"), _tarima(100, 20, "FRENTE")))
    assert tarima is not None
    assert tarima.distancia_cm == pytest.approx(100, abs=3)
    assert tarima.rumbo_grados == pytest.approx(20, abs=2)


def test_ca_4_4_12_puntos_a_menos_de_distancia_min_se_ignoran():
    """CA-4.4.12 / EJ-035: grupo del tamaño de una tarima a 10 cm (el propio robot) no cuenta."""
    from pi.lidar import localizar_tarima
    cuerpo = [(float(a), round(r, 2)) for a, r in sorted(_cara_plana(10, 18).items())]
    assert localizar_tarima(cuerpo) is None


def test_ca_4_4_12_el_robot_no_tapa_a_la_tarima_real():
    """CA-4.4.12 / EJ-035: con la tarima a 100 cm y puntos del robot a 10 cm, devuelve la tarima."""
    from pi.lidar import localizar_tarima
    cuerpo = [(float(a), round(r, 2)) for a, r in sorted(_cara_plana(10, 18, -60).items())]
    tarima = localizar_tarima(_escaneo(_tarima(100, 20, "FRENTE")) + cuerpo)
    assert tarima is not None
    assert tarima.distancia_cm == pytest.approx(100, abs=3)
    assert tarima.rumbo_grados == pytest.approx(20, abs=2)


def test_ca_4_4_12_puntos_a_mas_de_alcance_max_se_ignoran():
    """CA-4.4.12 / EJ-035: grupo del tamaño de una tarima a 250 cm (más allá de 200 cm) no cuenta."""
    from pi.lidar import localizar_tarima
    assert localizar_tarima(_escaneo(_tarima(250, 0, "FRENTE"))) is None


def test_ca_4_4_12_la_tarima_lejana_no_tapa_a_la_tarima_real():
    """CA-4.4.12 / EJ-035: tarima real a 150 cm y otra a 250 cm."""
    from pi.lidar import localizar_tarima
    tarima = localizar_tarima(_escaneo(_tarima(150, 0, "FRENTE"), _tarima(250, -60, "FRENTE")))
    assert tarima is not None
    assert tarima.distancia_cm == pytest.approx(150, abs=3)
