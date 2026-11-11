"""WP-4.4 — Lectura QR (CA-4.4.1 a CA-4.4.3).

Requiere las librerías `numpy`, `qrcode` y `Pillow` solo para generar las imágenes de prueba
(se omiten con importorskip si faltan). El tiempo de espera se reduce con `timeout_s` para
que las pruebas sean rápidas.
"""
import time

import pytest

np = pytest.importorskip("numpy")
qrcode = pytest.importorskip("qrcode")
pytest.importorskip("PIL")


def _imagen_qr(texto):
    img = qrcode.make(texto, box_size=10, border=4).convert("RGB")
    return np.array(img, dtype=np.uint8)


class CamaraFalsa:
    def __init__(self, imagen):
        self.imagen = imagen
        self.capturas = 0

    def capturar(self):
        self.capturas += 1
        time.sleep(0.005)
        return self.imagen


def _blanco():
    return np.full((480, 640, 3), 255, dtype=np.uint8)


def test_ca_4_4_1_qr_tar_101():
    """CA-4.4.1"""
    from pi.qr import identificar_tarima
    assert identificar_tarima(CamaraFalsa(_imagen_qr("TAR-101"))) == "TAR-101"


def test_ca_4_4_2_sin_qr_lanza_tarima_no_identificada():
    """CA-4.4.2 (timeout reducido para la prueba)."""
    from pi.qr import TarimaNoIdentificada, identificar_tarima
    camara = CamaraFalsa(_blanco())
    t0 = time.monotonic()
    with pytest.raises(TarimaNoIdentificada):
        identificar_tarima(camara, timeout_s=0.3)
    assert time.monotonic() - t0 < 5
    assert camara.capturas >= 1


def test_ca_4_4_3_qr_con_formato_invalido():
    """CA-4.4.3"""
    from pi.qr import TarimaNoIdentificada, identificar_tarima
    with pytest.raises(TarimaNoIdentificada):
        identificar_tarima(CamaraFalsa(_imagen_qr("XYZ")), timeout_s=0.3)
