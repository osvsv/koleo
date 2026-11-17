# Ejecución WP-3.2 — iteración 1
Resultado: LISTO en software (CA-3.2.1, 3.2.2, 3.2.3 y 3.2.6); BLOQUEADO por desviaciones de aprendizaje. CA-3.2.4, 3.2.5, 3.2.7 y 3.2.8 pendientes de hardware. Commit del trabajo: f48c5b7.

Archivos: pi/enlace.py, firmware/.gitignore, firmware/esp32/src/main.cpp, red_mqtt.h, red_mqtt.cpp, secrets.example.h.

## Verificación
- pytest de test_wp_3_2.py (ejecutado desde tests/ por el hook): 6 passed.
- Parser de comandos de host (g++ -Wall -Wextra, prueba interna descartada por estar fuera del alcance): 11.8 y 10.1 dan OVERWEIGHT; 10.0 y 0.1 dan LIFT_OK; peso ausente, string, 0, negativo, NaN, inf, null dan PESO_INVALIDO; mensaje mayor que 512 bytes se descarta completo. No es evidencia por MQTT.
- NO verificado: compilación para ESP32 (PlatformIO no instalado), protocolo MQTT contra el broker.

## Evidencia pendiente de hardware (no creada)
CA-3.2.4 comandos_banco.txt · CA-3.2.5 watchdog.mp4 · CA-3.2.7 peso_invalido.txt · CA-3.2.8 umbral.txt.
Requiere: Mosquitto de la Pi escuchando fuera de 127.0.0.1 (hoy solo en 127.0.0.1), PlatformIO, secrets.h, compilar y flashear una vez por USB.

## Desviaciones
| Archivo o criterio | Categoría | Nota |
| --- | --- | --- |
| firmware/esp32/platformio.ini | aprendizaje | Fuera del alcance y sin lib_deps (ni PubSubClient ni ArduinoJson). El ejecutor escribió un cliente MQTT 3.1.1 mínimo y un parser JSON propios, sin probar contra el broker. |
| `ts` del ESP32 | aprendizaje | El esquema exige ms desde epoch y el ESP32 no tiene reloj; usa NTP (pool.ntp.org) y, sin Internet, ms desde el arranque. El contrato no define la sincronización. |
| DROP | aprendizaje | El contrato solo define el acuse DROP_OK; el firmware responde DROP_OK sin accionar nada físico. |
| docs/pm/evidencia/hw/WP-3.2/LEEME.md | alcance | El hook guard_paths bloqueó la escritura; no existe. |
| tests/internas/test_parser_comando.cpp | alcance | Fuera del alcance; se eliminó. |

Sugerencias del ejecutor: MOVE debe reenviarse desde la Pi con periodo < 1 s (watchdog de 1 s); `pi/enlace.py` solo define la interfaz con un cliente inyectado (el cliente paho real va en el puente, WP-4.1); `reconectar` MQTT puede bloquear hasta 1 s e interferir con `elevacionActualizar()`.
