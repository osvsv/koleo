"""WP-4.1 — Puente MQTT (CA-4.1.1 a CA-4.1.3).

Los payloads de `esp32/*` son los de CA-1.1.8 (se validan contra el esquema). Las claves de
`contexto` (campos de telemetría y evento que no vienen del ESP32) no están definidas: es una
suposición de esta prueba.
"""
import pytest

from _ayudas import PREFIJO, TS, def_de_tema, errores

CONTEXTO = {"robot_id": "robot1", "id_tarima": "TAR-101", "x_cm": 60.0, "y_cm": 30.0,
            "velocidad_cm_s": 10.0, "estado": "EN_RUTA", "peso_kg": 8.45,
            "distancia_obstaculo_cm": 40.0}

ESTADOS_ROBOT = ["INACTIVO", "EN_MISION", "ELEVANDO", "EN_RUTA", "DEPOSITANDO",
                 "DETENIDO_OBSTACULO", "ERROR"]


def _consolidar(topic, payload, ts_ms):
    from pi.puente_mqtt import consolidar_esp32
    return consolidar_esp32(PREFIJO + topic, payload, dict(CONTEXTO), ts_ms)


def _validos(salida):
    assert salida, "debe producir al menos un mensaje"
    for tema, payload in salida:
        assert not errores(def_de_tema(tema), payload), (tema, payload)


def _eventos(salida):
    return [p for t, p in salida if t == PREFIJO + "evento"]


def test_ca_4_1_1_obstaculo_sobrepeso_y_lift_ok_son_eventos_validos():
    """CA-4.1.1"""
    entradas = [
        ("esp32/evento", {"ts": TS, "codigo": "OBSTACULO_CERCANO"}, TS + 1, "OBSTACULO"),
        ("esp32/evento", {"ts": TS + 5, "codigo": "OVERWEIGHT", "id_tarima": "TAR-101",
                          "peso_kg": 11.8}, TS + 6, "SOBREPESO"),
        ("esp32/resp", {"ts": TS + 9, "id_cmd": "CMD-9", "resultado": "ACK", "codigo": "LIFT_OK"}, TS + 10, "LIFT_OK"),
    ]
    ids = []
    for topic, payload, ts_ms, tipo in entradas:
        assert not errores(def_de_tema(PREFIJO + topic), payload), "entrada fuera de contrato"
        salida = _consolidar(topic, payload, ts_ms)
        _validos(salida)
        evs = _eventos(salida)
        assert [e["tipo"] for e in evs] == [tipo]
        ids.append(evs[0]["id_evento"])
    assert len(set(ids)) == 3, "id_evento único por evento"


def test_ca_4_1_1_sensores_produce_telemetria_valida():
    """CA-4.1.1"""
    payload = {"ts": TS, "distancia_obstaculo_cm": 40.0, "peso_kg": 8.45,
               "enc_izq": 100, "enc_der": 100}
    assert not errores("esp32_sensores", payload)
    salida = _consolidar("esp32/sensores", payload, TS + 2)
    _validos(salida)
    assert any(t == PREFIJO + "telemetria" for t, _ in salida)


def _orden(tipo="INICIAR", id_orden="ORD-1"):
    msg = {"ts": TS, "id_orden": id_orden, "tipo": tipo}
    if tipo == "INICIAR":
        msg.update({"ruta": "RUTA_1", "id_tarima": "TAR-101"})
    return msg


def _procesar(payload, estado, vistas):
    from pi.ordenes import procesar_orden
    return procesar_orden(payload, estado, vistas)


def test_ca_4_1_2_iniciar_con_robot_inactivo_se_acepta():
    """CA-4.1.2"""
    ack = _procesar(_orden(), "INACTIVO", set())
    assert not errores("orden_ack", ack)
    assert ack["id_orden"] == "ORD-1"
    assert ack["resultado"] == "aceptada"


def test_ca_4_1_2_id_orden_repetido_produce_el_mismo_ack():
    """CA-4.1.2: la repetición no se reevalúa (mismo ack)."""
    vistas = set()
    primero = _procesar(_orden(), "INACTIVO", vistas)
    segundo = _procesar(_orden(), "INACTIVO", vistas)
    assert primero == segundo
    assert segundo["resultado"] == "aceptada"


def test_ca_4_1_3_iniciar_en_mision_se_rechaza():
    """CA-4.1.3"""
    ack = _procesar(_orden(id_orden="ORD-2"), "EN_MISION", set())
    assert not errores("orden_ack", ack)
    assert ack["id_orden"] == "ORD-2"
    assert ack["resultado"] == "rechazada"


@pytest.mark.parametrize("estado", ESTADOS_ROBOT)
def test_ca_4_1_3_paro_se_acepta_en_cualquier_estado(estado):
    """CA-4.1.3"""
    ack = _procesar(_orden("PARO", id_orden="ORD-P"), estado, set())
    assert not errores("orden_ack", ack)
    assert ack["resultado"] == "aceptada"
