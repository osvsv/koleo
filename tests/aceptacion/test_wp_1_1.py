"""WP-1.1 — Contratos MQTT, estados y SQL (CA-1.1.1 a CA-1.1.5, CA-1.1.7 parte del esquema, CA-1.1.8)."""
import copy
import json
import sqlite3

import pytest

from _ayudas import RAIZ, TS, cargar_esquema, es_valido

DEFS = ["telemetria", "evento", "orden", "orden_ack", "conexion",
        "esp32_cmd", "esp32_resp", "esp32_sensores", "esp32_evento"]

TELEMETRIA = {"ts": TS, "robot_id": "robot1", "x_cm": 0.0, "y_cm": 0.0,
              "velocidad_cm_s": 0.0, "estado": "INACTIVO", "peso_kg": 0.0,
              "distancia_obstaculo_cm": 100.0}
EVENTO = {"ts": TS, "robot_id": "robot1", "tipo": "LIFT_OK",
          "id_evento": "EV-1", "id_tarima": "TAR-101"}
ORDEN_INICIAR = {"ts": TS, "id_orden": "ORD-1", "tipo": "INICIAR",
                 "ruta": "RUTA_1", "id_tarima": "TAR-101"}
CONEXION = {"ts": TS, "robot_id": "robot1", "estado": "EN_LINEA"}
CMD = {"ts": TS, "id_cmd": "CMD-1", "cmd": "STOP"}
RESP = {"ts": TS, "id_cmd": "CMD-1", "resultado": "ACK", "codigo": "LIFT_OK"}
SENSORES = {"ts": TS, "peso_kg": 8.45, "distancia_obstaculo_cm": 40.0, "enc_izq": 10, "enc_der": 12}
ESP_EVENTO = {"ts": TS, "codigo": "OBSTACULO_CERCANO"}
DROP_OK = {**EVENTO, "tipo": "DROP_OK", "peso_kg": 8.45, "x_cm": 150, "y_cm": 120,
           "ruta": "RUTA_1", "origen_x_cm": 0, "origen_y_cm": 0}
SOBREPESO = {**EVENTO, "tipo": "SOBREPESO", "id_tarima": "TAR-102", "peso_kg": 11.8}


def sin(msg, clave):
    m = copy.deepcopy(msg)
    del m[clave]
    return m


def test_interfaz_defs_presentes():
    """Interfaz WP-1.1: JSON Schema 2020-12 con los $defs declarados."""
    esq = cargar_esquema()
    assert "2020-12" in esq.get("$schema", "")
    for d in DEFS:
        assert d in esq["$defs"], d


def test_ca_1_1_1_telemetria_valida_y_campos_obligatorios():
    """CA-1.1.1"""
    assert es_valido("telemetria", TELEMETRIA)
    for campo in TELEMETRIA:
        assert not es_valido("telemetria", sin(TELEMETRIA, campo)), f"{campo} debe ser obligatorio"


def test_ca_1_1_1_telemetria_ts_entero():
    """CA-1.1.1: ts es entero (ms)."""
    assert not es_valido("telemetria", {**TELEMETRIA, "ts": "ayer"})
    assert not es_valido("telemetria", {**TELEMETRIA, "ts": 1.5})


def test_ca_1_1_1_evento_valido_y_campos_obligatorios():
    """CA-1.1.1"""
    assert es_valido("evento", EVENTO)
    for campo in ("ts", "robot_id", "tipo", "id_evento", "id_tarima"):
        assert not es_valido("evento", sin(EVENTO, campo)), f"{campo} debe ser obligatorio"


@pytest.mark.parametrize("tipo", ["LIFT_OK", "OBSTACULO", "ERROR"])
def test_ca_1_1_1_evento_tipos_admitidos(tipo):
    """CA-1.1.1 (DROP_OK y SOBREPESO exigen campos extra, ver CA-1.1.8)."""
    assert es_valido("evento", {**EVENTO, "tipo": tipo})


def test_ca_1_1_2_orden_iniciar_y_obligatorios():
    """CA-1.1.2"""
    assert es_valido("orden", ORDEN_INICIAR)
    for campo in ("ts", "id_orden", "tipo", "ruta", "id_tarima"):
        assert not es_valido("orden", sin(ORDEN_INICIAR, campo)), f"{campo} debe ser obligatorio en INICIAR"


