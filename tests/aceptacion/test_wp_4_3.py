"""WP-4.3 — Navegación guiada por LIDAR y misión (CA-4.3.1 a CA-4.3.8, CC-014).

Ejercita solo la interfaz de la WBS: `pi.navegacion.siguiente_accion`, `pi.navegacion.destino_cm`
y `pi.mision.ejecutar_mision(id_tarima, peso_kg, enlace, lidar, max_pasos)`.

El enlace y el lidar son falsos y comparten un "mundo" mínimo: cada MOVE de giro cambia el rumbo
del poste en 10° y cada MOVE de avance acerca el poste 15 cm. Los escaneos del lidar falso son
sintéticos (poste de 6 cm, resolución de 1°) y se generan con trigonometría.
Las respuestas del enlace usan el formato de WP-3.2: {"resultado", "codigo"}.
"""
import inspect
import math

import pytest

ACK = {"resultado": "ACK", "codigo": "OK"}
LIFT_OK = {"resultado": "ACK", "codigo": "LIFT_OK"}
MAX_LLAMADAS = 2000
PASO_GIRO_GRADOS = 10
PASO_AVANCE_CM = 15


# --------------------------------------------------------------------------- escaneos sintéticos
def _escaneo_poste(distancia_cm, rumbo_grados, diametro_cm=6.0):
    """Puntos (ángulo entero, distancia) de un poste cilíndrico. `distancia_cm` es la distancia
    a la mitad de la profundidad visible (centro a +1.5 cm), de modo que tanto la distancia a la
    superficie como al centro quedan dentro de ±1.5 cm del valor nominal."""
    radio = diametro_cm / 2
    centro = distancia_cm + radio / 2
    puntos = []
    for a in range(-180, 180):
        fi = math.radians(a - rumbo_grados)
        perp = centro * math.sin(fi)
        if math.cos(fi) > 0 and abs(perp) <= radio:
            r = centro * math.cos(fi) - math.sqrt(radio ** 2 - perp ** 2)
            puntos.append((float(a), round(r, 2)))
    return puntos


def _escaneo_pared(distancia_cm=120.0, semiangulo=40):
    return [(float(a), round(distancia_cm / math.cos(math.radians(a)), 2))
            for a in range(-semiangulo, semiangulo + 1)]


# --------------------------------------------------------------------------- dobles
class Mundo:
    def __init__(self, distancia_cm, rumbo_grados):
        self.distancia_cm = distancia_cm
        self.rumbo_grados = rumbo_grados
        self.eventos = []  # ("escanear",) o (nombre_comando, args...)

    def mover(self, izq, der):
        if izq < 0 < der:  # giro a la izquierda: el poste se desplaza hacia el frente
            self.rumbo_grados -= PASO_GIRO_GRADOS
        elif der < 0 < izq:  # giro a la derecha
            self.rumbo_grados += PASO_GIRO_GRADOS
        elif izq > 0 and der > 0:  # avance
            self.distancia_cm = max(self.distancia_cm - PASO_AVANCE_CM, 1.0)

    def nombres(self):
        return [e[0] for e in self.eventos]

    def llamadas(self, nombre):
        return [e[1:] for e in self.eventos if e[0] == nombre]


class EnlaceFalso:
    def __init__(self, mundo, lift=LIFT_OK, falla_en=None):
        self.mundo = mundo
        self._lift = lift
        self._falla_en = falla_en

    def _reg(self, nombre, *args):
        self.mundo.eventos.append((nombre,) + args)
        assert len(self.mundo.eventos) < MAX_LLAMADAS, "la misión no termina con el enlace falso"
        if nombre == self._falla_en:
            raise TimeoutError("sin respuesta")

    def lift(self, id_tarima, peso_kg):
        self._reg("lift", id_tarima, peso_kg)
        return self._lift

    def move(self, izq, der):
        self._reg("move", izq, der)
        self.mundo.mover(izq, der)
        return ACK

    def stop(self):
        self.mundo.eventos.append(("stop",))
        return ACK

    def drop(self, id_tarima, x_cm, y_cm):
        self._reg("drop", id_tarima, x_cm, y_cm)
        return ACK

    def enviar(self, cmd):
        c = cmd["cmd"].lower()
        if c == "lift":
            return self.lift(cmd.get("id_tarima"), cmd.get("peso_kg"))
        if c == "move":
            return self.move(cmd.get("pwm_izq"), cmd.get("pwm_der"))
        if c == "drop":
            return self.drop(cmd.get("id_tarima"), cmd.get("x_cm"), cmd.get("y_cm"))
        return self.stop()


class LidarFalso:
    """`escanear()` devuelve pares (ángulo, distancia cm). `guion(n, mundo)` (n desde 1) opcional."""

    def __init__(self, mundo, guion=None, lanza=None):
        self.mundo = mundo
        self.guion = guion
        self.lanza = lanza
        self.escaneos = 0

    def escanear(self, *args, **kwargs):
        self.escaneos += 1
        assert self.escaneos < MAX_LLAMADAS, "la misión no termina con el lidar falso"
        self.mundo.eventos.append(("escanear",))
        if self.lanza is not None:
            raise self.lanza
        if self.guion is not None:
            return self.guion(self.escaneos, self.mundo)
        return _escaneo_poste(self.mundo.distancia_cm, self.mundo.rumbo_grados)


