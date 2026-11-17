# Auditoría WP-3.1 — iteración 3
Dictamen: NO CONFORME
Commit: 8d47f83bbaeface4fdc087b07d71e5c6350f714e
Evidencia: docs/pm/evidencia/WP-3.1_it3_aceptacion_8d47f83.log
Archivos auditados: firmware/esp32/platformio.ini, firmware/esp32/src/elevacion.cpp, firmware/esp32/src/elevacion.h, firmware/esp32/src/main.cpp, firmware/esp32/src/pines.h, firmware/esp32/test/test_elevacion.cpp
Tipo: reverificación

Esta reverificación parte del dictamen vigente, docs/pm/auditorias/WP-3.1_it2.md (CONFORME en 70f90d4). Entre 70f90d4 y HEAD, el único commit que toca archivos auditados es f48c5b7 [WP-3.2], que cambia firmware/esp32/src/main.cpp. Los demás commits son [pm]. `git diff --stat 70f90d4..HEAD` sobre elevacion.cpp, elevacion.h, pines.h, platformio.ini y test/test_elevacion.cpp sale vacío. En WP-3.1 no cambió nada de la WBS: CC-011 y CC-012 solo modifican la entrada de WP-3.2.

Para seguir la cadena de llamadas de main.cpp leí también red_mqtt.cpp y red_mqtt.h (entregables de WP-3.2, fuera de "Archivos auditados").

## Cambios reverificados
| Commit | WP de origen | Efecto sobre WP-3.1 |
| --- | --- | --- |
| f48c5b7 | WP-3.2 (it1) | main.cpp deja de leer por serie y atiende LIFT, MOVE, STOP y DROP por MQTT a través de `redActualizar()`. LIFT sigue entrando por `elevacionSolicitar` (main.cpp:100) y `setup()` sigue llamando a `elevacionIniciarPines()` (main.cpp:130). `loop()` ahora llama a `redActualizar()` (main.cpp:141) antes de `elevacionActualizar()` (main.cpp:143), y `redActualizar()` puede bloquear: ver H-1. |
| 9862af2, d0e9fab, 3d4b687, 6608376, b051914, 1159676, ef9603a (CC-011), cc2ba9d, 3bc66f5 (CC-012), 36e1414, 8d47f83 | [pm] | Solo tocan docs/pm/. No afectan al firmware ni a los criterios de WP-3.1. |

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-3.1.1 | Cumple | pines.h no cambió (`PIN_MD_ENB 14`, pines.h:15). `setup()` llama primero a `elevacionIniciarPines()` (main.cpp:130), que hace `pinMode` y `digitalWrite(PIN_MD_ENB, LOW)` (elevacion.cpp:51-52). Las líneas nuevas de `setup()` (main.cpp:131-135) solo ponen en LOW los pines del motor izquierdo y los IN3/IN4. GPIO 14 solo recibe PWM con un MOVE (`pwmPrepara`/`ruedas`), lo cual es legítimo para el ENB de tracción. |
| CA-3.1.2 | Cumple | main.cpp:100 llama a `elevacionSolicitar(c.peso[0] ? c.peso : NULL)`, y elevacion.cpp no cambió. Todos los casos del encargo dan PESO_INVALIDO, y nunca 0 kg aceptado: **(1)** `peso_kg` ausente: `memset` deja `peso[0]==0`, se pasa NULL (red_mqtt.cpp:41) y elevacion.cpp:18 lo rechaza. **(2)** `peso_kg` como string JSON: red_mqtt.cpp:67 vacía `peso`. **(3)** No numérico (`NaN`, `Infinity`, `null`, `true`): el filtro de caracteres de red_mqtt.cpp:32-37 lo deja vacío (línea 82). **(4)** `0`, `-1`, `1e999`: pasan el filtro y los rechazan `!isfinite(v) \|\| v <= 0.0` (elevacion.cpp:23) y `strtod` con `endptr` (`5e`, `--5`). **(5)** Token de 32 caracteres o más: `largo` lo deja vacío. Un mensaje mayor que el buffer se descarta completo (red_mqtt.cpp:264-278, `len > RED_RX_MAX`) y nunca se procesa un prefijo, con lo que queda atendida la observación de la it2. El JSON inválido o anidado se descarta sin energizar. Si `id_cmd` está repetido no se vuelve a llamar a `elevacionSolicitar`; solo se reenvía la respuesta (main.cpp:88-93). La respuesta es `ERR`/`PESO_INVALIDO`. |
| CA-3.1.6 | No cumple (efecto de f48c5b7) | elevacion.cpp no cambió: usa `millis()`, no tiene `delay()`, compara `>= 8000UL` (elevacion.cpp:77-82) y un LIFT con la elevación activa no reinicia el límite (línea 67). Pero el corte solo se aplica cuando `loop()` llega a `elevacionActualizar()` (main.cpp:143), y antes `redActualizar()` (main.cpp:141) puede bloquear del orden de 1-2 s, con `delay(1)` en un ciclo de espera. Con la elevación activa y el enlace caído, el actuador puede quedar energizado más de 8 s. Ver H-1. |
| CA-3.1.3, 3.1.5 | No aplica | Movidos a WP-3.2 (CC-010). |
| CA-3.1.4, 3.1.7, 3.1.8 | No aplica | Retirados (CC-004). |