@pytest.mark.parametrize("tipo", ["CANCELAR", "PARO"])
def test_ca_1_1_2_orden_cancelar_y_paro_sin_ruta(tipo):
    """CA-1.1.2: solo INICIAR exige ruta e id_tarima."""
    msg = {"ts": TS, "id_orden": "ORD-2", "tipo": tipo}
    assert es_valido("orden", msg)
    for campo in ("ts", "id_orden", "tipo"):
        assert not es_valido("orden", sin(msg, campo))


@pytest.mark.parametrize("resultado", ["aceptada", "rechazada"])
def test_ca_1_1_2_orden_ack(resultado):
    """CA-1.1.2"""
    msg = {"ts": TS, "id_orden": "ORD-1", "resultado": resultado}
    assert es_valido("orden_ack", msg)
    assert not es_valido("orden_ack", sin(msg, "id_orden"))
    assert not es_valido("orden_ack", sin(msg, "resultado"))
    assert not es_valido("orden_ack", {**msg, "resultado": "quizas"})


@pytest.mark.parametrize("estado", ["EN_LINEA", "FUERA_DE_LINEA"])
def test_ca_1_1_2_conexion_estados_admitidos(estado):
    """CA-1.1.2"""
    assert es_valido("conexion", {**CONEXION, "estado": estado})


def test_ca_1_1_2_conexion_obligatorios_y_enum():
    """CA-1.1.2"""
    for campo in CONEXION:
        assert not es_valido("conexion", sin(CONEXION, campo)), campo
    assert not es_valido("conexion", {**CONEXION, "estado": "DESCONOCIDO"})


def test_ca_1_1_3_sin_ts_es_invalido():
    """CA-1.1.3"""
    assert not es_valido("telemetria", sin(TELEMETRIA, "ts"))
    assert not es_valido("evento", sin(EVENTO, "ts"))
    assert not es_valido("orden", sin(ORDEN_INICIAR, "ts"))


def test_ca_1_1_3_tipo_desconocido_es_invalido():
    """CA-1.1.3"""
    assert not es_valido("evento", {**EVENTO, "tipo": "EXPLOSION"})
    assert not es_valido("orden", {**ORDEN_INICIAR, "tipo": "BORRAR"})


def test_ca_1_1_4_estados_exactos():
    """CA-1.1.4"""
    estados = json.loads((RAIZ / "contratos" / "estados.json").read_text(encoding="utf-8"))
    robot = ["INACTIVO", "EN_MISION", "ELEVANDO", "EN_RUTA", "DEPOSITANDO",
             "DETENIDO_OBSTACULO", "ERROR"]
    tarima = ["EN_PISO", "EN_TRANSITO", "UBICADA_DESTINO", "BLOQUEADA_SOBREPESO"]
    assert sorted(estados["robot"]) == sorted(robot)
    assert sorted(estados["tarima"]) == sorted(tarima)
    assert len(estados["robot"]) == len(set(estados["robot"]))
    assert len(estados["tarima"]) == len(set(estados["tarima"]))


@pytest.fixture
def bd():
    conn = sqlite3.connect(":memory:")
    conn.executescript((RAIZ / "contratos" / "esquema.sql").read_text(encoding="utf-8"))
    yield conn
    conn.close()


def _columnas(conn, tabla):
    return {f[1] for f in conn.execute(f"PRAGMA table_info({tabla})")}


ESPERADAS = {
    "tarimas": ["id_tarima", "descripcion", "peso_kg", "ubicacion_nodo", "coord_x_cm",
                "coord_y_cm", "estado", "ultima_actualizacion"],
    "historial_movimientos": ["id_movimiento", "id_evento", "id_tarima", "ruta_ejecutada",
                              "origen_x_cm", "origen_y_cm", "destino_x_cm", "destino_y_cm",
                              "peso_medido_kg", "latencia_red_ms", "fecha_hora"],
    "registro_rechazos_seguridad": ["id_alerta", "id_tarima", "peso_detectado_kg", "motivo",
                                    "coord_x_cm", "coord_y_cm", "fecha_hora"],
}


