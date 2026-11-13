"""Logica de ordenes y registro de tarimas del tablero (WP-5.2, REQ-F-013/014).

El ack de una orden lo procesa ingesta.py (UPDATE de `ordenes`); aqui solo se crea
la orden en estado "pendiente" y se consulta.
"""
import re
import time
import uuid

TIPOS = ("INICIAR", "CANCELAR", "PARO")
TOPIC_ORDEN = "koleo/robot1/orden"
_RE_TARIMA = re.compile(r"^TAR-\d{3}$")


class ErrorValidacion(ValueError):
    pass


def _texto(v):
    return isinstance(v, str) and v.strip() != ""


def validar_orden(cuerpo):
    """Devuelve el payload de orden (sin id_orden ni ts) o lanza ErrorValidacion."""
    if not isinstance(cuerpo, dict):
        raise ErrorValidacion("cuerpo JSON requerido")
    tipo = cuerpo.get("tipo")
    if tipo not in TIPOS:
        raise ErrorValidacion("tipo debe ser INICIAR, CANCELAR o PARO")
    p = {"tipo": tipo}
    for campo in ("ruta", "id_tarima"):
        v = cuerpo.get(campo)
        if v is not None:
            if not _texto(v):
                raise ErrorValidacion(f"{campo} invalido")
            p[campo] = v
    if tipo == "INICIAR" and ("ruta" not in p or "id_tarima" not in p):
        raise ErrorValidacion("INICIAR requiere ruta e id_tarima")
    return p


def crear_orden(conn, publicador, cuerpo):
    p = validar_orden(cuerpo)
    if publicador is None:
        raise RuntimeError("publicador no configurado")
    ts = int(time.time() * 1000)
    id_orden = "ORD-" + uuid.uuid4().hex[:12]
    mensaje = {"ts": ts, "id_orden": id_orden, **p}
    publicador(TOPIC_ORDEN, mensaje)
    conn.execute(
        "INSERT OR IGNORE INTO ordenes (id_orden, tipo, ruta, id_tarima, estado, ts) "
        "VALUES (?,?,?,?, 'pendiente', ?)",
        (id_orden, p["tipo"], p.get("ruta"), p.get("id_tarima"), ts))
    conn.commit()
    return id_orden


def obtener_orden(conn, id_orden):
    f = conn.execute("SELECT * FROM ordenes WHERE id_orden=?", (id_orden,)).fetchone()
    return dict(f) if f else None


def registrar_tarima(conn, cuerpo):
    if not isinstance(cuerpo, dict):
        raise ErrorValidacion("cuerpo JSON requerido")
    id_t = cuerpo.get("id_tarima")
    if not isinstance(id_t, str) or not _RE_TARIMA.match(id_t):
        raise ErrorValidacion("id_tarima debe cumplir TAR-NNN")
    peso = cuerpo.get("peso_kg")
    if isinstance(peso, bool) or not isinstance(peso, (int, float)) or not (0 < peso <= 999.99):
        raise ErrorValidacion("peso_kg debe ser mayor que 0")
    desc = cuerpo.get("descripcion", "")
    if desc is None:
        desc = ""
    if not isinstance(desc, str) or len(desc) > 100:
        raise ErrorValidacion("descripcion invalida (max 100 caracteres)")
    from datetime import datetime, timezone
    ahora = datetime.now(timezone.utc).isoformat()
    try:
        conn.execute(
            "INSERT INTO tarimas (id_tarima, descripcion, peso_kg, estado, ultima_actualizacion) "
            "VALUES (?,?,?, 'EN_PISO', ?)", (id_t, desc, float(peso), ahora))
    except Exception as e:  # clave duplicada
        if "UNIQUE" in str(e) or "PRIMARY" in str(e):
            raise ErrorValidacion("la tarima ya existe") from e
        raise
    conn.commit()
    return id_t
