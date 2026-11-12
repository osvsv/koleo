"""Ingesta de mensajes MQTT a SQLite (REQ-F-008, REQ-F-017, REQ-NF-003).

`procesar_mensaje` no hace commit: lo hace quien llama.

Tablas auxiliares propias del backend (no estan en contratos/esquema.sql, que es
canonico y no se modifica): `robots`, `ordenes` y `eventos_vistos`. Se crean
con CREATE TABLE IF NOT EXISTS la primera vez que se procesa un mensaje valido.
"""
import json
import logging
import math
from datetime import datetime, timezone
from pathlib import Path

import jsonschema

log = logging.getLogger("koleo.ingesta")

PREFIJO = "koleo/robot1/"
RAIZ = Path(__file__).resolve().parents[2]

_TEMA_A_DEF = {
    "telemetria": "telemetria",
    "evento": "evento",
    "orden": "orden",
    "orden/ack": "orden_ack",
    "conexion": "conexion",
}

TABLAS_AUX = """
CREATE TABLE IF NOT EXISTS robots (
    robot_id      VARCHAR(32) PRIMARY KEY,
    estado        VARCHAR(20),
    conexion      VARCHAR(20),
    x_cm          REAL,
    y_cm          REAL,
    peso_kg       REAL,
    distancia_obstaculo_cm REAL,
    ultimo_ts     INTEGER,
    ts_lift_ms    INTEGER,
    ultimo_ciclo_s REAL,
    ultima_precision_cm REAL
);
CREATE TABLE IF NOT EXISTS ordenes (
    id_orden   VARCHAR(64) PRIMARY KEY,
    tipo       VARCHAR(16),
    ruta       VARCHAR(32),
    id_tarima  VARCHAR(32),
    estado     VARCHAR(16) NOT NULL DEFAULT 'enviada',
    motivo     VARCHAR(200),
    ts         INTEGER,
    ts_ack     INTEGER
);
CREATE TABLE IF NOT EXISTS eventos_vistos (
    id_evento VARCHAR(64) PRIMARY KEY
);
"""

_validadores = {}


def asegurar_tablas(conn):
    conn.executescript(TABLAS_AUX)


def _validador(nombre):
    if nombre not in _validadores:
        esq = json.loads((RAIZ / "contratos" / "mensajes.schema.json").read_text(encoding="utf-8"))
        _validadores[nombre] = jsonschema.Draft202012Validator({
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$defs": esq["$defs"],
            "$ref": f"#/$defs/{nombre}",
        })
    return _validadores[nombre]


def _iso(ts_ms):
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).isoformat()


def _asegurar_tarima(conn, id_tarima, ts_ms):
    conn.execute(
        "INSERT OR IGNORE INTO tarimas (id_tarima, estado, ultima_actualizacion) "
        "VALUES (?, 'EN_PISO', ?)", (id_tarima, _iso(ts_ms)))


def _robot(conn, robot_id):
    conn.execute("INSERT OR IGNORE INTO robots (robot_id) VALUES (?)", (robot_id,))


def procesar_mensaje(conn, topic, payload, recibido_ms):
    """Valida `payload` contra el contrato y lo persiste. Descarta (y registra
    en el log) lo invalido; en ese caso no toca la BD."""
    if not isinstance(topic, str) or not topic.startswith(PREFIJO):
        log.warning("mensaje descartado: tema fuera del contrato %r", topic)
        return
    sufijo = topic[len(PREFIJO):]
    nombre = _TEMA_A_DEF.get(sufijo)
    if nombre is None:
        log.warning("mensaje descartado: tema sin manejador %r", topic)
        return
    if not isinstance(payload, dict):
        log.warning("mensaje descartado en %s: el payload no es un objeto", topic)
        return
    errores = [e.message for e in _validador(nombre).iter_errors(payload)]
    if errores:
        log.warning("mensaje invalido descartado en %s: %s", topic, "; ".join(errores))
        return
    asegurar_tablas(conn)
    if nombre == "telemetria":
        _telemetria(conn, payload)
    elif nombre == "evento":
        _evento(conn, payload, recibido_ms)
    elif nombre == "orden":
        _orden(conn, payload)
    elif nombre == "orden_ack":
        _ack(conn, payload)
    elif nombre == "conexion":
        _robot(conn, payload["robot_id"])
        conn.execute("UPDATE robots SET conexion=? WHERE robot_id=?",
                     (payload["estado"], payload["robot_id"]))


def _telemetria(conn, p):
    _robot(conn, p["robot_id"])
    conn.execute(
        "UPDATE robots SET estado=?, x_cm=?, y_cm=?, peso_kg=?, distancia_obstaculo_cm=?, "
        "ultimo_ts=? WHERE robot_id=?",
        (p["estado"], p["x_cm"], p["y_cm"], p["peso_kg"], p["distancia_obstaculo_cm"],
         p["ts"], p["robot_id"]))


