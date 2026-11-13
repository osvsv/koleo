"""WP-1.3 — Backend de persistencia y Web API (CA-1.3.1 a CA-1.3.8 y CA-1.3.10 a CA-1.3.12; CA-1.3.9 requiere broker y no se prueba).

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


def test_ca_1_3_2_latencia_negativa_se_guarda_y_avisa(entorno, caplog):
    """CA-1.3.2 (CC-003): recibido_ms < ts se guarda sin recortar y se registra un aviso."""
    conn, _ = entorno
    caplog.set_level(logging.DEBUG)
    _procesar(conn, TEMA_EVENTO, _drop("EV-B2"), TS0 - 50)
    (fila,) = filas(conn, "historial_movimientos")
    assert fila["latencia_red_ms"] == -50
    assert any(r.levelno >= logging.WARNING for r in caplog.records), \
        "una latencia negativa debe registrar un aviso en el log"


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


CLAVES_INDICADORES = ("ocupacion", "posicion_robot", "tiempo_ciclo_s", "peso_kg",
                      "precision_cm", "alertas")


def test_ca_1_3_10_drop_ok_guarda_ruta_y_deja_ubicacion_nodo_nula(entorno):
    """CA-1.3.10 [D]. `ubicacion_nodo` existe solo en `tarimas` (no en historial)."""
    conn, _ = entorno
    _procesar(conn, TEMA_EVENTO, _drop("EV-H"), TS0 + 10)
    (h,) = filas(conn, "historial_movimientos")
    assert h["ruta_ejecutada"] == "RUTA_1"
    assert _tarima_bd(conn, "TAR-101")["ubicacion_nodo"] is None


def test_ca_1_3_11_indicadores_con_bd_vacia(entorno):
    """CA-1.3.11 [D]: BD vacía -> 200, seis claves, valores nulos o vacíos."""
    _, db = entorno
    resp = _api(db).get("/api/indicadores")
    assert resp.status_code == 200
    datos = resp.get_json()
    for clave in CLAVES_INDICADORES:
        assert clave in datos, clave
    assert datos["ocupacion"] == 0
    for clave in ("posicion_robot", "tiempo_ciclo_s", "peso_kg", "precision_cm", "alertas"):
        assert datos[clave] in (None, [], {}), f"{clave} debe ser nulo o vacío"


def test_ca_1_3_11_indicadores_tras_mision_ruta_1(entorno):
    """CA-1.3.11 [D]: misión RUTA_1 (8.45 kg) procesada."""
    from simulador.robot_falso import generar_mision
    conn, db = entorno
    mision = generar_mision("RUTA_1", 8.45)
    for tema, payload in mision:
        _procesar(conn, tema, copy.deepcopy(payload), payload["ts"] + 5)
    ts_lift = next(p["ts"] for _, p in mision if p.get("tipo") == "LIFT_OK")
    ts_drop = next(p["ts"] for _, p in mision if p.get("tipo") == "DROP_OK")
    ultima = [p for t, p in mision if t.endswith("/telemetria")][-1]

    resp = _api(db).get("/api/indicadores")
    assert resp.status_code == 200
    datos = resp.get_json()
    assert datos["ocupacion"] == pytest.approx(1.0)
    assert tiene_numero(datos["posicion_robot"], ultima["x_cm"])
    assert tiene_numero(datos["posicion_robot"], ultima["y_cm"])
    assert datos["peso_kg"] == pytest.approx(8.45)
    assert datos["precision_cm"] == pytest.approx(0.0)
    assert datos["tiempo_ciclo_s"] == pytest.approx((ts_drop - ts_lift) / 1000)


def _telemetria(ts=TS0 - 500, x=30.0, y=60.0):
    return {"ts": ts, "robot_id": "robot1", "x_cm": x, "y_cm": y,
            "velocidad_cm_s": 20.0, "estado": "EN_RUTA", "peso_kg": 0.0,
            "distancia_obstaculo_cm": 120.0}


def test_ca_1_3_12_rechazo_toma_coordenadas_de_ultima_telemetria(entorno):
    """CA-1.3.12 [D]"""
    conn, _ = entorno
    _procesar(conn, "koleo/robot1/telemetria", _telemetria(ts=TS0 - 1000, x=0.0, y=0.0), TS0 - 995)
    _procesar(conn, "koleo/robot1/telemetria", _telemetria(), TS0 - 495)
    _procesar(conn, TEMA_EVENTO, _sobrepeso(), TS0 + 10)
    (r,) = filas(conn, "registro_rechazos_seguridad")
    assert r["coord_x_cm"] == pytest.approx(30.0)
    assert r["coord_y_cm"] == pytest.approx(60.0)


def test_ca_1_3_12_rechazo_sin_telemetria_previa_deja_coordenadas_nulas(entorno):
    """CA-1.3.12 [D]"""
    conn, _ = entorno
    _procesar(conn, TEMA_EVENTO, _sobrepeso(), TS0 + 10)
    (r,) = filas(conn, "registro_rechazos_seguridad")
    assert r["coord_x_cm"] is None and r["coord_y_cm"] is None


# ---------------------------------------------------------------- CA-1.3.13 (CC-005)

def _telemetria_robot(robot_id="robot1", estado="EN_RUTA", velocidad=12.5, ts=TS0 - 500):
    return {"ts": ts, "robot_id": robot_id, "x_cm": 30.0, "y_cm": 60.0,
            "velocidad_cm_s": velocidad, "estado": estado, "peso_kg": 0.0,
            "distancia_obstaculo_cm": 120.0}


def _orden_iniciar_aceptada(conn):
    orden = {"ts": TS0 - 900, "id_orden": "ORD-13", "tipo": "INICIAR",
             "ruta": "RUTA_1", "id_tarima": "TAR-101"}
    _procesar(conn, "koleo/robot1/orden", orden, TS0 - 895)
    ack = {"ts": TS0 - 800, "id_orden": "ORD-13", "resultado": "aceptada"}
    _procesar(conn, "koleo/robot1/orden/ack", ack, TS0 - 795)


def _robot(db, robot_id):
    resp = _api(db).get("/api/robots")
    assert resp.status_code == 200
    r = [x for x in resp.get_json() if x.get("robot_id") == robot_id]
    assert len(r) == 1, f"{robot_id} debe aparecer una vez en /api/robots"
    return r[0]


def test_ca_1_3_13_robots_velocidad_y_ruta_actual_en_ruta(entorno):
    """CA-1.3.13 [D]"""
    conn, db = entorno
    _orden_iniciar_aceptada(conn)
    _procesar(conn, "koleo/robot1/telemetria", _telemetria_robot(), TS0 - 495)
    r = _robot(db, "robot1")
    assert r["velocidad_cm_s"] == pytest.approx(12.5)
    assert r["ruta_actual"] == "RUTA_1"


def test_ca_1_3_13_robots_ruta_actual_nula_si_inactivo(entorno):
    """CA-1.3.13 [D]"""
    conn, db = entorno
    _orden_iniciar_aceptada(conn)
    _procesar(conn, "koleo/robot1/telemetria",
              _telemetria_robot(estado="INACTIVO", velocidad=0.0), TS0 - 495)
    assert _robot(db, "robot1")["ruta_actual"] is None


def test_ca_1_3_13_robots_alertas_por_robot(entorno):
    """CA-1.3.13 [D]: el rechazo aparece en robot1 y no en robot2."""
    conn, db = entorno
    _procesar(conn, "koleo/robot1/telemetria", _telemetria_robot(), TS0 - 495)
    _procesar(conn, "koleo/robot2/telemetria", _telemetria_robot("robot2"), TS0 - 490)
    _procesar(conn, TEMA_EVENTO, _sobrepeso(), TS0 + 10)
    alertas = _robot(db, "robot1")["alertas"]
    assert len(alertas) == 1
    a = alertas[0]
    for clave in ("id_tarima", "peso_detectado_kg", "motivo", "fecha_hora"):
        assert clave in a, clave
    assert a["id_tarima"] == "TAR-102"
    assert a["peso_detectado_kg"] == pytest.approx(11.80)
    assert _robot(db, "robot2")["alertas"] == []


def test_ca_1_3_13_robots_alertas_maximo_5_mas_reciente_primero(entorno):
    """CA-1.3.13 [D]: con 6 sobrepesos solo quedan 5, el último primero."""
    conn, db = entorno
    _procesar(conn, "koleo/robot1/telemetria", _telemetria_robot(), TS0 - 495)
    for i in range(6):
        ev = _sobrepeso(f"EV-S{i}", ts=TS0 + i * 1000)
        ev["id_tarima"] = f"TAR-2{i:02d}"
        _procesar(conn, TEMA_EVENTO, ev, TS0 + i * 1000 + 10)
    alertas = _robot(db, "robot1")["alertas"]
    assert [a["id_tarima"] for a in alertas] == [f"TAR-2{i:02d}" for i in (5, 4, 3, 2, 1)]


def test_ca_1_3_13_robots_bd_vacia_devuelve_lista_vacia(entorno):
    """CA-1.3.13 [D]"""
    _, db = entorno
    resp = _api(db).get("/api/robots")
    assert resp.status_code == 200
    assert resp.get_json() == []
