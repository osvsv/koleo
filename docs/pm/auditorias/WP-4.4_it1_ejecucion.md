# WP-4.4 — informe de ejecución, iteración 1

Resultado: TERMINADO (CA-4.4.5 pendiente, es física)

Archivos creados o modificados:
- `pi/__init__.py`: creado, vacío (backend/ y simulador/ también son paquetes).
- `pi/qr.py`: `TarimaNoIdentificada` e `identificar_tarima(camara, timeout_s=2.5)`; captura en bucle, decodifica con `cv2.QRCodeDetector` y valida con `fullmatch` contra `TAR-\d{3}`; al vencer el timeout lanza la excepción tras al menos una captura.
- `pi/camara.py`: `CamaraPicamera2` con `capturar()` (`capture_array`, RGB888 640x480) y `cerrar()`; usa Picamera2, no `cv2.VideoCapture`.
- `requirements.txt`: añadido `opencv-python-headless==5.0.0.93` (SUP-020).

Autoverificación (del ejecutor):
- CA-4.4.1, 4.4.2, 4.4.3: pytest de `test_wp_4_4.py`, 3 passed.
- CA-4.4.4: por inspección al escribir el código; picamera2 solo existe en la Pi.
- CA-4.4.5: no verificado; requiere la Pi con Camera Module 3 (5 de 5 lecturas de TAR-101 en menos de 2.5 s). `docs/pm/evidencia/hw/WP-4.4/lectura_5_de_5.md` no se creó: debe aportarlo una persona.

Desviaciones:
| Archivo o criterio | Categoría | Nota |
| --- | --- | --- |
| requirements.txt | alcance | Dependencia nueva `opencv-python-headless` fijada, según SUP-020 |
| pi/__init__.py | alcance | Necesario para que `pi` sea paquete importable |

Bloqueos o contradicciones con la línea base: ninguno.
Variables de entorno nuevas: ninguna.

Sugerencias fuera de alcance:
- En la Pi, instalar `picamera2` con apt (`python3-picamera2`), no con pip; anotarlo en la documentación de despliegue.
- Confirmar que `opencv-python-headless` 5.0.0.93 tiene wheel para la arquitectura de la Pi.
- `main.py` debería llamar a `CamaraPicamera2.cerrar()` al terminar.
