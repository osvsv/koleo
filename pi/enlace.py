"""Enlace de comandos Pi-ESP32 por MQTT (WP-3.2).

El cliente inyectado implementa:
  publicar(topic, payload)               -> publica (payload es JSON str)
  esperar_respuesta(id_cmd, timeout_s)   -> dict de esp32/resp, o lanza TimeoutError
"""
import json
import time
import uuid

TEMA_CMD = "koleo/robot1/esp32/cmd"
TEMA_RESP = "koleo/robot1/esp32/resp"
TIMEOUT_S = 1.0


def _ts_ms():
    return int(time.time() * 1000)


def _nuevo_id():
    return "CMD-" + uuid.uuid4().hex[:12]


class EnlaceESP32:
    def __init__(self, cliente, timeout_s: float = TIMEOUT_S):
        self._cliente = cliente
        self._timeout_s = timeout_s

    def _publicar(self, cmd: dict):
        cmd = dict(cmd)
        cmd.setdefault("ts", _ts_ms())
        self._cliente.publicar(TEMA_CMD, json.dumps(cmd))

    def enviar(self, cmd: dict) -> dict:
        """Publica el comando y devuelve la respuesta con el mismo id_cmd.

        Sin respuesta en timeout_s lanza TimeoutError tras intentar enviar STOP
        (sin esperar su respuesta y sin reintentar el comando original).
        """
        cmd = dict(cmd)
        cmd.setdefault("id_cmd", _nuevo_id())
        self._publicar(cmd)
        try:
            return self._cliente.esperar_respuesta(cmd["id_cmd"], self._timeout_s)
        except TimeoutError:
            if cmd.get("cmd") != "STOP":
                try:
                    self._publicar({"cmd": "STOP", "id_cmd": _nuevo_id()})
                except Exception:
                    pass  # el STOP es de mejor esfuerzo; se reporta el timeout original
            raise

    def lift(self, id_tarima, peso_kg):
        return self.enviar({"cmd": "LIFT", "id_tarima": id_tarima, "peso_kg": peso_kg})

    def move(self, izq, der):
        return self.enviar({"cmd": "MOVE", "pwm_izq": izq, "pwm_der": der})

    def stop(self):
        return self.enviar({"cmd": "STOP"})

    def drop(self, id_tarima, x_cm, y_cm):
        return self.enviar({"cmd": "DROP", "id_tarima": id_tarima, "x_cm": x_cm, "y_cm": y_cm})
