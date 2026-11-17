# Auditoría WP-3.1 — iteración 1
Dictamen: NO CONFORME
Commit: e341bae0fc2072be2fcfcb38031156b647484068
Evidencia: docs/pm/evidencia/WP-3.1_it1_aceptacion_e341bae.log
Archivos auditados: firmware/esp32/platformio.ini, firmware/esp32/src/elevacion.cpp, firmware/esp32/src/elevacion.h, firmware/esp32/src/main.cpp, firmware/esp32/src/pines.h, firmware/esp32/test/test_elevacion.cpp

Nota: el trabajo está en 609ed17. `git diff --stat 609ed17 HEAD -- firmware` sale vacío, así que el firmware auditado en HEAD (e341bae) es idéntico al del commit del WP.

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-3.1.1 | Cumple | Se comparó firmware/esp32/src/pines.h:6-31 con importado/KOLEO_todo.md §9 (líneas 264-282). Coinciden: RPWM/LPWM 25/26; ENA/IN1/IN2 32/33/27; ENB/IN3/IN4 14/23/13 (IN3 en GPIO 23); encoders A/B 34/36 y 35/39 (canal B en 36/39); TRIG/ECHO 18/19; RX2/TX2 16/17. No aparecen HX711 (4/5) ni VL53L1X (21/22). GPIO 14 en LOW: elevacion.cpp:50-51 (`digitalWrite(PIN_MD_ENB, LOW)`), llamado desde `setup()` en main.cpp:9. |
| CA-3.1.2 | Cumple | elevacion.cpp:18: NULL o vacío dan PESO_INVALIDO. Líneas 19-22: `strtod` con `endptr` y rechazo de lo que sobra, así que "abc" y "5x" no pasan. Línea 24: `pesoValido` usa `isfinite(kg) && kg > 0` (línea 14), lo que deja fuera 0, negativos, NaN e inf. main.cpp:20: `LIFT` sin argumento pasa NULL. No hay ningún camino en que la ausencia de peso valga 0 kg. Las firmas de la Interfaz coinciden (elevacion.h:10,12). |
| CA-3.1.3 | No cumple | La evidencia que exige el diccionario, docs/pm/evidencia/hw/WP-3.1/peso_invalido.txt, no existe. Solo hay LEEME.md. El ejecutor lo reconoce en WP-3.1_it1_ejecucion.md:10. |
| CA-3.1.5 | No cumple (evidencia) | docs/pm/evidencia/hw/WP-3.1/umbral.txt no existe. El código es correcto (`kg > PESO_LIMITE_KG` con 10.0f, elevacion.cpp:15; 10.0 se acepta, 10.1 y 11.8 dan OVERWEIGHT, 0.1 se acepta), pero el criterio exige evidencia de banco. |
| CA-3.1.6 | Cumple, frágil | Usa `millis()` (elevacion.cpp:58) y no hay ningún `delay()` en src/. La parada por tiempo no bloquea: está en `elevacionActualizarEn` (líneas 74-79), con `ELEVACION_MAX_MS 8000UL` (elevacion.h:5), y apaga el pin. Ver H-3: un LIFT nuevo reinicia el contador. |
| CA-3.1.4, 3.1.7, 3.1.8 | No aplica | Retirados por CC-004. |

## Predicciones frente a lo observado
- CA-3.1.1: se predijo que GPIO 14 en bajo tenía que estar en `setup()`. Se cumple a través de `elevacionIniciarPines()`. No hay divergencia.
- CA-3.1.2: los riesgos predichos eran valor por defecto 0, `strtof` sin `endptr` y falta de `isfinite`. Ninguno se materializó. El caso de `peso_kg` como string JSON corresponde al parseo MQTT de WP-3.2 y no se evalúa aquí.
- CA-3.1.3 y CA-3.1.5: se predijo que no cumplirían en it1 por falta de evidencia de banco. Confirmado.
- CA-3.1.6: se predijo el riesgo de que un "LIFT nuevo reinicie el contador". Se materializó: es H-3.
- Interfaz: firmas exactas, códigos literales `LIFT_OK`/`OVERWEIGHT`/`PESO_INVALIDO` (elevacion.cpp:29-35) y nada de Wi-Fi ni MQTT. Coincide.
- Compilación para ESP32 sin verificar: confirmado (informe de ejecución, línea 12). Ver H-5.

## Hallazgos
### H-1 [Mayor] Falta la evidencia de banco de CA-3.1.3
- Criterio o requisito afectado: CA-3.1.3; REQ-F-003 (verificación "Inspección de código y evidencia física"); RK-03.
- Evidencia: en docs/pm/evidencia/hw/WP-3.1/ solo está LEEME.md. peso_invalido.txt no existe.
- Qué tendría que ser cierto para cerrarlo: que exista peso_invalido.txt con la salida serie real del ESP32 ante `LIFT` sin peso, que muestre `PESO_INVALIDO`, y una constancia (medición o registro) de que el actuador no se energizó. Debe estar firmada o fechada por la persona que hizo la prueba.

