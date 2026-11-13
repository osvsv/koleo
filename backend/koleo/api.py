"""Web API REST de KOLEO (REQ-F-011). Lee la BD SQLite del backend."""
import json
import os
import sqlite3

from flask import Flask, jsonify, request

from . import ordenes as ord_
from .ingesta import asegurar_tablas

ESTADOS_EN_RUTA = ("EN_MISION", "ELEVANDO", "EN_RUTA", "DEPOSITANDO")


def crear_app(db_path, publicador=None):
    """`publicador(topic, payload_dict)` publica las ordenes de POST /api/ordenes (REQ-F-011).

    Si es None, POST /api/ordenes responde 503; el resto de la API sigue funcionando.
    """
    app = Flask(__name__)

    def conectar():
        conn = sqlite3.connect(db_path, timeout=5)
        conn.row_factory = sqlite3.Row
        asegurar_tablas(conn)
        return conn

    def consulta(sql, args=()):
        conn = conectar()
        try:
            return [dict(f) for f in conn.execute(sql, args)]
        finally:
            conn.close()

    @app.get("/api/tarimas")
    def tarimas():
        return jsonify(consulta("SELECT * FROM tarimas ORDER BY id_tarima"))

    @app.get("/api/historial")
    def historial():
        return jsonify(consulta("SELECT * FROM historial_movimientos ORDER BY id_movimiento"))

    @app.get("/api/rechazos")
    def rechazos():
        return jsonify(consulta("SELECT * FROM registro_rechazos_seguridad ORDER BY id_alerta"))

    @app.get("/api/robots")
    def robots():
        filas = consulta("SELECT robot_id, estado, conexion, x_cm, y_cm, peso_kg, "
                         "distancia_obstaculo_cm, velocidad_cm_s, ultimo_ts FROM robots "
                         "ORDER BY robot_id")
        orden = consulta("SELECT ruta FROM ordenes WHERE tipo='INICIAR' AND estado='aceptada' "
                         "ORDER BY COALESCE(ts_ack, ts) DESC, rowid DESC LIMIT 1")
        for f in filas:
            f["ruta_actual"] = (orden[0]["ruta"] if orden and f["estado"] in ESTADOS_EN_RUTA
                                else None)
            f["alertas"] = consulta(
                "SELECT r.id_tarima, r.peso_detectado_kg, r.motivo, r.fecha_hora "
                "FROM registro_rechazos_seguridad r JOIN rechazos_robot x ON x.id_alerta=r.id_alerta "
                "WHERE x.robot_id=? ORDER BY r.id_alerta DESC LIMIT 5", (f["robot_id"],))
        return jsonify(filas)

    @app.get("/api/indicadores")
    def indicadores():
        total = consulta("SELECT COUNT(*) AS n FROM tarimas")[0]["n"]
        ubicadas = consulta("SELECT COUNT(*) AS n FROM tarimas WHERE estado='UBICADA_DESTINO'")[0]["n"]
        rob = (consulta("SELECT * FROM robots ORDER BY ultimo_ts DESC LIMIT 1") or [None])[0]
        alertas = consulta("SELECT id_tarima, peso_detectado_kg, motivo, fecha_hora FROM "
                           "registro_rechazos_seguridad ORDER BY id_alerta DESC LIMIT 5")
        return jsonify({
            "ocupacion": (ubicadas / total) if total else 0,
            "posicion_robot": ({"x_cm": rob["x_cm"], "y_cm": rob["y_cm"]}
                               if rob and rob["x_cm"] is not None else None),
            "tiempo_ciclo_s": rob["ultimo_ciclo_s"] if rob else None,
            "peso_kg": rob["peso_kg"] if rob else None,
            "precision_cm": rob["ultima_precision_cm"] if rob else None,
            "alertas": alertas,
        })

    @app.get("/api/ordenes")
    def ordenes():
        return jsonify(consulta("SELECT * FROM ordenes ORDER BY ts"))

    @app.post("/api/ordenes")
    def crear_orden():
        conn = conectar()
        try:
            id_orden = ord_.crear_orden(conn, publicador, request.get_json(silent=True))
        except ord_.ErrorValidacion as e:
            return jsonify({"error": str(e)}), 400
        except RuntimeError as e:
            return jsonify({"error": str(e)}), 503
        finally:
            conn.close()
        return jsonify({"id_orden": id_orden}), 202

    @app.get("/api/ordenes/<id_orden>")
    def orden(id_orden):
        conn = conectar()
        try:
            o = ord_.obtener_orden(conn, id_orden)
        finally:
            conn.close()
        return (jsonify(o), 200) if o else (jsonify({"error": "orden no encontrada"}), 404)

    @app.post("/api/tarimas")
    def registrar_tarima():
        conn = conectar()
        try:
            id_t = ord_.registrar_tarima(conn, request.get_json(silent=True))
        except ord_.ErrorValidacion as e:
            return jsonify({"error": str(e)}), 400
        finally:
            conn.close()
        return jsonify({"id_tarima": id_t}), 201

    return app


def crear_publicador(env, cliente=None):
    """Devuelve `publicador(topic, payload_dict)` sobre MQTT, o None si falta KOLEO_MQTT_HOST."""
    host = env.get("KOLEO_MQTT_HOST")
    if not host:
        return None
    if cliente is None:
        import paho.mqtt.client as mqtt
        cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="koleo-api")
        usuario = env.get("KOLEO_MQTT_USER")
        if usuario:
            cliente.username_pw_set(usuario, env.get("KOLEO_MQTT_PASSWORD") or None)
        cliente.connect(host, int(env.get("KOLEO_MQTT_PORT") or 1883))
        cliente.loop_start()

    def publicador(topic, payload):
        cliente.publish(topic, json.dumps(payload), qos=1)

    return publicador


def main():
    app = crear_app(os.environ.get("KOLEO_DB_PATH", "koleo.db"),
                    crear_publicador(os.environ))
    app.run(host=os.environ.get("KOLEO_API_HOST", "127.0.0.1"),
            port=int(os.environ.get("KOLEO_API_PORT", "5000")))


if __name__ == "__main__":
    main()
