"""Robot simulado: genera (y opcionalmente publica por MQTT) una misión conforme
a contratos/mensajes.schema.json y contratos/mqtt.md.

Uso: python -m simulador.robot_falso --ruta RUTA_1 --peso 8.45 [--broker HOST]
Entorno: KOLEO_MQTT_PORT, KOLEO_MQTT_USER, KOLEO_MQTT_PASSWORD.
"""
import argparse
import json
import os
import sys
import time
import uuid

PREFIJO = "koleo/robot1/"
ROBOT_ID = "robot1"
LIMITE_KG = 10.0          # límite inclusivo (REQ-F-009)
PASO_MS = 500             # telemetría 2 veces por segundo
CELDA_CM = 30
VELOCIDAD_CM_S = 20.0

# Simulación: cada ruta de referencia parte de la celda (0, 0) y lleva una tarima
# fija. Destino = celda (fila, col) -> (x_cm, y_cm) = (col*30, fila*30);
# RUTA_1 termina en (4, 5) -> (150, 120). Las metas de RUTA_2 y RUTA_3 son
# supuestos del simulador (cuentan 6 y 8 celdas con camino en L).
RUTAS = {
    "RUTA_1": {"id_tarima": "TAR-101", "meta": (4, 5)},
    "RUTA_2": {"id_tarima": "TAR-102", "meta": (2, 3)},
    "RUTA_3": {"id_tarima": "TAR-103", "meta": (3, 4)},
}


def _camino(meta):
    """Celdas (fila, col) de (0,0) a meta: primero filas, luego columnas."""
    fila, col = meta
    celdas = [(f, 0) for f in range(fila + 1)]
    celdas += [(fila, c) for c in range(1, col + 1)]
    return celdas


def _cm(celda):
    return float(celda[1] * CELDA_CM), float(celda[0] * CELDA_CM)


def generar_mision(ruta, peso_kg):
    """Devuelve [(tema, payload), ...] en orden. ValueError si la ruta no existe."""
    if ruta not in RUTAS:
        raise ValueError(f"ruta desconocida: {ruta!r}")
    peso_kg = float(peso_kg)
    if peso_kg < 0:
        raise ValueError("peso_kg no puede ser negativo")
    cfg = RUTAS[ruta]
    id_tarima = cfg["id_tarima"]
    camino = _camino(cfg["meta"])
    ox, oy = _cm(camino[0])
    dx, dy = _cm(camino[-1])
    ts = int(time.time() * 1000)
    corrida = uuid.uuid4().hex[:12]
    msgs = []

    def telem(estado, x, y, vel, peso):
        nonlocal ts
        msgs.append((PREFIJO + "telemetria", {
            "ts": ts, "robot_id": ROBOT_ID, "x_cm": x, "y_cm": y,
            "velocidad_cm_s": vel, "estado": estado, "peso_kg": peso,
            "distancia_obstaculo_cm": 120.0}))
        ts += PASO_MS

    def evento(tipo, **extra):
        # Mismo ts que la última telemetría emitida (ts ya avanzó un paso).
        p = {"ts": ts - PASO_MS, "robot_id": ROBOT_ID, "tipo": tipo,
             "id_evento": f"EV-{corrida}-{tipo}-{len(msgs)}", "id_tarima": id_tarima}
        p.update(extra)
        msgs.append((PREFIJO + "evento", p))

    telem("EN_MISION", ox, oy, 0.0, 0.0)
    telem("ELEVANDO", ox, oy, 0.0, peso_kg)
    if peso_kg > LIMITE_KG:
        evento("SOBREPESO", peso_kg=peso_kg)
        telem("INACTIVO", ox, oy, 0.0, 0.0)
        return msgs
    evento("LIFT_OK", peso_kg=peso_kg)
    for celda in camino[1:]:
        x, y = _cm(celda)
        telem("EN_RUTA", x, y, VELOCIDAD_CM_S, peso_kg)
    telem("DEPOSITANDO", dx, dy, 0.0, peso_kg)
    evento("DROP_OK", peso_kg=peso_kg, x_cm=dx, y_cm=dy, ruta=ruta,
           origen_x_cm=ox, origen_y_cm=oy)
    return msgs


def _publicar(mensajes, host, puerto, usuario, clave):
    try:
        import paho.mqtt.client as mqtt
    except ImportError:
        print("Falta paho-mqtt (pip install paho-mqtt) para usar --broker", file=sys.stderr)
        return 2
    try:
        cli = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"koleo-sim-{uuid.uuid4().hex[:6]}")
    except AttributeError:  # paho-mqtt 1.x
        cli = mqtt.Client(client_id=f"koleo-sim-{uuid.uuid4().hex[:6]}")
    if usuario:
        cli.username_pw_set(usuario, clave or None)
    ahora = int(time.time() * 1000)
    testamento = {"ts": ahora, "robot_id": ROBOT_ID, "estado": "FUERA_DE_LINEA"}
    cli.will_set(PREFIJO + "conexion", json.dumps(testamento), qos=1, retain=True)
    cli.connect(host, puerto)
    cli.loop_start()
    try:
        def pub(tema, payload, qos, retain=False):
            info = cli.publish(tema, json.dumps(payload), qos=qos, retain=retain)
            info.wait_for_publish()

        pub(PREFIJO + "conexion", {"ts": ahora, "robot_id": ROBOT_ID, "estado": "EN_LINEA"}, 1, True)
        for tema, payload in mensajes:
            qos = 0 if tema.endswith("/telemetria") else 1
            pub(tema, payload, qos)
            if qos == 0:
                time.sleep(PASO_MS / 1000)
        pub(PREFIJO + "conexion",
            {"ts": int(time.time() * 1000), "robot_id": ROBOT_ID, "estado": "FUERA_DE_LINEA"}, 1, True)
    finally:
        cli.loop_stop()
        cli.disconnect()
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m simulador.robot_falso")
    ap.add_argument("--ruta", required=True)
    ap.add_argument("--peso", required=True, type=float)
    ap.add_argument("--broker", help="host MQTT; sin él solo imprime la misión")
    args = ap.parse_args(argv)
    try:
        mision = generar_mision(args.ruta, args.peso)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    host = args.broker
    if not host:
        for tema, payload in mision:
            print(tema, json.dumps(payload))
        return 0
    puerto = int(os.environ.get("KOLEO_MQTT_PORT", "1883"))
    return _publicar(mision, host, puerto, os.environ.get("KOLEO_MQTT_USER"),
                     os.environ.get("KOLEO_MQTT_PASSWORD"))


if __name__ == "__main__":
    raise SystemExit(main())
