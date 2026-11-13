# Auditoría WP-1.2 — iteración 5
Dictamen: CONFORME CON OBSERVACIONES
Commit: 7ccd0964e0c2b9b6a26e0022322013b9517f73ed
Evidencia: docs/pm/evidencia/WP-1.2_it5_aceptacion_7ccd096.log
Archivos auditados: simulador/__init__.py, simulador/robot_falso.py, requirements.txt, .env.example, docs/pm/evidencia/WP-1.2/captura_mosquitto.txt
Tipo: reverificación

**Resumen:** desde 615282d, el único archivo auditado que cambió es requirements.txt, por el commit 1acf146 de WP-4.4 (una línea añadida, registrada en desviaciones.md:8). El cambio de contratos por CC-004 solo toca las definiciones `esp32_*`, que el simulador no usa. Las pruebas de test_wp_1_2.py no fallan en el log de HEAD y ese archivo no cambió. No hay hallazgos nuevos; siguen abiertas las dos observaciones del dictamen anterior.

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-1.2.1 | Cumple | El log es de HEAD 7ccd096 (log:2) y termina en "51 failed, 73 passed" (log:946). Ninguna de las 51 líneas FAILED (log:895-945) es de test_wp_1_2.py: son de test_wp_3_2, 4_1, 4_2, 4_3 y 5_2. La prueba valida contra el esquema vigente (test_wp_1_2.py:16-21), que ya incluye CC-004. |
| CA-1.2.2 | Cumple | test_wp_1_2.py:43-51 no aparece entre las fallas. `evento` y `telemetria` no cambiaron con CC-004 (`git diff 615282d..HEAD -- contratos`). |
| CA-1.2.3 | Cumple | test_wp_1_2.py:54-65 no aparece entre las fallas. |
| CA-1.2.4 | Cumple | test_wp_1_2.py:68-71 no aparece entre las fallas. |
| CA-1.2.5 | Cumple | test_wp_1_2.py:74-80 no aparece entre las fallas. |
| CA-1.2.6 | Cumple | `git log 615282d..HEAD -- docs/pm/evidencia/WP-1.2` no devuelve commits: la captura es la misma. CC-004 no cambió los temas MQTT (contratos/mqtt.md no está en el diff). |
| CA-1.2.7 | Cumple | test_wp_1_2.py:85-101 no aparece entre las fallas. El texto coincide con docs/pm/03-wbs.md:69 (v1.4). |

## Cambios reverificados
| Commit | WP de origen | Archivo | Efecto |
| --- | --- | --- | --- |
| 1acf146 "[WP-4.4] it1: lectura QR con Picamera2 y validación TAR-NNN" | WP-4.4 | requirements.txt (+1: `opencv-python-headless==5.0.0.93`) | Registrado en docs/pm/desviaciones.md:8. Añade una dependencia que el simulador no importa; no cambia `paho-mqtt==2.1.0`, necesario para `--broker`. No afecta a ningún criterio. |
| e96ab71 "[WP-1.1] it3: contratos del ESP32 con peso declarado (CC-004)" | WP-1.1 | contratos/mensajes.schema.json, contratos/esp32.md (no auditados por WP-1.2, pero el simulador valida contra ellos) | Cambian `esp32_cmd`, `esp32_resp`, `esp32_evento` y `esp32_sensores`. El simulador solo emite `telemetria` y `evento` (simulador/robot_falso.py:64, 76-86), que no cambiaron. Sigue conforme. |

`git log 615282d..HEAD` sobre simulador/, tests/aceptacion/test_wp_1_2.py, docs/pm/evidencia/WP-1.2 y .env.example no devuelve commits. Las pruebas no se debilitaron: las 9 funciones de test, con sus parametrizaciones, siguen iguales.

## Hallazgos
El diff no genera hallazgos nuevos.

Observaciones abiertas del dictamen anterior (solo se listan):
- H-2 [Observación], abierta: el comentario de simulador/robot_falso.py:23-24 está desactualizado y no cita CC-002.
- H-3 [Observación], abierta: `connect` no captura errores y `wait_for_publish` no tiene timeout (simulador/robot_falso.py:106, 111).

## Alcance, integridad y regresión
- Alcance: el único cambio en un archivo auditado (1acf146, WP-4.4) está registrado en desviaciones.md:8.
- Integridad de la evidencia: el log dice "Árbol limpio: no" (log:4). `git status --porcelain --untracked-files=all` solo muestra archivos sin seguimiento: los dos de esta evidencia y tres sueltos en la raíz con nombres anómalos (`$defs`, `` ` ``, `` numpy.ndarray` ``), restos de una redirección de shell mal escapada, ajenos a WP-1.2. No hay archivos con seguimiento modificados ni sueltos en simulador/ o tests/.
- Regresión: pasan 73 pruebas (68 en it4). Ninguna de test_wp_1_1, 1_2, 1_3 ni 4_4 falla. Las 51 fallas son de WP pendientes (3.2, 4.1, 4.2, 4.3, 5.2) por módulos que aún no existen (por ejemplo, log:26-27, `pi.enlace`).
- Credenciales: el código del simulador no cambió y la línea añadida a requirements.txt no contiene secretos. Sobre .env.example sigue la salvedad de it4: no se pudo leer por permisos, aunque no cambió desde entonces.

## Hallazgos de iteraciones previas: cerrados / persistentes
- H-1 [Mayor] (it2): sigue cerrado. La captura no cambió.
- H-2 [Observación]: persistente, no bloquea.
- H-3 [Observación]: persistente, no bloquea.