def _evento(conn, p, recibido_ms):
    tipo, id_tarima, ts = p["tipo"], p["id_tarima"], p["ts"]
    if tipo == "DROP_OK":
        _drop_ok(conn, p, recibido_ms)
        return
    # Los reenvios por QoS 1 repiten id_evento: se procesan una sola vez.
    if conn.execute("INSERT OR IGNORE INTO eventos_vistos (id_evento) VALUES (?)",
                    (p["id_evento"],)).rowcount == 0:
        log.info("evento repetido ignorado: %s", p["id_evento"])
        return
    _asegurar_tarima(conn, id_tarima, ts)
    _robot(conn, p["robot_id"])
    if tipo == "LIFT_OK":
        conn.execute("UPDATE tarimas SET estado='EN_TRANSITO', peso_kg=COALESCE(?, peso_kg), "
                     "ultima_actualizacion=? WHERE id_tarima=?",
                     (p.get("peso_kg"), _iso(ts), id_tarima))
        conn.execute("UPDATE robots SET ts_lift_ms=? WHERE robot_id=?", (ts, p["robot_id"]))
    elif tipo == "SOBREPESO":
        x, y = conn.execute("SELECT x_cm, y_cm FROM robots WHERE robot_id=?",
                            (p["robot_id"],)).fetchone()[:2]
        conn.execute(
            "INSERT INTO registro_rechazos_seguridad "
            "(id_tarima, peso_detectado_kg, motivo, coord_x_cm, coord_y_cm, fecha_hora) "
            "VALUES (?,?,?,?,?,?)",
            (id_tarima, p["peso_kg"], "SOBREPESO", p.get("x_cm", x), p.get("y_cm", y), _iso(ts)))
        conn.execute("UPDATE tarimas SET estado='BLOQUEADA_SOBREPESO', peso_kg=?, "
                     "ultima_actualizacion=? WHERE id_tarima=?",
                     (p["peso_kg"], _iso(ts), id_tarima))
    # OBSTACULO y ERROR: solo se garantiza la tarima; no hay tabla canonica para ellos.


def _drop_ok(conn, p, recibido_ms):
    ts, id_tarima = p["ts"], p["id_tarima"]
    _asegurar_tarima(conn, id_tarima, ts)
    cur = conn.execute(
        "INSERT OR IGNORE INTO historial_movimientos (id_evento, id_tarima, ruta_ejecutada, "
        "origen_x_cm, origen_y_cm, destino_x_cm, destino_y_cm, peso_medido_kg, "
        "latencia_red_ms, fecha_hora) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (p["id_evento"], id_tarima, p["ruta"], p["origen_x_cm"], p["origen_y_cm"],
         p["x_cm"], p["y_cm"], p["peso_kg"], recibido_ms - ts, _iso(ts)))
    if cur.rowcount == 0:
        log.info("DROP_OK repetido ignorado: %s", p["id_evento"])
        return
    if recibido_ms - ts < 0:
        log.warning("latencia negativa (%d ms) en %s: relojes desfasados",
                    recibido_ms - ts, p["id_evento"])
    conn.execute(
        "UPDATE tarimas SET estado='UBICADA_DESTINO', coord_x_cm=?, coord_y_cm=?, peso_kg=?, "
        "ultima_actualizacion=? WHERE id_tarima=?",
        (p["x_cm"], p["y_cm"], p["peso_kg"], _iso(ts), id_tarima))
    _robot(conn, p["robot_id"])
    r = conn.execute("SELECT ts_lift_ms, x_cm, y_cm FROM robots WHERE robot_id=?",
                     (p["robot_id"],)).fetchone()
    ciclo = (ts - r[0]) / 1000 if r[0] is not None and ts >= r[0] else None
    precision = (math.hypot(r[1] - p["x_cm"], r[2] - p["y_cm"])
                 if r[1] is not None and r[2] is not None else None)
    conn.execute("UPDATE robots SET ultimo_ciclo_s=?, ultima_precision_cm=?, ts_lift_ms=NULL "
                 "WHERE robot_id=?", (ciclo, precision, p["robot_id"]))


def _orden(conn, p):
    conn.execute(
        "INSERT OR IGNORE INTO ordenes (id_orden, tipo, ruta, id_tarima, estado, ts) "
        "VALUES (?,?,?,?, 'enviada', ?)",
        (p["id_orden"], p["tipo"], p.get("ruta"), p.get("id_tarima"), p["ts"]))


def _ack(conn, p):
    cur = conn.execute("UPDATE ordenes SET estado=?, motivo=?, ts_ack=? WHERE id_orden=?",
                       (p["resultado"], p.get("motivo"), p["ts"], p["id_orden"]))
    if cur.rowcount == 0:
        log.warning("ack de orden desconocida ignorado: %s", p["id_orden"])
