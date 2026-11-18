# Auditoría WP-3.2 — iteración 3
Dictamen: NO CONFORME
Commit: 783165665e7d5649a5d016996f5c4897078ed2f3
Evidencia: docs/pm/evidencia/WP-3.2_it3_aceptacion_7831656.log
Archivos auditados: pi/enlace.py, firmware/.gitignore, firmware/esp32/platformio.ini, firmware/esp32/src/main.cpp, firmware/esp32/src/red_mqtt.cpp, firmware/esp32/src/red_mqtt.h, firmware/esp32/src/secrets.example.h

**Resumen:** los cuatro criterios vigentes (CA-3.2.1, 3.2.2, 3.2.3 y 3.2.6) se cumplen y no hay hallazgos Mayores ni Menores. El dictamen es NO CONFORME por un único hallazgo de Línea base (H-1): una contradicción entre documentos de la línea base, no un defecto del código. El ejecutor no tiene nada que corregir. Para cerrarlo hace falta una aclaración aprobada con `/pm-cambio`; después basta con volver a auditar, sin trabajo nuevo.

## Verificación por criterio
| Criterio | Resultado | Evidencia |
| --- | --- | --- |
| CA-3.2.1 | Cumple | `pytest tests/aceptacion/test_wp_3_2.py -v`: `test_ca_3_2_1_lift_ack_devuelve_la_respuesta` y `test_ca_3_2_1_lift_overweight_devuelve_error_sin_lanzar` PASSED. El log (`-q`) solo registra fallos de test_wp_4_1/4_2/4_3. pi/enlace.py:53-54 publica LIFT con el `peso_kg` tal cual, sin validarlo en la Pi. Correlación: pi/enlace.py:41-44 espera con el mismo `cmd["id_cmd"]` que publica. |
| CA-3.2.2 | Cumple | `test_ca_3_2_2_timeout_lanza_y_envia_stop` PASSED. pi/enlace.py:45-51: ante `TimeoutError` publica STOP con `_publicar` (no llama a `enviar`, sin recursión), no espera su respuesta, ignora cualquier fallo del STOP y relanza el `TimeoutError` original. Timeout por defecto 1.0 (líneas 13 y 25). |
| CA-3.2.3 | Cumple | `test_ca_3_2_3_drop_publica_mensaje_valido`, `test_ca_3_2_3_move_publica_pwm_y_valida` y `test_ca_3_2_3_id_cmd_unico` PASSED. `id_cmd` = `"CMD-" + uuid4().hex[:12]` (pi/enlace.py:20-21), único entre instancias y reinicios; cabe en `idCmd[48]` del firmware. `move` no invierte signos (línea 57). `drop` publica una sola vez. |
| CA-3.2.6 | Cumple | firmware/.gitignore:1 `esp32/src/secrets.h` (patrón con separador, relativo al directorio del .gitignore). `git log --all -- firmware/esp32/src/secrets.h` no devuelve nada; `git ls-files firmware` solo lista `secrets.example.h`. secrets.example.h:3-5 solo valores de ejemplo. Sin literales de SSID, contraseña ni IP en main.cpp, red_mqtt.*, platformio.ini ni pi/enlace.py. |

## Predicciones frente a lo observado
Sin divergencias, salvo el reenvío de SUP-035 (ver H-1) y la compilación (O-2).
- STOP sin recursión: sale por `_publicar`, solo si el comando no era STOP (enlace.py:48).
- Se conserva un `id_cmd` dado y se generan `id_cmd`/`ts` si faltan, sin mutar el dict del llamador (`dict(cmd)` + `setdefault`, enlace.py:30-31, 40-41).
- STOP válido contra el esquema: `cmd`, `id_cmd` y `ts` entero en ms (contratos/esp32.md:16).
- No hay reenvío: el docstring dice "sin reintentar el comando original" (enlace.py:37-38).
- platformio.ini fija `knolleary/PubSubClient@2.8` y `bblanchon/ArduinoJson@7.2.0` (líneas 7-9); sin cliente ni parser propios.
- QoS según SUP-035: `subscribe(TEMA_CMD, 1)` y testamento QoS 1 retenido (red_mqtt.cpp:103-104); EN_LINEA retenido QoS 0 (108); resp QoS 0 sin retain (main.cpp:78).
- `ts`: NTP y, si no, `millis()`, sin bloquear (red_mqtt.cpp:73-81, `configTime` en 122).
- DROP solo responde DROP_OK, sin tocar 18 y 19 (main.cpp:109-111).
- Paro por 1 s sin comandos o pérdida de red: `vigilante()` (main.cpp:123-126, 140-142).
- `elevacionIniciarPines()` primero en `setup()` (main.cpp:130); sin pines de HC-SR04, encoders, VL53L1X ni HX711.

