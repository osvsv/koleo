"""WP-3.2 — Enlace de comandos Pi–ESP32 por MQTT (CA-3.2.1 a CA-3.2.3)."""
import pytest

from _ayudas import como_dict, errores

TEMA_CMD = "koleo/robot1/esp32/cmd"


class ClienteFalso:
    """Implementa publicar(topic, payload) y esperar_respuesta(id_cmd, timeout_s)."""

    def __init__(self, respuesta=None, sin_respuesta=False):
        self.respuesta = respuesta if respuesta is not None else {"resultado": "ACK", "codigo": "OK"}
        self.sin_respuesta = sin_respuesta
        self.publicados = []
        self.esperas = []

    def publicar(self, topic, payload):
        self.publicados.append((topic, como_dict(payload)))

    def esperar_respuesta(self, id_cmd, timeout_s):
        self.esperas.append((id_cmd, timeout_s))
        if self.sin_respuesta:
            raise TimeoutError("sin respuesta")
        return self.respuesta


def _enlace(cliente):
    from pi.enlace import EnlaceESP32
    return EnlaceESP32(cliente)


def test_ca_3_2_1_lift_ack_devuelve_la_respuesta():
    """CA-3.2.1"""
    resp = {"resultado": "ACK", "codigo": "LIFT_OK"}
    cliente = ClienteFalso(resp)
    assert _enlace(cliente).lift("TAR-101") == resp
    assert cliente.publicados and cliente.publicados[0][0] == TEMA_CMD
    assert cliente.publicados[0][1]["cmd"] == "LIFT"


def test_ca_3_2_1_lift_overweight_devuelve_error_sin_lanzar():
    """CA-3.2.1"""
    resp = {"resultado": "ERR", "codigo": "OVERWEIGHT"}
    assert _enlace(ClienteFalso(resp)).lift("TAR-101") == resp


def test_ca_3_2_2_timeout_lanza_y_envia_stop():
    """CA-3.2.2"""
    cliente = ClienteFalso(sin_respuesta=True)
    enlace = _enlace(cliente)
    with pytest.raises(TimeoutError):
        enlace.enviar({"cmd": "LIFT", "id_cmd": "CMD-T1", "id_tarima": "TAR-101"})
    comandos = [p.get("cmd") for _, p in cliente.publicados]
    assert comandos[0] == "LIFT"
    assert "STOP" in comandos[1:], "tras el timeout el enlace debe intentar enviar STOP"
    assert cliente.esperas[0][1] == 1.0, "tiempo de espera por defecto de 1 s"


def test_ca_3_2_3_drop_publica_mensaje_valido():
    """CA-3.2.3"""
    cliente = ClienteFalso()
    _enlace(cliente).drop("TAR-101", 150, 120)
    assert len(cliente.publicados) == 1
    topic, msg = cliente.publicados[0]
    assert topic == TEMA_CMD
    assert not errores("esp32_cmd", msg), errores("esp32_cmd", msg)
    assert msg["cmd"] == "DROP"
    assert msg["x_cm"] == 150 and msg["y_cm"] == 120


def test_ca_3_2_3_move_publica_pwm_y_valida():
    """CA-3.2.3"""
    cliente = ClienteFalso()
    _enlace(cliente).move(80, -80)
    topic, msg = cliente.publicados[0]
    assert topic == TEMA_CMD
    assert not errores("esp32_cmd", msg), errores("esp32_cmd", msg)
    assert msg["cmd"] == "MOVE"
    assert msg["pwm_izq"] == 80 and msg["pwm_der"] == -80


def test_ca_3_2_3_id_cmd_unico():
    """CA-3.2.3: cada comando lleva un id_cmd único."""
    cliente = ClienteFalso()
    enlace = _enlace(cliente)
    enlace.drop("TAR-101", 150, 120)
    enlace.drop("TAR-101", 150, 120)
    enlace.move(80, -80)
    enlace.stop()
    ids = [m["id_cmd"] for _, m in cliente.publicados]
    assert len(ids) == 4 and len(set(ids)) == 4