def _armar(distancia_cm=120.0, rumbo_grados=20.0, lift=LIFT_OK, falla_en=None, guion=None, lanza=None):
    mundo = Mundo(distancia_cm, rumbo_grados)
    return mundo, EnlaceFalso(mundo, lift=lift, falla_en=falla_en), LidarFalso(mundo, guion, lanza)


def _ejecutar(enlace, lidar, **kw):
    from pi.mision import ejecutar_mision
    return ejecutar_mision("TAR-101", 8.45, enlace, lidar, **kw)


def _const(nombre):
    import pi.mision
    import pi.navegacion
    for mod in (pi.navegacion, pi.mision):
        if hasattr(mod, nombre):
            return getattr(mod, nombre)
    raise AssertionError(f"la constante {nombre} no existe en pi.navegacion ni en pi.mision")


# --------------------------------------------------------------------------- CA-4.3.1 / CA-4.3.2
def test_interfaz_constantes():
    """Constantes de la interfaz de WP-4.3 (valores exactos de la WBS)."""
    esperadas = {
        "DISTANCIA_DEPOSITO_CM": 30, "DISTANCIA_MAX_CM": 35, "DISTANCIA_MIN_CM": 20,
        "TOLERANCIA_RUMBO_GRADOS": 5, "PWM_GIRO": 70, "PWM_AVANCE": 80, "MAX_PASOS": 200,
    }
    for nombre, valor in esperadas.items():
        assert _const(nombre) == valor, nombre
    from pi.mision import ejecutar_mision
    assert inspect.signature(ejecutar_mision).parameters["max_pasos"].default == 200


@pytest.mark.parametrize("distancia,rumbo,esperada", [
    (150, 30, "GIRAR_IZQ"),
    (150, -30, "GIRAR_DER"),
    (150, 2, "AVANZAR"),
    (30, 0, "LLEGO"),
])
def test_ca_4_3_1_siguiente_accion(distancia, rumbo, esperada):
    """CA-4.3.1"""
    from pi.lidar import Poste
    from pi.navegacion import siguiente_accion
    assert siguiente_accion(Poste(distancia_cm=distancia, rumbo_grados=rumbo)) == esperada


def test_ca_4_3_1_poste_none_es_perdido():
    """CA-4.3.1"""
    from pi.navegacion import siguiente_accion
    assert siguiente_accion(None) == "PERDIDO"


@pytest.mark.parametrize("distancia,esperada", [
    (35, "LLEGO"),
    (20, "LLEGO"),
    (36, "AVANZAR"),
    (19, "DEMASIADO_CERCA"),
])
def test_ca_4_3_2_limites_inclusivos_de_20_a_35_cm(distancia, esperada):
    """CA-4.3.2 (caso límite)"""
    from pi.lidar import Poste
    from pi.navegacion import siguiente_accion
    assert siguiente_accion(Poste(distancia_cm=distancia, rumbo_grados=0)) == esperada


# --------------------------------------------------------------------------- CA-4.3.3
@pytest.mark.parametrize("distancia,rumbo,esperado", [
    (150, 0, (150, 0)),
    (100, 90, (0, 100)),
])
def test_ca_4_3_3_destino_cm(distancia, rumbo, esperado):
    """CA-4.3.3"""
    from pi.lidar import Poste
    from pi.navegacion import destino_cm
    x, y = destino_cm(Poste(distancia_cm=distancia, rumbo_grados=rumbo))
    assert x == pytest.approx(esperado[0], abs=0.5)
    assert y == pytest.approx(esperado[1], abs=0.5)


# --------------------------------------------------------------------------- CA-4.3.4
def test_ca_4_3_4_mision_completa_con_lidar_y_enlace_falsos():
    """CA-4.3.4: poste a 120 cm y 20° que se aproxima hasta 30 cm."""
    mundo, enlace, lidar = _armar(120.0, 20.0)
    resultado = _ejecutar(enlace, lidar)
    assert resultado["estado"] == "completada"

    nombres = mundo.nombres()
    assert "escanear" in nombres and "lift" in nombres
    assert nombres.index("escanear") < nombres.index("lift"), "debe escanear antes de LIFT"
    assert mundo.llamadas("lift")[0] == ("TAR-101", 8.45)

    pwm_giro, pwm_avance = _const("PWM_GIRO"), _const("PWM_AVANCE")
    moves = mundo.llamadas("move")
    assert (-pwm_giro, pwm_giro) in moves, "falta el giro a la izquierda"
    assert (pwm_avance, pwm_avance) in moves, "falta el avance"
    assert (pwm_giro, -pwm_giro) not in moves, "no debe girar a la derecha"
    idx_move = [i for i, e in enumerate(mundo.eventos) if e[0] == "move"]
    idx_giro = [i for i in idx_move if mundo.eventos[i][1:] == (-pwm_giro, pwm_giro)]
    idx_avance = [i for i in idx_move if mundo.eventos[i][1:] == (pwm_avance, pwm_avance)]
    assert min(idx_giro) < min(idx_avance), "primero gira y luego avanza"
    assert nombres.index("lift") < min(idx_move)

    assert "stop" in nombres and "drop" in nombres
    assert max(idx_move) < nombres.index("stop") < nombres.index("drop")
    assert nombres.count("drop") == 1

    drop = mundo.llamadas("drop")[0]
    esperado_x = 120 * math.cos(math.radians(20))
    esperado_y = 120 * math.sin(math.radians(20))
    assert drop[0] == "TAR-101"
    # Coordenadas de destino_cm del primer escaneo (el localizador admite ±3 cm y ±2°).
    assert drop[1] == pytest.approx(esperado_x, abs=6)
    assert drop[2] == pytest.approx(esperado_y, abs=6)


