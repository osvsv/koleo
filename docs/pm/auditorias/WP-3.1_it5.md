# Auditoría WP-3.1 — iteración 5
Dictamen: CONFORME CON OBSERVACIONES
Commit: 19e4177a63fb9c07c881eb46cd0ac090ddc03975
Evidencia: docs/pm/evidencia/WP-3.1_it5_aceptacion_19e4177.log
Archivos auditados: firmware/esp32/platformio.ini, firmware/esp32/src/elevacion.cpp, firmware/esp32/src/elevacion.h, firmware/esp32/src/main.cpp, firmware/esp32/src/pines.h, firmware/esp32/test/test_elevacion.cpp
Tipo: reverificación

Esta es una reverificación del dictamen de la it4 (CONFORME CON OBSERVACIONES en ba9f74b). El ejecutor de WP-3.1 no hizo trabajo nuevo. Revisé el diff `ba9f74b..HEAD` de `firmware/esp32/`. El único archivo auditado que cambió es platformio.ini, en el commit 420b7e4 [WP-3.2]. Como pediste, también leí red_mqtt.cpp y red_mqtt.h tal como están en HEAD, porque están en la cadena de llamadas de main.cpp. No reabro nada de lo que ya estaba antes del diff.

## Cambios reverificados
| Commit | WP de origen | Archivos | Efecto sobre WP-3.1 |
| --- | --- | --- | --- |
| 420b7e4 | WP-3.2 it2 | firmware/esp32/platformio.ini (+8, -0) | Solo agrega `lib_deps` con versiones fijadas (PubSubClient@2.8, ArduinoJson@7.2.0) y `build_flags` (-DARDUINOJSON_ENABLE_NAN=1, -DARDUINOJSON_ENABLE_INFINITY=1). Siguen intactos `[env:esp32dev]`, `platform = espressif32`, `board = esp32dev`, `framework = arduino` y `monitor_speed = 115200` (platformio.ini:1-5). Los flags solo actúan en ArduinoJson, que únicamente usa red_mqtt.cpp. |
| 420b7e4 | WP-3.2 it2 | firmware/esp32/src/red_mqtt.cpp, red_mqtt.h | No son archivos auditados de WP-3.1. Los revisé solo por su efecto en CA-3.1.2 (peso que llega a `elevacionSolicitar`) y en CA-3.1.6 (bloqueos en `loop()`). No hay efecto adverso (ver la tabla siguiente). |
| 0c717a8, 2da9a61, 1b1b04c, dbdb95e, 19e4177 | [pm] | docs/pm/ | No tocan firmware/esp32/. |

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-3.1.1 | Cumple | `git diff --stat ba9f74b..HEAD -- firmware/esp32/` solo lista platformio.ini, red_mqtt.cpp y red_mqtt.h, así que pines.h, elevacion.* y main.cpp no cambiaron. `setup()` sigue llamando primero a `elevacionIniciarPines()`, justo después de `Serial.begin` (main.cpp:130). Esa función deja GPIO 14 en LOW (elevacion.cpp:83-84). |
| CA-3.1.2 | Cumple | `evaluarLift` no cambió (elevacion.cpp:26-37) y rechaza NULL o vacío, valores no numéricos, no finitos y ≤ 0 con PESO_INVALIDO. Con los flags nuevos, ArduinoJson acepta los tokens `NaN` e `Infinity` en vez de fallar la deserialización. El parser solo llena `out.peso` si `p.is<double>()` y `isfinite(d)` (red_mqtt.cpp:32-36). NaN, ±inf, strings, objetos y valores ausentes dejan `peso` vacío, porque `memset` va primero (línea 20). main.cpp:100 pasa NULL cuando `peso[0]==0`, y eso da PESO_INVALIDO (elevacion.cpp:27). Los flags no debilitan el criterio: un peso no finito nunca llega como número. Antes del cambio, el comando con NaN se descartaba sin responder. Ahora recibe ERR/PESO_INVALIDO. En ningún caso vale 0 kg. Caso límite: un número finito que `%.9g` imprime como subnormal o 0 vuelve a pasar por `strtod` y por `pesoValido` y da PESO_INVALIDO (elevacion.cpp:32,35). El buffer `peso[32]` cabe la salida de `%.9g` (red_mqtt.h:18). |
| CA-3.1.6 | Cumple (H-1 de la it3 sigue cerrado) | elevacion.cpp no cambió. El corte sigue en un `esp_timer` one-shot armado a `(uint64_t)ELEVACION_MAX_MS * 1000ULL` = 8 000 000 µs (elevacion.cpp:113), con callback `cbCorte` → `elevacionCorteTimerEn`, que actúa sobre el pin (líneas 60-70). Eso no depende de `loop()`. En la red nueva, `redActualizar()` ya no tiene bucles de espera propios. Lo más que puede bloquear es un reintento de `conectarMqtt()` cada 2 s, con `setTimeout(1000)` y `setSocketTimeout(1)` (red_mqtt.cpp:113-117, 128-141). Aunque bloqueara más, no retrasaría el corte. `grep "delay\s*\("` sobre firmware/esp32 no encuentra nada: no hay `delay()` nuevo. `loop()` sigue igual (main.cpp:139-144). |
| CA-3.1.3, 3.1.5 | No aplica | Movidos a WP-3.2 por CC-010. |
| CA-3.1.4, 3.1.7, 3.1.8 | No aplica | Retirados por CC-004. |

