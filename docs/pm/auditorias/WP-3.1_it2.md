# Auditoría WP-3.1 — iteración 2
Dictamen: CONFORME
Commit: 9862af2b36d59995a08698a429b131ef4dbb64db
Evidencia: docs/pm/evidencia/WP-3.1_it2_aceptacion_70f90d4.log
Archivos auditados: firmware/esp32/platformio.ini, firmware/esp32/src/elevacion.cpp, firmware/esp32/src/elevacion.h, firmware/esp32/src/main.cpp, firmware/esp32/src/pines.h, firmware/esp32/test/test_elevacion.cpp

Nota: el trabajo está en cfb927f. Los commits posteriores (70f90d4, 9862af2) son solo [pm]. `git diff --stat 70f90d4 HEAD -- firmware tests` sale vacío, así que el log generado en 70f90d4 corresponde al firmware y a las pruebas de HEAD. Dejo en "Archivos auditados" los mismos seis archivos de la it1, porque siguen siendo el entregable del WP. pines.h y platformio.ini no cambiaron desde e341bae (`git diff --stat e341bae HEAD -- firmware` solo lista los 4 archivos del commit cfb927f).

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-3.1.1 | Cumple | pines.h no cambió desde la it1, en la que se verificó contra KOLEO_todo.md §9. `elevacionIniciarPines()` sigue en `setup()` (main.cpp:9) y pone GPIO 14 en LOW (elevacion.cpp:51-52). |
| CA-3.1.2 | Cumple | elevacion.cpp:18: NULL o vacío dan PESO_INVALIDO. Líneas 19-22: `strtod` con `endptr`, así que "abc" y "5x" quedan rechazados. Línea 23: `!isfinite(v) \|\| v <= 0.0` deja fuera 0, -0, negativos, NaN e inf ya en double. Línea 26: un subdesbordamiento a 0.0f en float (por ejemplo "1e-50") también da PESO_INVALIDO. main.cpp:20: `LIFT` sin argumento pasa NULL. No hay ningún camino en que la ausencia de peso valga 0 kg aceptable. Las firmas de la Interfaz (`pesoValido(float)`, `excedeLimite(float)`) no cambiaron (elevacion.h:10,12). |
| CA-3.1.3 | No aplica | Movido a WP-3.2 como CA-3.2.7 por CC-010. |
| CA-3.1.5 | No aplica | Movido a WP-3.2 como CA-3.2.8 por CC-010. |
| CA-3.1.6 | Cumple | Usa `millis()` (elevacion.cpp:59). Ni src/ ni la Grep de `delay` muestran ningún `delay()`; la única coincidencia es un comentario en elevacion.h:21. El apagado no bloquea: está en `elevacionActualizarEn` (líneas 77-82), compara `(uint32_t)(ahora - g_inicioMs) >= 8000UL`, pone el pin en LOW y `g_activa=false`. Un LIFT válido con la elevación activa ya no reasigna `g_inicioMs` (línea 67: `c == LIFT_OK && !g_activa`). La prueba interna test_elevacion.cpp:21-24 lo cubre: LIFT en 1000, LIFT en 5000, sigue activo en 8999 y se apaga en 9000. |
| CA-3.1.4, 3.1.7, 3.1.8 | No aplica | Retirados por CC-004. |