## Hallazgos
### H-1 [Línea base] SUP-035 y CC-013 dicen que la Pi reenvía con el mismo `id_cmd`; el contrato y CA-3.2.2 dicen que no hay reintento
- **Afecta:** entregable de WP-3.2 (docs/pm/03-wbs.md:173: "la Pi cubre la pérdida con su timeout de 1 s y el reenvío con el mismo `id_cmd`"), SUP-035 (docs/pm/supuestos.md:40) y CC-013 (docs/pm/cambios.md:17), frente a contratos/esp32.md:28 ("No hay reintento del comando: el error se reporta a 1 s") y CA-3.2.2 (TimeoutError a 1 s y STOP).
- **Evidencia:** pi/enlace.py:34-51 sigue el contrato y CA-3.2.2: no reenvía. Ningún otro WP tiene asignado el reenvío; CA-4.3.6 aborta la misión con STOP ante un timeout. La cobertura de la pérdida de `resp` con QoS 0 que CC-013 da por hecha no la entrega ningún WP. Reenviar dentro de `enviar` rompería el "1 s" de CA-3.2.2. El código deja la puerta abierta (conserva un `id_cmd` dado; el firmware tiene caché de idempotencia, main.cpp:89-95).
- **Para cerrarlo:** una aclaración aprobada por `/pm-cambio` que (a) deje escrito que no hay reintento y que una `resp` perdida termina en timeout, STOP y aborto (corregir SUP-035, CC-013 y el entregable), o (b) asigne el reenvío con el mismo `id_cmd` a un WP y criterio concretos, compatibles con el 1 s. Con (a), la implementación actual queda conforme sin cambios.

### O-1 [Observación] CA-3.2.6 se verificó por inspección, no por ejecución
`git check-ignore -v` fue bloqueado por el hook y `secrets.h` no existe en este equipo. Se cierra en WP-6.1 con el `secrets.h` real: `git status --short` limpio y `git check-ignore -v` mostrando `firmware/.gitignore:1`.

### O-2 [Observación] Firmware sin compilar en esta auditoría
PlatformIO no está instalado. La API usada parece coherente con ArduinoJson 7 y con la firma de 8 parámetros de `connect()` de PubSubClient 2.8, pero ningún criterio vigente lo comprueba. Se cierra compilando y probando en banco en WP-6.1 (CA-6.1.5 a 6.1.8).

## Alcance, integridad y regresión
- Alcance: f48c5b7 (it1) toca firmware/.gitignore, main.cpp, red_mqtt.cpp, red_mqtt.h, secrets.example.h y pi/enlace.py; 420b7e4 (it2) toca platformio.ini y red_mqtt.*. Todos dentro del alcance de WP-3.2; ninguno toca `docs/pm/`.
- a356f12 (WP-3.1 it6, dentro de su alcance) solo renombra constantes de pines y un comentario en main.cpp.
- Integridad: `git diff --stat 7831656 HEAD` solo muestra predicciones y evidencia de esta iteración, en `docs/pm/`.
- Regresión: 111 aprobadas, 49 falladas, todas de test_wp_4_1, 4_2 y 4_3 (módulos de WP pendientes). Sin regresión.
- Credenciales: ninguna en el código.

## Hallazgos de iteraciones previas
No hay informes de auditoría previos de WP-3.2: las iteraciones 1 y 2 terminaron en bloqueo y se resolvieron con CC-011, CC-012 y CC-013. Los criterios CA-3.2.4, 3.2.5, 3.2.7 y 3.2.8 pasaron a WP-6.1 por CC-017.
