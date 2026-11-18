"""Lectura del RPLIDAR A1 desde la Pi (WP-4.4, REQ-F-006).

El puerto serie sale de la variable de entorno KOLEO_LIDAR_PUERTO (ver .env.example).
"""
import os
import queue
import threading

VARIABLE_PUERTO = "KOLEO_LIDAR_PUERTO"


class LidarSinDatos(Exception):
    """No llegó una vuelta completa dentro del tiempo de espera."""


def puerto_desde_entorno():
    puerto = os.environ.get("KOLEO_LIDAR_PUERTO")
    if not puerto:
        raise RuntimeError(f"Falta la variable de entorno {VARIABLE_PUERTO}")
    return puerto


def _al_marco_del_robot(angulo_driver_grados):
    """Driver: 0-360 en sentido horario. Robot: 0° al frente, positivo a la izquierda, (-180, 180]."""
    a = (0.0 - float(angulo_driver_grados) + 180.0) % 360.0 - 180.0
    return 180.0 if a == -180.0 else a


class RPLidarA1:
    def __init__(self, puerto=None, driver=None):
        self.puerto = puerto if puerto is not None else puerto_desde_entorno()
        if driver is None:
            from rplidar import RPLidar  # biblioteca PyPI `rplidar`
            driver = RPLidar(self.puerto)
        self._driver = driver

    def escanear(self, timeout_s=2.0):
        """Una vuelta completa como pares (ángulo en el marco del robot, distancia en cm)."""
        salida = queue.Queue()

        def leer():
            try:
                for vuelta in self._driver.iter_scans():
                    salida.put(vuelta)
                    return
                salida.put(None)
            except Exception as error:  # el driver real lanza RPLidarException
                salida.put(error)

        hilo = threading.Thread(target=leer, daemon=True)
        hilo.start()
        try:
            vuelta = salida.get(timeout=timeout_s)
        except queue.Empty:
            vuelta = None
        if vuelta is None or isinstance(vuelta, Exception):
            self._detener()
            raise LidarSinDatos(f"sin vuelta completa en {timeout_s} s")
        self._detener()
        return [
            (_al_marco_del_robot(angulo), float(mm) / 10.0)
            for _calidad, angulo, mm in vuelta
            if float(mm) > 0
        ]

    def _detener(self):
        try:
            self._driver.stop()
        except Exception:
            pass

    def cerrar(self):
        self._detener()
        for metodo in ("stop_motor", "disconnect"):
            try:
                getattr(self._driver, metodo)()
            except Exception:
                pass
