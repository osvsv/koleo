# Auditoría WP-3.1 — iteración 4
Dictamen: CONFORME CON OBSERVACIONES
Commit: ba9f74b45436b8a9f1e228dc6b5e6476ba314785
Evidencia: docs/pm/evidencia/WP-3.1_it4_aceptacion_ba9f74b.log
Archivos auditados: firmware/esp32/platformio.ini, firmware/esp32/src/elevacion.cpp, firmware/esp32/src/elevacion.h, firmware/esp32/src/main.cpp, firmware/esp32/src/pines.h, firmware/esp32/test/test_elevacion.cpp

Esta iteración corrige H-1 [Mayor] de la it3, que fue una reverificación. Rige la regla de hallazgos congelados: solo se evalúan el cierre de H-1, la regresión y hallazgos nuevos de severidad Mayor. El commit de trabajo es 8642734 [WP-3.1]. ba9f74b [pm] solo agrega docs/pm/auditorias/WP-3.1_it4_ejecucion.md.

Leí elevacion.cpp, elevacion.h, el diff de test_elevacion.cpp y main.cpp, entero a HEAD. No reabrí red_mqtt.*: el commit no lo toca y el corte ya no depende de esa ruta.

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-3.1.1 | Cumple | `git diff 70f90d4..HEAD --stat -- firmware/esp32/src/pines.h firmware/esp32/platformio.ini` sale vacío, así que pines.h no cambió. `elevacionIniciarPines()` sigue haciendo `pinMode(PIN_MD_ENB, OUTPUT)` y `digitalWrite(PIN_MD_ENB, LOW)` (elevacion.cpp:83-84). `setup()` sigue llamándola en primer lugar (main.cpp:130). Lo único nuevo es la creación del temporizador, antes de los `pinMode` (elevacion.cpp:75-80). No toca GPIO 14 y solo añade microsegundos. |
| CA-3.1.2 | Cumple | `evaluarLift` no cambió (elevacion.cpp:26-37). En `elevacionSolicitarEn` el actuador se energiza y el temporizador se arma solo si `c == LIFT_OK` (líneas 100-114). Con PESO_INVALIDO u OVERWEIGHT no se tocan pines ni temporizador. La llamada de main.cpp:100 es la misma que en la it3. Las firmas y los códigos de interfaz se mantienen (elevacion.h:7-12). |
| CA-3.1.6 | Cumple (H-1 cerrado) | **Uso de millis y delay:** `ahoraMs()` usa `millis()` (elevacion.cpp:91) y elevacion.cpp no tiene `delay()`. **Corte independiente:** un `esp_timer` one-shot se arma con `(uint64_t)ELEVACION_MAX_MS * 1000ULL` = 8 000 000 µs (línea 113) en el mismo punto donde se energiza. Su callback `cbCorte` (línea 70) llama a `elevacionCorteTimerEn`, que pone el pin en LOW y marca `g_activa=false` dentro de `portENTER_CRITICAL` (líneas 60-67). Actúa sobre el hardware, no deja una bandera para que la lea loop(). **Respaldo:** `elevacionActualizar()` usa la misma función y el mismo candado, con resta sin signo y `>= 8000UL` (línea 124). **Sin rearme:** un LIFT con la elevación activa deja `inicio=false` y no reinicia ni el límite ni el temporizador (líneas 102-111), así que H-3 sigue cerrado. Detalle en "Predicciones frente a lo observado". |
| CA-3.1.3, 3.1.5 | No aplica | Movidos a WP-3.2 por CC-010. |
| CA-3.1.4, 3.1.7, 3.1.8 | No aplica | Retirados por CC-004. |

## Predicciones frente a lo observado
- **Corte que actúa sobre el hardware, no por bandera.** Coincide. El callback llama a `actuadorSube(false)` directamente (elevacion.cpp:63). El despacho es por tarea de esp_timer, porque `esp_timer_create_args_t a = {}` deja `dispatch_method` en el valor por defecto, ESP_TIMER_TASK. No hay delay, Serial ni MQTT en el callback. Esa tarea corre aparte de loop(), así que los bloqueos de `redActualizar()` de la it3 ya no retrasan el corte.
- **Unidades.** Coincide. La constante está en µs en el código de producción (línea 113), no solo en la prueba.
- **Reloj del callback frente a `g_inicioMs`.** `cbCorte` usa `esp_timer_get_time()/1000` truncado a uint32, y `g_inicioMs` viene de `millis()`. Que esto sea coherente se apoya en que Arduino-ESP32 implementa `millis()` como `esp_timer_get_time()/1000ULL`. No hay framework instalado (`~/.platformio/packages` no existe), así que no pude comprobarlo en este equipo. El temporizador se arma después de capturar `g_inicioMs` y esp_timer no dispara antes de tiempo. Por eso, al disparar, `ahora - g_inicioMs >= 8000` se cumple y el corte se aplica.
- **Callback tardío.** Coincide. Un callback viejo no corta una elevación nueva porque se compara contra el `g_inicioMs` vigente (línea 62). Además, `esp_timer_stop` antes de `start_once` (líneas 112-113) cancela un armado pendiente. El error ESP_ERR_INVALID_STATE se ignora, que es lo tolerable.
- **Concurrencia.** Coincide. `g_activa` y `g_inicioMs` son `volatile` y se escriben dentro de la sección crítica (portMUX). La única escritura en HIGH del actuador está en `elevacionSolicitarEn`, bajo el mismo candado y solo si `!g_activa`. loop() no puede volver a energizar después del corte sin un LIFT nuevo. main.cpp no usa PIN_ACT_RPWM ni PIN_ACT_LPWM, ni con ledc ni con digitalWrite, y DROP no mueve el actuador (main.cpp:109-111).
- **Creación del temporizador. Divergencia.** Predije que se comprobaría el `esp_err_t`. No se comprueba (elevacion.cpp:79), tampoco el de `esp_timer_start_once` (línea 113). Si la creación fallara, `g_timerCorte` quedaría en NULL y el corte dependería solo de loop(), como en la it3. No lo clasifico como Mayor:
  - la única falla realista de `esp_timer_create` con argumentos válidos es ESP_ERR_NO_MEM, al arrancar;
  - la condición de cierre de H-1 se refería a rutas de `loop()`.

  Por la regla de hallazgos congelados no se agrega como observación nueva. Queda anotado aquí.
