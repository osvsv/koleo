# Ejecución WP-3.2 — iteración 2
Resultado: BLOQUEADO (parcial): código listo y compilado; una desviación de aprendizaje (QoS) y evidencia de hardware pendiente. Commit del trabajo: ver `git log -1 --grep "WP-3.2] it2"`.

## Cambios (CC-011, CC-012)
- firmware/esp32/platformio.ini: conserva env esp32dev, platform, board, framework y monitor_speed; añade `lib_deps` con `knolleary/PubSubClient@2.8` y `bblanchon/ArduinoJson@7.2.0` (fijadas) y `build_flags` `-DARDUINOJSON_ENABLE_NAN=1` y `-DARDUINOJSON_ENABLE_INFINITY=1` (NaN e inf se deserializan y dan PESO_INVALIDO en vez de descartar el comando).
- firmware/esp32/src/red_mqtt.cpp y red_mqtt.h: reescritos sobre PubSubClient y ArduinoJson; se quitaron el cliente MQTT y el parser propios. Mantiene los nombres de la API y añade `RED_BUFFER_MQTT`.
  - `peso_kg` solo cuenta si es número finito; string, objeto, NaN o inf dejan el peso vacío (→ PESO_INVALIDO). `id_cmd` y `cmd` deben ser texto no vacío que quepa.
  - Testamento FUERA_DE_LINEA (QoS 1, retenido) y EN_LINEA retenido en `esp32/conexion`; suscripción a `esp32/cmd` con QoS 1; keepalive de 6 s.
  - `setBufferSize(768)` y descarte completo de mensajes de 512 bytes o más (nunca se procesa un prefijo).
  - `redTsMs()`: NTP si hay hora sincronizada y, si no, `millis()` (SUP-033). Sin `delay()`; un reintento de conexión bloquea como máximo ~1 a 2 s.
- No se tocaron main.cpp, elevacion.*, firmware/esp32/test/, pi/enlace.py, .gitignore ni secrets.example.h. `elevacionIniciarPines()` sigue primero en `setup()`; DROP solo acusa `DROP_OK` (SUP-034).

## Verificación (resultados reales del ejecutor)
- pytest de test_wp_3_2.py (desde tests/, por el hook): 6 passed.
- Compilación en la Pi (`pio run -e esp32dev` sobre una copia en /tmp con un secrets.h de prueba, borrada después): SUCCESS en 414.89 s; RAM 14.8 % (48628 de 327680 bytes), Flash 70.8 % (927365 de 1310720 bytes); versiones fijadas resueltas. Solo compilación: no se ejecutó en un ESP32 ni contra el broker.

## Evidencia pendiente de hardware (no creada)
CA-3.2.4 comandos_banco.txt · CA-3.2.5 watchdog.mp4 · CA-3.2.7 peso_invalido.txt · CA-3.2.8 umbral.txt.

## Procedimiento sugerido por el ejecutor para capturarla
(El hook guard_paths le impidió escribir docs/pm/evidencia/hw/WP-3.2/LEEME.md; queda aquí.)
- Preparación: copiar `secrets.example.h` a `secrets.h` con los valores reales y `MQTT_BROKER_HOST` = `192.168.137.239`; flashear una sola vez con `pio run -e esp32dev -t upload`. En la Pi, dos terminales: `mosquitto_sub -h localhost -v -F '%I %t %r %p' -t 'koleo/robot1/esp32/#' | tee captura.txt` y `mosquitto_pub -h localhost -q 1 -t koleo/robot1/esp32/cmd -m '<json>'` con un `id_cmd` distinto cada vez.
- CA-3.2.4 (comandos_banco.txt): reiniciar el ESP32 y ver `EN_LINEA` retenido; cortarle la alimentación ~10 s y ver `FUERA_DE_LINEA`; enviar LIFT con peso_kg 8.45, MOVE con pwm 80/80, STOP y DROP con x_cm 150 y y_cm 120, y esperar LIFT_OK, MOVE_OK, STOP_OK y DROP_OK.
- CA-3.2.5 (watchdog.mp4), con las ruedas en el aire: un solo MOVE y silencio (debe parar a poco más de 1 s); MOVE cada 0,5 s y apagar el Wi-Fi; MOVE cada 0,5 s y `sudo systemctl stop mosquitto`.
- CA-3.2.7 (peso_invalido.txt): LIFT sin peso_kg debe dar PESO_INVALIDO en esp32/resp con el actuador sin energizar; opcionalmente repetir con "8", 0 y -1.
- CA-3.2.8 (umbral.txt): LIFT con 11.8 y 10.1 debe dar OVERWEIGHT; con 10.0 y 0.1, LIFT_OK. Dejar más de 8 s entre LIFT aceptados.

## Desviaciones
| Archivo o criterio | Categoría | Nota |
| --- | --- | --- |
| CA-3.2.4, contratos/esp32.md (QoS de resp y conexion) | aprendizaje | PubSubClient 2.8 solo publica con QoS 0: `resp` y `EN_LINEA` salen con QoS 0 aunque el contrato dice QoS 1; el testamento sí usa QoS 1 retenido y la suscripción a `cmd` usa QoS 1 con PUBACK automático. El parámetro `qos` de `redPublicar` se ignora. Requiere solicitud de cambio: relajar el contrato a QoS 0 para el ESP32 o usar otra librería. |
| docs/pm/evidencia/hw/WP-3.2/LEEME.md | alcance | El hook guard_paths bloquea escribir en docs/pm/; el procedimiento queda en este informe. |

Efecto en otros WP: platformio.ini es archivo auditado de WP-3.1, que vuelve a "Requiere reverificación". Se borraron tres archivos vacíos sin rastrear de la raíz (`10.0)`, `Project`, `RED_RX_MAX)`), residuos de redirecciones de shell.
