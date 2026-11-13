"""WP-4.4 — Lectura QR y validación del formato de tarima `TAR-NNN` (REQ-F-007)."""
import re
import time

import cv2

PATRON_TARIMA = re.compile(r"TAR-\d{3}")


class TarimaNoIdentificada(Exception):
    """No se leyó un QR válido (`TAR-NNN`) dentro del tiempo de espera."""


def identificar_tarima(camara, timeout_s: float = 2.5) -> str:
    """Captura imágenes hasta leer un QR con formato `TAR-NNN`.

    `camara` es un objeto con `capturar() -> numpy.ndarray`. Si no se obtiene un
    identificador válido en `timeout_s` segundos, lanza `TarimaNoIdentificada`.
    """
    detector = cv2.QRCodeDetector()
    limite = time.monotonic() + timeout_s
    while True:
        imagen = camara.capturar()
        texto, _, _ = detector.detectAndDecode(imagen)
        if texto and PATRON_TARIMA.fullmatch(texto):
            return texto
        if time.monotonic() >= limite:
            raise TarimaNoIdentificada(
                "no se leyó un QR TAR-NNN en %.1f s" % timeout_s)