- **Orden respecto de los pines. Divergencia menor.** La creación del temporizador va antes de los `pinMode`, no después como predije. No tiene efecto sobre CA-3.1.1.
- **Pruebas de host.** Coincide: 7999 no corta, 8000 sí; hay un callback tardío idempotente, un callback viejo que no corta la nueva elevación y la vuelta del reloj uint32 (test_elevacion.cpp, líneas añadidas en 8642734). El diff solo agrega líneas y no quita ni relaja casos de la it1 ni de la it2. **No ejecuté estas pruebas.** Solo tengo permitidos comandos de lectura, los scripts del método y los comandos de config.json (pytest), y el hook bloquea `g++`. La afirmación del ejecutor de que pasaron con g++ -Wall no es evidencia.
- **Compilación para ESP32.** Sin verificar, como predije (H-5).
- **El residuo `10.0)`.** Coincide: el log marca "Árbol limpio: no".

## Hallazgos
No hay hallazgos nuevos. El único que queda abierto es H-5 [Observación], de iteraciones anteriores (ver la última sección).

## Alcance, integridad y regresión
- **Alcance:** 8642734 toca solo firmware/esp32/src/elevacion.cpp, firmware/esp32/src/elevacion.h y firmware/esp32/test/test_elevacion.cpp (`git show --stat`). Los tres están dentro de `firmware/esp32/**`, el Alcance de WP-3.1. No toca main.cpp ni red_mqtt.*, así que no hace falta reverificar WP-3.2 por este commit.
- **Integridad:** 8642734 no modifica nada en docs/pm/. ba9f74b es un commit [pm] separado.
- **Regresión:** el log (commit ba9f74b = HEAD, código de salida 1) da 37 failed y 96 passed, igual que en la it3. Las 37 fallas están todas en test_wp_4_1, test_wp_4_2 y test_wp_4_3, que son WP pendientes cuyos módulos no existen (ModuleNotFoundError/ImportError de pi.puente_mqtt, pi.ordenes, pi.odometria, pi.mapa, pi.mision). No falla ninguna prueba de WP-1.x, 3.2, 4.4 ni 5.x, así que no hay regresión.
- **Credenciales:** no hay ninguna en los archivos tocados.
- **Árbol de trabajo:** "Árbol limpio: no" se debe al residuo `10.0)` en la raíz, ya señalado antes, y a los archivos de evidencia y predicciones de esta iteración, que aún no están commiteados. No afecta al firmware.

## Hallazgos de iteraciones previas: cerrados / persistentes
- **H-1 [Mayor] de la it3 (la red bloquea `loop()` y el actuador puede superar los 8 s): cerrado.** El corte ya no depende de `loop()`. Lo aplica un esp_timer one-shot de 8 000 000 µs que actúa directamente sobre el pin, y queda el corte por `millis()` en loop() como respaldo. La salvedad es que esto se verificó por inspección y no se compiló ni se probó en hardware (H-5).
- **H-3 de la it1 (LIFT repetido reiniciaba el límite): sigue cerrado.** Un LIFT con la elevación activa no reinicia ni el límite ni el temporizador (elevacion.cpp:102-111).
- **H-4 de la it1 (precisión de float en 10 kg): sigue atendido.** `evaluarLift` no cambió.
- **H-1 y H-2 de la it1 (evidencia de banco):** siguen trasladados a WP-3.2 (CA-3.2.7 y CA-3.2.8).
- **H-5 [Observación] (compilación para ESP32 sin verificar): persiste.** El commit agrega dependencias de la API de ESP-IDF (`esp_timer.h`, `portMUX_TYPE`, `portENTER_CRITICAL`) sin compilar para esp32dev. El ejecutor declara que no compiló para ESP32 ni probó en hardware. Se cierra con una compilación `pio run -e esp32dev` registrada en evidencia, y conviene una prueba en banco de que el actuador se corta a los 8 s con la red caída.
- **Nota de la it2 sobre docs/pm/evidencia/hw/WP-3.1/LEEME.md** (menciona CA-3.1.3 y 3.1.5): sigue abierta, solo se lista.
