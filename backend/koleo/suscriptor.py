"""Suscriptor MQTT: recibe koleo/# y llama a procesar_mensaje.

Uso: python -m backend.koleo.suscriptor [--broker HOST] [--db RUTA]
Entorno: KOLEO_MQTT_HOST, KOLEO_MQTT_PORT, KOLEO_MQTT_USER, KOLEO_MQTT_PASSWORD, KOLEO_DB_PATH.
"""
import argparse
import json
import logging
import os
import sqlite3
import threading
import time

from .ingesta import RAIZ, procesar_mensaje

log = logging.getLogger("koleo.suscriptor")


def abrir_bd(ruta):
    conn = sqlite3.connect(ruta, check_same_thread=False, timeout=5)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript((RAIZ / "contratos" / "esquema.sql").read_text(encoding="utf-8"))
    conn.commit()
    return conn


def crear_cliente(conn, host, puerto, usuario=None, clave=None):
    import paho.mqtt.client as mqtt
    cli = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="koleo-backend")
    if usuario:
        cli.username_pw_set(usuario, clave or None)
    cerrojo = threading.Lock()

    def al_conectar(c, userdata, flags, rc, props=None):
        log.info("conectado al broker (%s)", rc)
        c.subscribe("koleo/#", qos=1)

    def al_mensaje(c, userdata, msg):
        recibido_ms = int(time.time() * 1000)
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            log.warning("mensaje descartado en %s: no es JSON valido", msg.topic)
            return
        with cerrojo:
            try:
                procesar_mensaje(conn, msg.topic, payload, recibido_ms)
                conn.commit()
            except Exception:
                conn.rollback()
                log.exception("error procesando %s", msg.topic)

    cli.on_connect = al_conectar
    cli.on_message = al_mensaje
    cli.connect(host, puerto)
    return cli


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m backend.koleo.suscriptor")
    ap.add_argument("--broker", default=os.environ.get("KOLEO_MQTT_HOST"))
    ap.add_argument("--db", default=os.environ.get("KOLEO_DB_PATH", "koleo.db"))
    args = ap.parse_args(argv)
    if not args.broker:
        ap.error("falta --broker o KOLEO_MQTT_HOST")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    conn = abrir_bd(args.db)
    cli = crear_cliente(conn, args.broker, int(os.environ.get("KOLEO_MQTT_PORT", "1883")),
                        os.environ.get("KOLEO_MQTT_USER"), os.environ.get("KOLEO_MQTT_PASSWORD"))
    try:
        cli.loop_forever()
    except KeyboardInterrupt:
        pass
    finally:
        cli.disconnect()
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