### H-2 [Mayor] Falta la evidencia de banco de CA-3.1.5
- Criterio o requisito afectado: CA-3.1.5; REQ-F-001, REQ-F-002, REQ-NF-009, SUP-010.
- Evidencia: docs/pm/evidencia/hw/WP-3.1/umbral.txt no existe.
- Qué tendría que ser cierto para cerrarlo: que exista umbral.txt con la salida serie real de `LIFT 11.8` y `LIFT 10.1` (OVERWEIGHT) y de `LIFT 10.0` y `LIFT 0.1` (LIFT_OK).

### H-3 [Menor] Un LIFT válido durante una elevación activa reinicia el límite de 8 s
- Criterio o requisito afectado: CA-3.1.6 ("el actuador tiene un tiempo máximo de 8 s").
- Evidencia: elevacion.cpp:64-70. `elevacionSolicitar` pone `g_inicioMs = ahoraMs()` con cada LIFT_OK aunque `g_activa` ya sea verdadero. Si llegan LIFT válidos antes de cumplirse 8 s (por ejemplo, reenvíos QoS 1 desde WP-3.2 o repeticiones por el monitor serie), el actuador sigue energizado sin interrupción más de 8 s. La prueba interna (test_elevacion.cpp:17-19) no cubre este caso.
- Qué tendría que ser cierto para cerrarlo: que ninguna secuencia de comandos mantenga el actuador energizado de forma continua más de 8 s. Por ejemplo, que un LIFT recibido con la elevación activa no reinicie `g_inicioMs` (o se rechace), y que una prueba lo demuestre.

### H-4 [Observación] La precisión de `float` acepta valores apenas por encima de 10.0
- Criterio o requisito afectado: CA-3.1.5 (no lo incumple con los valores del criterio).
- Evidencia: elevacion.cpp:20-25. Se lee en `double` y luego se convierte a `float`, así que "10.0000001" se vuelve 10.0f y se acepta. Comparar el `double` contra 10.0 evitaría el redondeo. Con pesos registrados con 2 decimales no tiene efecto práctico.

### H-5 [Observación] La compilación para ESP32 y la semántica de LIFT_OK no están verificadas
- Evidencia: la compilación con PlatformIO no se ha hecho (WP-3.1_it1_ejecucion.md:12). La evidencia de banco de H-1 y H-2 la demostrará de hecho. Además, main.cpp:21 imprime `LIFT_OK` al empezar a subir, mientras que contratos/esp32.md:20 describe `LIFT_OK` como "tarima elevada". Conviene alinear ese momento cuando WP-3.2 arme la respuesta MQTT. La línea `linea` (main.cpp:5,15) crece sin límite si nunca llega un '\n'.

## Alcance, integridad y regresión
- Alcance: 609ed17 toca solo firmware/esp32/** (6 archivos), dentro del Alcance del WP. d17df56 ([pm]) agrega docs/pm/auditorias/WP-3.1_it1_ejecucion.md y docs/pm/evidencia/hw/WP-3.1/LEEME.md. LEEME.md también está en el Alcance (docs/pm/evidencia/hw/WP-3.1/**), así que la desviación que declara el ejecutor no hace falta registrarla en desviaciones.md.
- Integridad: el commit del WP (609ed17) no modifica nada en docs/pm/.
- Regresión: el log (commit e341bae = HEAD, código de salida 1) da 43 failed y 90 passed. Las 43 fallas son de test_wp_3_2, test_wp_4_1, test_wp_4_2 y test_wp_4_3, todos WP Pendientes, por módulos que no existen (`pi.enlace`, `pi.puente_mqtt`, `pi.ordenes`, `pi.odometria`, `pi.mapa`, `pi.mision`). El log anterior (WP-1.3_it6_aceptacion_7528a91.log) también da 43 failed y 90 passed. No falla ninguna prueba de WP-1.1, 1.2, 1.3, 4.4, 5.1 ni 5.2, así que no hay regresión. El log marca "Árbol limpio: no" por estado.md y archivos de docs/pm sin commit. Ninguno afecta a firmware ni a tests.
- Credenciales: no hay ninguna en el firmware. No hay Wi-Fi ni MQTT, que corresponden a WP-3.2.
- Ningún criterio de WP-3.1 apunta a tests/aceptacion. test/test_elevacion.cpp es una prueba interna. No la ejecuté (g++ no está entre los comandos permitidos) y no la cuento como evidencia.

## Hallazgos de iteraciones previas: cerrados / persistentes
No aplica (iteración 1).
