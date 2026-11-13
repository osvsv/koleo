"""WP-5.2 — Tablero: control y gestión logística, parte API (CA-5.2.1 a CA-5.2.4)."""
import pytest

from _ayudas import TS, aplanar, como_dict, crear_bd, errores


class PublicadorFalso:
    """Función publicador(topic, payload) que registra lo publicado."""

    def __init__(self):
        self.publicados = []

    def __call__(self, topic, payload):
        self.publicados.append((topic, como_dict(payload)))


@pytest.fixture
def entorno(tmp_path):
    ruta = tmp_path / "koleo.db"
    crear_bd(ruta).close()
    pub = PublicadorFalso()
    from backend.koleo.api import crear_app
    app = crear_app(str(ruta), publicador=pub)
    return app.test_client(), pub, str(ruta)


INICIAR = {"tipo": "INICIAR", "ruta": "RUTA_1", "id_tarima": "TAR-101"}


def test_ca_5_2_1_iniciar_valido_responde_202_publica_y_queda_pendiente(entorno):
    """CA-5.2.1"""
    client, pub, _ = entorno
    resp = client.post("/api/ordenes", json=INICIAR)
    assert resp.status_code == 202
    id_orden = resp.get_json()["id_orden"]
    assert len(pub.publicados) == 1
    topic, msg = pub.publicados[0]
    assert topic == "koleo/robot1/orden"
    assert not errores("orden", msg), errores("orden", msg)
    assert msg["tipo"] == "INICIAR" and msg["id_orden"] == id_orden
    estado = client.get(f"/api/ordenes/{id_orden}")
    assert estado.status_code == 200
    assert "pendiente" in list(aplanar(estado.get_json()))


@pytest.mark.parametrize("faltante", ["id_tarima", "ruta"])
def test_ca_5_2_2_iniciar_incompleto_responde_400_sin_publicar(entorno, faltante):
    """CA-5.2.2"""
    client, pub, _ = entorno
    cuerpo = {k: v for k, v in INICIAR.items() if k != faltante}
    assert client.post("/api/ordenes", json=cuerpo).status_code == 400
    assert pub.publicados == []


@pytest.mark.parametrize("resultado", ["aceptada", "rechazada"])
def test_ca_5_2_3_ack_actualiza_el_estado_de_la_orden(entorno, resultado):
    """CA-5.2.3: el ack llega por la ingesta del backend (tema orden/ack)."""
    import sqlite3
    from backend.koleo.ingesta import procesar_mensaje
    client, _, db = entorno
    id_orden = client.post("/api/ordenes", json=INICIAR).get_json()["id_orden"]
    conn = sqlite3.connect(db)
    try:
        procesar_mensaje(conn, "koleo/robot1/orden/ack",
                         {"ts": TS, "id_orden": id_orden, "resultado": resultado}, TS + 15)
        conn.commit()
    finally:
        conn.close()
    estado = client.get(f"/api/ordenes/{id_orden}").get_json()
    valores = list(aplanar(estado))
    assert resultado in valores
    assert "pendiente" not in valores


def test_ca_5_2_4_registrar_tarima_queda_en_piso(entorno):
    """CA-5.2.4"""
    client, _, _ = entorno
    resp = client.post("/api/tarimas",
                       json={"id_tarima": "TAR-104", "peso_kg": 5.0, "descripcion": "Lote de prueba"})
    assert 200 <= resp.status_code < 300
    tarimas = client.get("/api/tarimas").get_json()
    t = [x for x in tarimas if "TAR-104" in list(aplanar(x))]
    assert len(t) == 1
    assert "EN_PISO" in list(aplanar(t[0]))


@pytest.mark.parametrize("cuerpo", [
    {"id_tarima": "TAR-104", "peso_kg": 0, "descripcion": "peso cero"},
    {"id_tarima": "ABC", "peso_kg": 5.0, "descripcion": "id inválido"},
])
def test_ca_5_2_4_registro_invalido_responde_400(entorno, cuerpo):
    """CA-5.2.4"""
    client, _, _ = entorno
    assert client.post("/api/tarimas", json=cuerpo).status_code == 400
    assert client.get("/api/tarimas").get_json() == []


# --- CA-5.2.6 (CC-008): publicador MQTT, parte verificable sin broker ---------
# La captura con Mosquitto real (orden_mosquitto.txt) es evidencia física.

class ClienteFalso:
    """Imita paho-mqtt: publish(topic, payload=None, qos=0, retain=False)."""

    def __init__(self):
        self.llamadas = []

    def publish(self, topic, payload=None, qos=0, retain=False):
        self.llamadas.append({"topic": topic, "payload": payload, "qos": qos})


def _env_mqtt():
    return {"KOLEO_MQTT_HOST": "broker.invalido", "KOLEO_MQTT_PORT": "1883"}


def test_ca_5_2_6_sin_host_crear_publicador_devuelve_none():
    """CA-5.2.6"""
    from backend.koleo.api import crear_publicador
    assert crear_publicador({}) is None


def test_ca_5_2_6_publicador_publica_json_con_qos_1():
    """CA-5.2.6"""
    import json
    from backend.koleo.api import crear_publicador
    cliente = ClienteFalso()
    pub = crear_publicador(_env_mqtt(), cliente=cliente)
    assert callable(pub)
    mensaje = {"tipo": "INICIAR", "ruta": "RUTA_1", "id_tarima": "TAR-101", "id_orden": "ORD-1"}
    pub("koleo/robot1/orden", mensaje)
    assert len(cliente.llamadas) == 1
    ll = cliente.llamadas[0]
    assert ll["topic"] == "koleo/robot1/orden"
    assert isinstance(ll["payload"], str)
    assert json.loads(ll["payload"]) == mensaje
    assert ll["qos"] == 1


def test_ca_5_2_6_post_ordenes_con_publicador_real_publica_en_el_tema(tmp_path):
    """CA-5.2.6"""
    from backend.koleo.api import crear_app, crear_publicador
    ruta = tmp_path / "koleo.db"
    crear_bd(ruta).close()
    cliente = ClienteFalso()
    app = crear_app(str(ruta), publicador=crear_publicador(_env_mqtt(), cliente=cliente))
    resp = app.test_client().post("/api/ordenes", json=INICIAR)
    assert resp.status_code == 202
    assert [ll["topic"] for ll in cliente.llamadas] == ["koleo/robot1/orden"]
    assert como_dict(cliente.llamadas[0]["payload"])["tipo"] == "INICIAR"


def test_ca_5_2_6_sin_publicador_ordenes_503_y_resto_de_la_api_sigue(tmp_path):
    """CA-5.2.6"""
    from backend.koleo.api import crear_app
    ruta = tmp_path / "koleo.db"
    crear_bd(ruta).close()
    client = crear_app(str(ruta)).test_client()
    assert client.post("/api/ordenes", json=INICIAR).status_code == 503
    assert client.get("/api/robots").status_code == 200
