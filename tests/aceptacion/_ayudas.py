"""Ayudas compartidas por las pruebas de aceptación. No dependen de la implementación."""
import copy
import json
import sqlite3
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PREFIJO = "koleo/robot1/"
TS = 1700000000000

_TEMA_A_DEF = {
    "telemetria": "telemetria",
    "evento": "evento",
    "orden": "orden",
    "orden/ack": "orden_ack",
    "conexion": "conexion",
    "esp32/cmd": "esp32_cmd",
    "esp32/resp": "esp32_resp",
    "esp32/sensores": "esp32_sensores",
    "esp32/evento": "esp32_evento",
    "esp32/conexion": "conexion",
}


def cargar_esquema():
    return json.loads((RAIZ / "contratos" / "mensajes.schema.json").read_text(encoding="utf-8"))


def validador(nombre):
    import jsonschema

    esq = cargar_esquema()
    envoltura = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$defs": esq["$defs"],
        "$ref": f"#/$defs/{nombre}",
    }
    return jsonschema.Draft202012Validator(envoltura)


def es_valido(nombre, mensaje):
    return validador(nombre).is_valid(mensaje)


def errores(nombre, mensaje):
    return [e.message for e in validador(nombre).iter_errors(mensaje)]


def def_de_tema(tema):
    sufijo = tema[len(PREFIJO):] if tema.startswith(PREFIJO) else tema
    assert sufijo in _TEMA_A_DEF, f"tema fuera del contrato: {tema}"
    return _TEMA_A_DEF[sufijo]


def como_dict(payload):
    if isinstance(payload, (bytes, bytearray)):
        payload = payload.decode("utf-8")
    if isinstance(payload, str):
        return json.loads(payload)
    return payload


def aplanar(obj):
    """Todos los valores hoja de una estructura JSON."""
    if isinstance(obj, dict):
        for v in obj.values():
            yield from aplanar(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from aplanar(v)
    else:
        yield obj


def tiene_numero(obj, numero, tol=1e-6):
    return any(
        isinstance(v, (int, float)) and not isinstance(v, bool) and abs(v - numero) <= tol
        for v in aplanar(obj)
    )


def crear_bd(ruta):
    conn = sqlite3.connect(str(ruta))
    conn.executescript((RAIZ / "contratos" / "esquema.sql").read_text(encoding="utf-8"))
    conn.commit()
    return conn


def filas(conn, tabla):
    conn.row_factory = sqlite3.Row
    return [dict(f) for f in conn.execute(f"SELECT * FROM {tabla}")]


def eventos_de(mision, tipo=None):
    out = [p for t, p in mision if t.endswith("/evento") and not t.endswith("esp32/evento")]
    return [p for p in out if tipo is None or p.get("tipo") == tipo]


def evento_de_mision(mision, tipo):
    for p in eventos_de(mision, tipo):
        return copy.deepcopy(p)
    raise AssertionError(f"la misión no contiene evento {tipo}")