# --------------------------------------------------------------------------- CA-4.3.5
@pytest.mark.parametrize("codigo", ["OVERWEIGHT", "PESO_INVALIDO"])
def test_ca_4_3_5_lift_rechazado_no_mueve_ni_deposita(codigo):
    """CA-4.3.5"""
    mundo, enlace, lidar = _armar(lift={"resultado": "ERR", "codigo": codigo})
    resultado = _ejecutar(enlace, lidar)
    assert "move" not in mundo.nombres() and "drop" not in mundo.nombres()
    assert resultado["estado"] == "rechazada"


# --------------------------------------------------------------------------- CA-4.3.6
@pytest.mark.parametrize("falla_en", ["lift", "move"])
def test_ca_4_3_6_timeout_aborta_con_stop(falla_en):
    """CA-4.3.6"""
    mundo, enlace, lidar = _armar(falla_en=falla_en)
    resultado = _ejecutar(enlace, lidar)  # no debe propagar la excepción
    assert "stop" in mundo.nombres()
    assert "drop" not in mundo.nombres()
    assert resultado["estado"] == "error"
    assert resultado["codigo"] == "ENLACE"


# --------------------------------------------------------------------------- CA-4.3.7
def _sin_poste(n, mundo):
    return _escaneo_pared(120.0)


@pytest.mark.parametrize("variante", ["pared", "vacio", "lidar_sin_datos"])
def test_ca_4_3_7_sin_poste_no_inicia_ni_usa_destino_por_defecto(variante):
    """CA-4.3.7 (caso límite, antes EJ-014)"""
    if variante == "lidar_sin_datos":
        from pi.rplidar import LidarSinDatos
        mundo, enlace, lidar = _armar(lanza=LidarSinDatos("sin vuelta"))
    elif variante == "vacio":
        mundo, enlace, lidar = _armar(guion=lambda n, m: [])
    else:
        mundo, enlace, lidar = _armar(guion=_sin_poste)
    resultado = _ejecutar(enlace, lidar)
    nombres = mundo.nombres()
    for prohibido in ("lift", "move", "drop"):
        assert prohibido not in nombres
    assert resultado["estado"] == "error"
    assert resultado["codigo"] == "DESTINO_NO_ENCONTRADO"


# --------------------------------------------------------------------------- CA-4.3.8
def test_ca_4_3_8_poste_perdido_tres_escaneos_consecutivos():
    """CA-4.3.8: el poste desaparece durante el avance."""
    def guion(n, mundo):
        return _escaneo_poste(120.0, 0.0) if n <= 2 else _escaneo_pared(120.0)

    mundo, enlace, lidar = _armar(120.0, 0.0, guion=guion)
    resultado = _ejecutar(enlace, lidar)
    assert resultado["estado"] == "error"
    assert resultado["codigo"] == "POSTE_PERDIDO"
    assert "stop" in mundo.nombres()
    assert "drop" not in mundo.nombres()


def test_ca_4_3_8_demasiado_cerca_durante_el_avance():
    """CA-4.3.8: el poste aparece a menos de DISTANCIA_MIN_CM tras comenzar el avance."""
    def guion(n, mundo):
        return _escaneo_poste(120.0, 0.0) if n <= 2 else _escaneo_poste(18.0, 0.0)

    mundo, enlace, lidar = _armar(120.0, 0.0, guion=guion)
    resultado = _ejecutar(enlace, lidar)
    assert resultado["estado"] == "error"
    assert resultado["codigo"] == "DEMASIADO_CERCA"
    assert "stop" in mundo.nombres()
    assert "drop" not in mundo.nombres()


def test_ca_4_3_8_tiempo_agotado_al_llegar_a_max_pasos():
    """CA-4.3.8: el poste nunca se acerca; la misión se corta en max_pasos."""
    mundo, enlace, lidar = _armar(120.0, 0.0, guion=lambda n, m: _escaneo_poste(120.0, 0.0))
    resultado = _ejecutar(enlace, lidar, max_pasos=5)
    assert resultado["estado"] == "error"
    assert resultado["codigo"] == "TIEMPO_AGOTADO"
    assert "stop" in mundo.nombres()
    assert "drop" not in mundo.nombres()