## Hallazgos
El diff no genera hallazgos nuevos.

## Alcance, integridad y regresión
- **Alcance:** el único cambio en un archivo auditado viene de 420b7e4, un commit de WP-3.2 que toca platformio.ini para añadir dependencias de su propio entregable. No toca elevacion.*, pines.h, main.cpp ni firmware/esp32/test/. Por eso test_elevacion.cpp no tiene casos quitados ni relajados.
- **Integridad:** 420b7e4 no modifica docs/pm/ (`git show --stat 420b7e4` solo muestra los tres archivos de firmware).
- **Regresión:** el log tiene `Commit: 19e4177a63fb…` (= HEAD), "Árbol limpio: sí" y código de salida 1. El resultado es 37 failed y 96 passed, el mismo que en la it3 y la it4. Las 37 fallas están en tests/aceptacion/test_wp_4_1.py, test_wp_4_2.py y test_wp_4_3.py (log:655-691), y fallan por `ModuleNotFoundError`/`ImportError` de módulos de WP pendientes (p. ej. `pi.puente_mqtt`, log:35-36). Ninguna prueba de otro WP que antes pasaba falla ahora, así que no hay regresión.
- **Credenciales:** no hay ninguna en el código. red_mqtt.cpp toma `WIFI_SSID`/`WIFI_PASSWORD` de `secrets.h` (línea 63, 121). Ese archivo no está versionado: `git ls-files firmware/esp32` no lo lista y firmware/.gitignore:1 lo ignora. secrets.example.h solo tiene valores de ejemplo ("tu_red_wifi", "tu_contrasena"). platformio.ini no tiene credenciales.
- **Compilación:** no pude verificarla. Con los comandos que tengo permitidos no tengo acceso a la Pi ni a una toolchain local, y en docs/pm/evidencia/ no hay ningún log de `pio run -e esp32dev` (grep de "esp32dev|SUCCESS" sin resultados). La afirmación del ejecutor de WP-3.2 en docs/pm/auditorias/WP-3.2_it2_ejecucion.md no es evidencia de esta auditoría.

## Hallazgos de iteraciones previas: cerrados / persistentes
- **H-1 [Mayor] de la it3 (la red bloquea `loop()` y el actuador puede pasar de 8 s): sigue cerrado.** La reescritura de red_mqtt.* no cambia el mecanismo de corte por esp_timer.
- **H-3 de la it1 (LIFT repetido reiniciaba el límite): sigue cerrado.** elevacion.cpp:100-111 no cambió.
- **H-4 de la it1 (precisión de float en 10 kg): sigue atendido.** `evaluarLift` no cambió.
- **H-1 y H-2 de la it1 (evidencia de banco):** siguen trasladados a WP-3.2 (CA-3.2.7 y CA-3.2.8).
- **H-5 [Observación] (compilación para ESP32 sin verificar): persiste.** Se cierra con un log de `pio run -e esp32dev` registrado en docs/pm/evidencia/, idealmente generado en el commit vigente. Conviene además una prueba en banco del corte a 8 s con la red caída.
- **Nota de la it2 sobre docs/pm/evidencia/hw/WP-3.1/LEEME.md** (menciona CA-3.1.3 y 3.1.5): sigue abierta, solo se lista.
