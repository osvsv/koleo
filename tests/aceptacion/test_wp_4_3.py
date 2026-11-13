"""WP-4.3 — Planificador A* y misión (CA-4.3.1 a CA-4.3.6).

Inicio y meta de cada ruta se toman del mapa de referencia del DG §8 (fila, columna).
Las respuestas del enlace falso usan el formato de WP-3.2: {"resultado", "codigo"}.
"""
import inspect

import pytest

RUTAS = {
    "RUTA_1": ((0, 0), (4, 5), 10),
    "RUTA_2": ((0, 2), (3, 4), 6),
    "RUTA_3": ((4, 2), (0, 5), 8),
}
ACK = {"resultado": "ACK", "codigo": "OK"}
MAX_LLAMADAS = 2000


def _planificador():
    from pi.mapa import MAPA
    from pi.planificador import PlanificadorAStar
    return MAPA, PlanificadorAStar(MAPA)


@pytest.mark.parametrize("ruta", list(RUTAS))
def test_ca_4_3_1_rutas_de_referencia(ruta):
    """CA-4.3.1"""
    mapa, plan = _planificador()
    inicio, meta, largo = RUTAS[ruta]
    camino = plan.planificar(inicio, meta)
    assert camino is not None
    camino = [tuple(c) for c in camino]
    assert len(camino) == largo
    assert camino[0] == inicio and camino[-1] == meta
    assert all(mapa[f][c] == 0 for f, c in camino)
    for (f1, c1), (f2, c2) in zip(camino, camino[1:]):
        assert abs(f1 - f2) + abs(c1 - c2) == 1


def test_ca_4_3_2_meta_en_obstaculo_devuelve_none():
    """CA-4.3.2"""
    _, plan = _planificador()
    assert plan.planificar((0, 0), (0, 3)) is None


def test_ca_4_3_2_inicio_igual_a_meta_devuelve_solo_esa_celda():
    """CA-4.3.2"""
    _, plan = _planificador()
    assert [tuple(c) for c in plan.planificar((2, 2), (2, 2))] == [(2, 2)]


def test_ca_4_3_3_celda_a_cm():
    """CA-4.3.3"""
    from pi.mision import celda_a_cm
    assert tuple(celda_a_cm(4, 5)) == (150, 120)


class EnlaceFalso:
    def __init__(self, lift=ACK, falla_en=None):
        self.llamadas = []
        self._lift = lift
        self._falla_en = falla_en

    def _reg(self, nombre, *args):
        self.llamadas.append((nombre, args))
        assert len(self.llamadas) < MAX_LLAMADAS, "la misión no termina con el enlace falso"
        if nombre == self._falla_en:
            raise TimeoutError("sin respuesta")

    def lift(self, id_tarima, peso_kg):
        self._reg("lift", id_tarima, peso_kg)
        return self._lift

    def move(self, izq, der):
        self._reg("move", izq, der)
        return ACK

    def stop(self):
        self.llamadas.append(("stop", ()))
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


def _ejecutar(enlace):
    from pi import odometria
    from pi.mision import ejecutar_mision
    return ejecutar_mision("RUTA_1", "TAR-101", 8.45, enlace, odometria)


def _nombres(enlace):
    return [n for n, _ in enlace.llamadas]


def test_ca_4_3_4_secuencia_lift_move_drop():
    """CA-4.3.4"""
    enlace = EnlaceFalso()
    resultado = _ejecutar(enlace)
    assert resultado["estado"] == "completada"
    nombres = _nombres(enlace)
    assert nombres[0] == "lift"
    assert enlace.llamadas[0][1] == ("TAR-101", 8.45)
    assert "move" in nombres
    assert "drop" in nombres
    assert nombres.index("lift") < nombres.index("move") < nombres.index("drop")
    drop = [a for n, a in enlace.llamadas if n == "drop"][-1]
    assert (drop[0], drop[1], drop[2]) == ("TAR-101", 150, 120)


@pytest.mark.parametrize("codigo", ["OVERWEIGHT", "PESO_INVALIDO"])
def test_ca_4_3_5_lift_rechazado_no_mueve_ni_deposita(codigo):
    """CA-4.3.5"""
    enlace = EnlaceFalso(lift={"resultado": "ERR", "codigo": codigo})
    resultado = _ejecutar(enlace)
    nombres = _nombres(enlace)
    assert "move" not in nombres and "drop" not in nombres
    assert resultado["estado"] == "rechazada"


@pytest.mark.parametrize("falla_en", ["lift", "move"])
def test_ca_4_3_6_timeout_aborta_con_stop(falla_en):
    """CA-4.3.6"""
    enlace = EnlaceFalso(falla_en=falla_en)
    resultado = _ejecutar(enlace)  # no debe propagar la excepción
    nombres = _nombres(enlace)
    assert "stop" in nombres
    assert "drop" not in nombres
    assert resultado["estado"] == "error"