## Hallazgos
### H-1 [Mayor] La red MQTT bloquea `loop()` y el actuador puede superar los 8 s (lo introdujo f48c5b7, de WP-3.2)
- **Criterio o requisito afectado:** CA-3.1.6 ("el actuador tiene un tiempo máximo de 8 s", "no `delay()` bloqueante").
- **Evidencia:**
  - main.cpp:139-144: `loop()` ejecuta `vigilante(); redActualizar(); vigilante(); elevacionActualizar();`. El paro de tracción se vigila antes y después de la red; el corte de la elevación solo después.
  - Ruta de reconexión, `redActualizar` → `conectarMqtt`:
    - `g_cli.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 1000)` (red_mqtt.cpp:208) puede tardar hasta 1 s si la Pi no responde.
    - Después, `leerBytes(ack, 4, 1000)` (línea 230) espera hasta 1 s más por el CONNACK con `delay(1)` en el ciclo (líneas 142-153).
    - Los reintentos van cada 2 s y se miden desde el inicio del intento anterior (líneas 317-319). Así, en cuanto termina un intento de unos 2 s puede empezar otro. Entre intentos, `elevacionActualizar()` corre una vez por vuelta.
  - Ruta con enlace activo: `atenderPaquete` encadena esperas de 200 + hasta 4×200 + 300 ms (líneas 252-279) antes de `caer()`.
  - Un escenario concreto: LIFT válido en t=0, el broker deja de responder en t≈3 s, el enlace se da por caído por falta de RX (5 s) y empieza un intento de reconexión que bloquea alrededor de 2 s. Si el intento empieza poco antes de t=8 s, el corte se aplica cerca de t=10 s. El mismo ejecutor lo reconoce en el comentario de red_mqtt.h:31 ("no bloquea mas de ~1 s"), y el dato de 1 s solo cubre `connect`.
  - Antes de f48c5b7, `loop()` solo hacía lecturas no bloqueantes de `Serial`, y el criterio se cumplía.
- **Qué tendría que ser cierto para cerrarlo:** que ninguna ruta de `loop()` pueda retrasar el corte del actuador más allá de 8 s desde el inicio de la elevación. Opciones:
  - un corte independiente de `loop()` (por ejemplo, un temporizador one-shot de `esp_timer` en elevacion.cpp);
  - llamar a `elevacionActualizar()` dentro de las esperas de red (`leerBytes` y la conexión);
  - o una red no bloqueante.

  Si la corrección se hace en main.cpp o en red_mqtt.cpp, le corresponde a WP-3.2. Por CC-011, ese WP va a rehacer el cliente con PubSubClient y ArduinoJson. `PubSubClient::connect` también bloquea, así que el riesgo seguirá ahí si no se trata explícitamente. Si se hace en elevacion.cpp, le corresponde a WP-3.1, porque el archivo está en su Alcance.

## Alcance, integridad y regresión
- **Alcance:** f48c5b7 toca main.cpp, red_mqtt.*, secrets.example.h, firmware/.gitignore y pi/enlace.py, todos dentro del Alcance de WP-3.2. El commit no modifica ningún archivo de docs/pm/. No tocó ningún archivo de prueba, así que test_elevacion.cpp no se debilitó.
- **Credenciales:** no hay ninguna en el código. secrets.example.h solo trae marcadores ("tu_red_wifi", "tu_contrasena"). secrets.h está en firmware/.gitignore y no está versionado (`git ls-files firmware`).
- **Regresión:**
  - El log (commit 8d47f83 = HEAD, código de salida 1) da 37 failed y 96 passed. En la it2 eran 43 failed y 90 passed.
  - Las 6 pruebas de test_wp_3_2 que fallaban ahora pasan.
  - Las 37 fallas están todas en test_wp_4_1, test_wp_4_2 y test_wp_4_3, WP pendientes cuyos módulos aún no existen (ImportError/ModuleNotFoundError). Son las mismas 37 de la it2.
  - No falla ninguna prueba de WP-1.x, 3.2, 4.4 ni 5.x, así que no hay regresión.
- **Árbol de trabajo:** el log marca "Árbol limpio: no" por el residuo `10.0)` en la raíz, ya señalado en la it2, y por el propio log y el .json de evidencia, que aún no están commiteados. Ninguno afecta al firmware.

## Hallazgos de iteraciones previas: cerrados / persistentes
- H-1 y H-2 de la it1 (evidencia de banco): siguen trasladados a WP-3.2 (CA-3.2.7 y CA-3.2.8).
- H-3 (LIFT con la elevación activa reiniciaba el límite): sigue cerrado. elevacion.cpp:67 no cambió y main.cpp no tiene otra vía para reiniciarlo.
- H-4 (precisión de float en el límite de 10 kg): sigue atendida. El archivo no cambió.
- H-5 [Observación], compilación para ESP32 sin verificar: sigue abierta y se agrava. f48c5b7 se declara "sin compilar para ESP32", y el código depende de macros de `ESP_ARDUINO_VERSION_MAJOR` y de la API ledc según la versión del core.
- Observación de la it2 sobre la línea serie truncada procesada como prefijo: **cerrada por el cambio**. La vía serie desapareció, y la vía MQTT descarta completo el mensaje que excede el buffer (red_mqtt.cpp:264-278).
- La nota de la it2 sobre LEEME.md (docs/pm/evidencia/hw/WP-3.1/LEEME.md, que menciona CA-3.1.3 y CA-3.1.5) queda solo listada, no repetida: el diff no la afecta.