@pytest.mark.parametrize("tabla", list(ESPERADAS))
def test_ca_1_1_5_tablas_y_columnas(bd, tabla):
    """CA-1.1.5: columnas de Documentación General §10.2 (+ id_evento en historial)."""
    tablas = {f[0] for f in bd.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert tabla in tablas
    faltan = set(ESPERADAS[tabla]) - _columnas(bd, tabla)
    assert not faltan, faltan


def test_ca_1_1_5_id_evento_unico(bd):
    """CA-1.1.5: id_evento es único en historial_movimientos."""
    unico = False
    for f in bd.execute("PRAGMA index_list(historial_movimientos)"):
        if f[2]:
            cols = [c[2] for c in bd.execute(f"PRAGMA index_info({f[1]})")]
            unico = unico or cols == ["id_evento"]
    assert unico, "id_evento debe tener restricción UNIQUE"


@pytest.mark.parametrize("tabla", ["historial_movimientos", "registro_rechazos_seguridad"])
def test_ca_1_1_5_claves_foraneas_a_tarimas(bd, tabla):
    """CA-1.1.5"""
    destinos = {f[2] for f in bd.execute(f"PRAGMA foreign_key_list({tabla})")}
    assert "tarimas" in destinos


def test_ca_1_1_7_esp32_cmd_sin_id_cmd_es_invalido():
    """CA-1.1.7 (parte del esquema): un esp32_cmd sin id_cmd es inválido."""
    assert es_valido("esp32_cmd", CMD)
    assert not es_valido("esp32_cmd", sin(CMD, "id_cmd"))


def test_ca_1_1_8_esp32_cmd():
    """CA-1.1.8"""
    for campo in CMD:
        assert not es_valido("esp32_cmd", sin(CMD, campo)), campo
    assert not es_valido("esp32_cmd", {**CMD, "id_cmd": 7})
    assert not es_valido("esp32_cmd", {**CMD, "cmd": "EXPLOTAR"})
    for cmd in ("LIFT", "MOVE", "STOP", "DROP"):
        assert es_valido("esp32_cmd", {**CMD, "cmd": cmd})
    completo = {**CMD, "cmd": "DROP", "id_tarima": "TAR-101", "pwm_izq": 80, "pwm_der": -80,
                "x_cm": 150, "y_cm": 120}
    assert es_valido("esp32_cmd", completo)


def test_ca_1_1_8_esp32_resp():
    """CA-1.1.8"""
    assert es_valido("esp32_resp", RESP)
    for campo in RESP:
        assert not es_valido("esp32_resp", sin(RESP, campo)), campo
    assert es_valido("esp32_resp", {**RESP, "resultado": "ERR", "codigo": "OVERWEIGHT"})
    assert not es_valido("esp32_resp", {**RESP, "resultado": "OK"})


def test_ca_1_1_8_esp32_sensores():
    """CA-1.1.8"""
    assert es_valido("esp32_sensores", SENSORES)
    for campo in SENSORES:
        assert not es_valido("esp32_sensores", sin(SENSORES, campo)), campo


@pytest.mark.parametrize("codigo", ["LIFT_OK", "OVERWEIGHT", "SCALE_FAIL", "NO_LOAD",
                                    "OBSTACULO_CERCANO", "DROP_OK"])
def test_ca_1_1_8_esp32_evento_codigos(codigo):
    """CA-1.1.8"""
    assert es_valido("esp32_evento", {**ESP_EVENTO, "codigo": codigo})
    assert es_valido("esp32_evento", {**ESP_EVENTO, "codigo": codigo,
                                      "id_tarima": "TAR-101", "peso_kg": 8.45})


def test_ca_1_1_8_esp32_evento_obligatorios_y_enum():
    """CA-1.1.8"""
    for campo in ESP_EVENTO:
        assert not es_valido("esp32_evento", sin(ESP_EVENTO, campo)), campo
    assert not es_valido("esp32_evento", {**ESP_EVENTO, "codigo": "OTRO"})


def test_ca_1_1_8_evento_drop_ok_exige_campos_extra():
    """CA-1.1.8"""
    assert es_valido("evento", DROP_OK)
    for campo in ("peso_kg", "x_cm", "y_cm", "ruta", "origen_x_cm", "origen_y_cm"):
        assert not es_valido("evento", sin(DROP_OK, campo)), campo


def test_ca_1_1_8_evento_sobrepeso_exige_peso():
    """CA-1.1.8"""
    assert es_valido("evento", SOBREPESO)
    assert not es_valido("evento", sin(SOBREPESO, "peso_kg"))
