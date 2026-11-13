# Auditoría WP-4.4 — iteración 1
Dictamen: NO CONFORME
Commit: d17df56400529808879ec63e8ff256efc5f570cd
Evidencia: docs/pm/evidencia/WP-4.4_it1_aceptacion_d17df56.log
Archivos auditados: pi/qr.py, pi/camara.py, pi/__init__.py, requirements.txt

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-4.4.1 | Cumple | El log (líneas 8 y 9, `.venv\Scripts\python.exe -m pytest tests/aceptacion -q`, commit d17df56) termina con "51 failed, 73 passed" (línea 946). Ningún test de test_wp_4_4.py aparece en la lista FAILED (líneas 895 a 945). Con el recuento de la barra de progreso, los "..." de la línea 9 entre los 11 F de test_wp_4_3 y los 8 F de test_wp_5_2 son las 3 pruebas de test_wp_4_4 y pasan. No hay omitidas: el importorskip no se activó. `test_ca_4_4_1_qr_tar_101` hace la aserción `== "TAR-101"` con un QR real generado. Implementación: pi/qr.py:21-26 (cv2.QRCodeDetector y `PATRON_TARIMA.fullmatch`). |
| CA-4.4.2 | Cumple | La prueba `test_ca_4_4_2_sin_qr_lanza_tarima_no_identificada` pasa (mismo log). Usa una imagen en blanco y `timeout_s=0.3`. Por inspección, el valor por defecto de 2.5 s está en pi/qr.py:14. Con lectura vacía el bucle llega al límite y lanza `TarimaNoIdentificada` (pi/qr.py:27-29), así que no hay ID por defecto (EJ-014). |
| CA-4.4.3 | Cumple | La prueba `test_ca_4_4_3_qr_con_formato_invalido` pasa con un QR "XYZ" (mismo log). Se usa `re.fullmatch(r"TAR-\d{3}")` (pi/qr.py:7 y :25), que rechaza también "TAR-1011" y textos con prefijo o sufijo. |
| CA-4.4.4 | Cumple | Inspección: pi/camara.py:2 `from picamera2 import Picamera2`, :9-12 configure/start, :15 `capture_array()`. Un Grep de `VideoCapture` en pi/ no da coincidencias. |
| CA-4.4.5 | No cumple (sin evidencia) | `docs/pm/evidencia/hw/WP-4.4/lectura_5_de_5.md` no existe: el Glob `docs/pm/evidencia/hw/WP-4.4/**` no devuelve archivos. |

## Hallazgos
### H-1 [Mayor] Falta la evidencia física de CA-4.4.5
- Criterio o requisito afectado: CA-4.4.5 [S]: en la Pi con el Camera Module 3, TAR-101 se lee en menos de 2.5 s en 5 de 5 intentos. Afecta también a REQ-F-007, cuyo método de verificación incluye "evidencia física".
- Evidencia: no existe `docs/pm/evidencia/hw/WP-4.4/lectura_5_de_5.md` ni ningún archivo bajo `docs/pm/evidencia/hw/WP-4.4/`. Las pruebas de aceptación usan una cámara falsa y no cubren el hardware ni la latencia real.
- Qué tendría que ser cierto para cerrarlo: que exista `docs/pm/evidencia/hw/WP-4.4/lectura_5_de_5.md`, aportado por una persona, con 5 intentos en la Pi con Camera Module 3 usando `pi.camara.CamaraPicamera2` y `pi.qr.identificar_tarima`. Cada intento debe registrar el tiempo medido (< 2.5 s) y el valor devuelto "TAR-101", además de la fecha, el responsable y las condiciones (distancia e iluminación). No hace falta cambiar código; si la lectura falla en el hardware, sí habría que corregirlo.

### H-2 [Observación] `picamera2` no figura en requirements.txt
- Criterio o requisito afectado: ninguno incumplido. Tiene relación con SUP-020.
- Evidencia: pi/camara.py:2 importa `picamera2`, pero requirements.txt solo agrega `opencv-python-headless==5.0.0.93`. En Raspberry Pi OS, picamera2 suele instalarse con apt (`python3-picamera2`), no con pip.
- Qué tendría que ser cierto para cerrarlo: dejar documentado cómo se instala picamera2 en la Pi, por ejemplo en la evidencia de CA-4.4.5.

### H-3 [Observación] El orden de canales de "RGB888" no coincide con el docstring
- Criterio o requisito afectado: ninguno incumplido.
- Evidencia: el docstring de pi/camara.py:6 dice "RGB, HxWx3", pero en Picamera2 el formato "RGB888" entrega los píxeles en orden BGR en el arreglo numpy. Para decodificar QR no importa.
- Qué tendría que ser cierto para cerrarlo: corregir el docstring o el formato si otro consumidor llega a depender del orden de canales.

## Alcance, integridad y regresión
- Alcance: el commit de trabajo 1acf146 toca pi/__init__.py, pi/camara.py, pi/qr.py y requirements.txt. pi/qr.py y pi/camara.py están en el Alcance de archivos del WP. pi/__init__.py y requirements.txt están registrados en docs/pm/desviaciones.md (líneas 8 y 9). No hay desvíos sin registrar.
- Integridad: 1acf146 no modifica nada en `docs/pm/` ni en `tests/aceptacion/`. `git diff 1acf146 HEAD -- pi requirements.txt` sale vacío.
- Evidencia: el log y el .json corresponden a HEAD d17df56. `arbol_limpio: false` se debe a archivos sin seguimiento (`ui/`, nuevos logs de evidencia y archivos espurios en la raíz: `$defs`, `` ` ``, `` numpy.ndarray` ``). Ninguno afecta a test_wp_4_4.
- Regresión: las pruebas de WP-1.1, WP-1.2 y WP-1.3 (las 70 primeras) pasan. Los 51 fallos son de test_wp_3_2, 4_1, 4_2, 4_3 y 5_2, de WP todavía sin implementar. No hay regresión atribuible a WP-4.4.
- Credenciales: ninguna en los archivos auditados.
- Limitación: el hook no permitió ejecutar `pytest -v` para aislar test_wp_4_4; el resultado de las 3 pruebas se verificó con la barra de progreso y la lista FAILED del log de la suite completa.

## Hallazgos de iteraciones previas: cerrados / persistentes
No aplica (iteración 1).
