"""Cámara de la Raspberry Pi (Camera Module 3) con Picamera2."""
from picamera2 import Picamera2


class CamaraPicamera2:
    """Implementa `capturar() -> numpy.ndarray` (RGB, HxWx3)."""

    def __init__(self, ancho: int = 640, alto: int = 480):
        self._picam = Picamera2()
        self._picam.configure(self._picam.create_still_configuration(
            main={"size": (ancho, alto), "format": "RGB888"}))
        self._picam.start()

    def capturar(self):
        return self._picam.capture_array()

    def cerrar(self):
        self._picam.stop()
        self._picam.close()
