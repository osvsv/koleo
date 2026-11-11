"""WP-1.3 — Backend de persistencia y Web API (CA-1.3.1 a CA-1.3.8; CA-1.3.9 requiere broker y no se prueba).

`procesar_mensaje` crea la tarima (EN_PISO) si no existe, por eso no se siembra.
"""
import copy
import logging

import pytest

from _ayudas import aplanar, crear_bd, filas, tiene_numero

TEMA_EVENTO = "koleo/robot1/evento"
TS0 = 1700000000000


@pytest.fixture
def entorno(tmp_path):
    ruta = tmp_path / "koleo.db"
    conn = crear_bd(ruta)
    yield conn, str(ruta)
    conn.close()


def _procesar(conn, topic, payload, recibido_ms):
    from backend.koleo.ingesta import procesar_mensaje
    procesar_mensaje(conn, topic, payload, recibido_ms)
    conn.commit()


def _drop(id_evento, id_tarima="TAR-101", ts=TS0):
    return {"ts": ts, "robot_id": "robot1", "tipo": "DROP_OK", "id_evento": id_evento,
            "id_tarima": id_tarima, "peso_kg": 8.45, "x_cm": 150, "y_cm": 120,
            "ruta": "RUTA_1", "origen_x_cm": 0, "origen_y_cm": 0}


def _sobrepeso(id_evento="EV-S1", ts=TS0):
    return {"ts": ts, "robot_id": "robot1", "tipo": "SOBREPESO", "id_evento": id_evento,
            "id_tarima": "TAR-102", "peso_kg": 11.80}


def _api(db_path):
    from backend.koleo.api import crear_app
    return crear_app(db_path).test_client()


def _tarima_bd(conn, id_tarima):
    ts = [t for t in filas(conn, "tarimas") if t["id_tarima"] == id_tarima]
    assert len(ts) == 1, f"{id_tarima} debe existir una vez en tarimas"
    return ts[0]


def test_ca_1_3_1_drop_ok_ubica_tarima_y_crea_historial(entorno):
    """CA-1.3.1"""
    conn, _ = entorno
    _procesar(conn, TEMA_EVENTO, _drop("EV-A"), TS0 + 20)
    t = _tarima_bd(conn, "TAR-101")
    assert t["estado"] == "UBICADA_DESTINO"
    assert t["coord_x_cm"] == 150 and t["coord_y_cm"] == 120
    (h,) = filas(conn, "historial_movimientos")
    assert h["id_tarima"] == "TAR-101"


@pytest.mark.parametrize("delta", [37, 0])
def test_ca_1_3_2_latencia_es_recibido_menos_ts(entorno, delta):
    """CA-1.3.2"""
    conn, _ = entorno
    _procesar(conn, TEMA_EVENTO, _drop("EV-B"), TS0 + delta)
    (fila,) = filas(conn, "historial_movimientos")
    assert fila["latencia_red_ms"] == delta >= 0


def test_ca_1_3_3_sobrepeso_registra_rechazo_y_bloquea(entorno):
    """CA-1.3.3"""
    conn, _ = entorno
    _procesar(conn, TEMA_EVENTO, _sobrepeso(), TS0 + 10)
    (r,) = filas(conn, "registro_rechazos_seguridad")
    assert r["id_tarima"] == "TAR-102"
    assert r["peso_detectado_kg"] == pytest.approx(11.80)
    assert filas(conn, "historial_movimientos") == []
    assert _tarima_bd(conn, "TAR-102")["estado"] == "BLOQUEADA_SOBREPESO"


def test_ca_1_3_4_tres_misiones_dos_historiales_un_rechazo(entorno):
    """CA-1.3.4 (VAL-08)"""
    from simulador.robot_falso import generar_mision
    conn, _ = entorno
    for ruta, peso in (("RUTA_1", 8.45), ("RUTA_2", 11.80), ("RUTA_3", 6.20)):
        for tema, payload in generar_mision(ruta, peso):
            _procesar(conn, tema, copy.deepcopy(payload), payload["ts"] + 5)
    assert len(filas(conn, "historial_movimientos")) == 2
    assert len(filas(conn, "registro_rechazos_seguridad")) == 1


def _instantanea(conn):
    return list(conn.iterdump())


@pytest.mark.parametrize("defecto", ["sin_ts", "tipo_desconocido"])
def test_ca_1_3_5_mensaje_invalido_se_descarta_y_se_registra(entorno, caplog, defecto):
    """CA-1.3.5"""
    conn, _ = entorno
    ev = _drop("EV-C")
    if defecto == "sin_ts":
        del ev["ts"]
    else:
        ev["tipo"] = "EXPLOSION"
    antes = _instantanea(conn)
    caplog.set_level(logging.DEBUG)
    _procesar(conn, TEMA_EVENTO, ev, TS0 + 100)
    assert _instantanea(conn) == antes
    assert len(caplog.records) >= 1, "el descarte debe quedar en el log"


def test_ca_1_3_6_mismo_id_evento_no_duplica(entorno):
    """CA-1.3.6 [D]"""
    conn, _ = entorno
    ev = _drop("EV-D")
    _procesar(conn, TEMA_EVENTO, ev, TS0 + 10)
    _procesar(conn, TEMA_EVENTO, copy.deepcopy(ev), TS0 + 30)
    assert len(filas(conn, "historial_movimientos")) == 1


def test_ca_1_3_6_id_evento_distintos_crean_dos_filas(entorno):
    """CA-1.3.6 [D]: dos entregas de la misma tarima."""
    conn, _ = entorno
    _procesar(conn, TEMA_EVENTO, _drop("EV-E1"), TS0 + 10)
    _procesar(conn, TEMA_EVENTO, _drop("EV-E2", ts=TS0 + 1000), TS0 + 1010)
    assert len(filas(conn, "historial_movimientos")) == 2


def test_ca_1_3_6_drop_sin_id_evento_se_descarta(entorno):
    """CA-1.3.6 [D]"""
    conn, _ = entorno
    ev = _drop("EV-F")
    del ev["id_evento"]
    _procesar(conn, TEMA_EVENTO, ev, TS0 + 10)
    assert filas(conn, "historial_movimientos") == []


def test_ca_1_3_7_tarimas_devuelve_id_estado_y_coordenadas(entorno):
    """CA-1.3.7"""
    conn, db = entorno
    _procesar(conn, TEMA_EVENTO, _drop("EV-G"), TS0 + 10)
    resp = _api(db).get("/api/tarimas")
    assert resp.status_code == 200
    t = [x for x in resp.get_json() if "TAR-101" in list(aplanar(x))]
    assert len(t) == 1
    assert "UBICADA_DESTINO" in list(aplanar(t[0]))
    assert tiene_numero(t[0], 150) and tiene_numero(t[0], 120)


def test_ca_1_3_7_historial_vacio_devuelve_lista_vacia(entorno):
    """CA-1.3.7"""
    _, db = entorno
    resp = _api(db).get("/api/historial")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_ca_1_3_8_indicadores_claves(entorno):
    """CA-1.3.8"""
    _, db = entorno
    resp = _api(db).get("/api/indicadores")
    assert resp.status_code == 200
    datos = resp.get_json()
    for clave in ("ocupacion", "posicion_robot", "tiempo_ciclo_s", "peso_kg",
                  "precision_cm", "alertas"):
        assert clave in datos, clave
