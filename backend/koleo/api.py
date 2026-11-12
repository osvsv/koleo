"""Web API REST de KOLEO (REQ-F-011). Lee la BD SQLite del backend."""
import os
import sqlite3

from flask import Flask, jsonify

from .ingesta import asegurar_tablas


def crear_app(db_path, publicador=None):
    """`publicador(topic, payload_dict)` se conserva para el WP-5.2 (publicacion de ordenes); aqui no se usa."""
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
        return jsonify(consulta("SELECT robot_id, estado, conexion, x_cm, y_cm, peso_kg, "
                                "distancia_obstaculo_cm, ultimo_ts FROM robots ORDER BY robot_id"))

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

    return app


def main():
    app = crear_app(os.environ.get("KOLEO_DB_PATH", "koleo.db"))
    app.run(host=os.environ.get("KOLEO_API_HOST", "127.0.0.1"),
            port=int(os.environ.get("KOLEO_API_PORT", "5000")))


if __name__ == "__main__":
    main()