## Predicciones frente a lo observado
- CA-3.1.1: se predijo el riesgo de perder o reordenar `elevacionIniciarPines()` al tocar main.cpp. El cambio en main.cpp es una sola línea (main.cpp:15) y `setup()` sigue igual. No hay divergencia.
- CA-3.1.2, cambio a double: no se cambiaron las firmas de la Interfaz. `isfinite` y `> 0` se aplican en double, y además se revalida en float. Las incoherencias predichas no se materializan: "1e-50" da PESO_INVALIDO (no 0 kg aceptado) y "1e40" da OVERWEIGHT, que es lo coherente para un número finito mayor que 10. El '\r' pegado lo resuelven `trim()` (main.cpp:16,19) y el salto de blancos (elevacion.cpp:21).
- CA-3.1.2, buffer acotado: el riesgo predicho se materializa en parte. Con más de 64 caracteres, main.cpp:15 descarta los caracteres sobrantes y procesa el prefijo. Una línea como "LIFT 5" seguida de más de 58 espacios y una basura final se truncaría antes de la basura y daría LIFT_OK. Por la regla de hallazgos congelados no lo registro como hallazgo. Una divergencia solo podría entrar en esta iteración como hallazgo nuevo Mayor, y esta no lo es: la vía serie es solo de depuración según la Interfaz, CC-010 elimina el uso del ESP32 por USB en operación y los valores que el criterio enumera (ausente, no numérico, 0, negativo) se siguen rechazando. Conviene tenerlo presente en WP-3.2 al parsear el payload MQTT.
- CA-3.1.6: todo lo predicho se observa. No se reasigna `g_inicioMs`, la comparación es unsigned y segura ante el desbordamiento de `millis()`, el apagado pone el pin en LOW y `g_activa` en falso, no hay `delay()` nuevo y existe la prueba de LIFT en dos instantes.
- Interfaz: un LIFT válido con la elevación activa responde `LIFT_OK` (elevacion.cpp:66-72) y no hay códigos nuevos. `elevacionSolicitarEn` es una función auxiliar añadida que no altera las firmas declaradas. No hay desvío.
- Alcance y credenciales: cfb927f solo toca firmware/esp32/**. No hay Wi-Fi, MQTT ni credenciales (la Grep de wifi, password, ssid y mqtt solo encuentra un comentario en main.cpp:1). Coincide con lo predicho.
- H-1 y H-2: no se inventó evidencia de banco. En docs/pm/evidencia/hw/WP-3.1/ solo está LEEME.md. Coincide.
- Regresión: se predijeron 43 failed y 90 passed, con fallas solo en test_wp_3_2 y test_wp_4_x. Coincide.
- Compilación para ESP32: sigue sin verificarse (WP-3.1_it2_ejecucion.md:15). Coincide; es la observación H-5, que sigue abierta.

## Hallazgos
No hay hallazgos nuevos. La regla de hallazgos congelados solo admitiría nuevos de severidad Mayor, y no hay ninguno.

## Alcance, integridad y regresión
- Alcance: cfb927f modifica firmware/esp32/src/elevacion.cpp, firmware/esp32/src/elevacion.h, firmware/esp32/src/main.cpp y firmware/esp32/test/test_elevacion.cpp, todos dentro de `firmware/esp32/**`. 70f90d4 y 9862af2 son commits [pm] que solo agregan archivos de docs/pm/auditorias y docs/pm/evidencia.
- Integridad: el commit del WP (cfb927f) no toca nada en docs/pm/.
- LEEME.md (docs/pm/evidencia/hw/WP-3.1/LEEME.md): sigue diciendo que peso_invalido.txt y umbral.txt están pendientes "para CA-3.1.3 y CA-3.1.5", lo que contradice CC-010. Lo valoro así:
  - No es un desvío de alcance, porque no se modificó y está dentro del Alcance del WP.
  - Ningún criterio vigente (3.1.1, 3.1.2, 3.1.6) lo usa como evidencia, así que no afecta al dictamen.
  - Sería, como mucho, una Observación, y la regla de hallazgos congelados no admite observaciones nuevas en la it2. Por eso no lo registro como hallazgo.
  - Recomendación al orquestador: actualizarlo o retirarlo con un commit [pm], remitiendo a CA-3.2.7 y CA-3.2.8 de WP-3.2, para que nadie produzca evidencia por serie que CC-010 ya descartó.
- Árbol de trabajo: el log marca "Árbol limpio: no". `git status` muestra solo un archivo sin seguimiento en la raíz, `10.0)`, de 0 bytes y creado a las 08:18, antes del commit del WP. Parece un residuo de una redirección de shell. No está en ningún commit ni afecta al firmware ni a las pruebas, pero conviene borrarlo.
- Regresión: el log (commit 70f90d4, cuyo firmware y pruebas son idénticos a HEAD; código de salida 1) da 43 failed y 90 passed. Todas las fallas están en test_wp_3_2, test_wp_4_1, test_wp_4_2 y test_wp_4_3, WP pendientes con módulos que todavía no existen. Es el mismo recuento que en la it1 (WP-3.1_it1_aceptacion_e341bae.log: 43 failed y 90 passed). No falla ninguna prueba de WP-1.x, 4.4 ni 5.x, así que no hay regresión.
- Credenciales: no hay ninguna en el firmware.
- Ningún criterio de WP-3.1 apunta a tests/aceptacion. test/test_elevacion.cpp es una prueba interna. No la ejecuté (g++ no está entre los comandos permitidos) y no la cuento como evidencia. La verifiqué siguiendo el código a mano y sus aserciones nuevas son coherentes con elevacion.cpp.

## Hallazgos de iteraciones previas: cerrados / persistentes
- H-1 [Mayor] Falta la evidencia de banco de CA-3.1.3: **trasladado, no aplica en WP-3.1**. CC-010 (aprobado el 2026-11-17) movió el criterio a WP-3.2 como CA-3.2.7.
- H-2 [Mayor] Falta la evidencia de banco de CA-3.1.5: **trasladado, no aplica en WP-3.1**. CC-010 lo movió a WP-3.2 como CA-3.2.8.
- H-3 [Menor] Un LIFT válido durante una elevación activa reinicia el límite de 8 s: **cerrado**.
  - elevacion.cpp:67 ya no reasigna `g_inicioMs` ni vuelve a energizar si `g_activa` es verdadero, y la prueba interna test_elevacion.cpp:21-24 lo demuestra.
  - Matiz: un LIFT que llegue *después* del apagado por tiempo inicia otro ciclo de 8 s, con una pausa de apenas un ciclo de `loop()`. Lo trato como un comando nuevo y legítimo. CA-3.1.6 fija el máximo por elevación y no exige un período de enfriamiento ni rechazar un LIFT con la tarima ya elevada. Si se quiere esa protección, corresponde a la máquina de estados de WP-3.2 o WP-4.x, o a una solicitud de cambio, y no a este WP.
- H-4 [Observación] La precisión de float acepta valores apenas por encima de 10.0: **atendida**. elevacion.cpp:24 compara el double contra 10.0 antes de convertir, y test_elevacion.cpp:26 comprueba que "10.0000000001" da OVERWEIGHT.
- H-5 [Observación] La compilación para ESP32 y la semántica de LIFT_OK no están verificadas: **persiste en parte, sigue abierta como Observación**. El buffer `linea` quedó acotado (main.cpp:15). Siguen pendientes la compilación con PlatformIO y la alineación del momento de `LIFT_OK` con contratos/esp32.md:20. La compilación se demostrará de hecho con la evidencia de CA-3.2.7 y CA-3.2.8 en WP-3.2.
