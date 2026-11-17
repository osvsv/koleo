# Ejecución WP-3.1 — iteración 4
Resultado: LISTO (prueba de host pasa; NO compilado para ESP32). Desviaciones: ninguna.

Archivos: firmware/esp32/src/elevacion.cpp, firmware/esp32/src/elevacion.h, firmware/esp32/test/test_elevacion.cpp. No se tocaron main.cpp ni red_mqtt.*.

## Corrección de H-1 (informe docs/pm/auditorias/WP-3.1_it3.md; opción A de Osvaldo)
- `elevacionSolicitarEn` arma un `esp_timer` one-shot a ELEVACION_MAX_MS (8000 ms); el timer se crea en `elevacionIniciarPines()`. Todo lo de hardware va en `#ifdef ARDUINO`.
- El callback llama a la nueva `elevacionCorteTimerEn(ahora)` (declarada en elevacion.h): apaga el pin y pone `g_activa=false`, sin delay() ni llamadas bloqueantes. Corre en la tarea de esp_timer, independiente de loop() y de la red.
- `g_activa` y `g_inicioMs` pasan a `volatile`, con secciones críticas mínimas (portMUX; macros vacías en host). `elevacionActualizarEn` usa la misma función de corte y cancela el timer con `esp_timer_stop` si la elevación ya terminó.
- Seguridad ante carreras: el corte es idempotente y solo corta si pasaron 8 s desde `g_inicioMs`, así que un callback tardío de una elevación anterior no corta una nueva. Un LIFT válido con la elevación activa sigue sin reiniciar el límite. Se mantienen los códigos y las firmas de la Interfaz; solo se añade `elevacionCorteTimerEn`.

## Verificación
- `g++ -Wall -I src test/test_elevacion.cpp src/elevacion.cpp` (desde firmware/esp32): sin warnings, imprime "OK". Pruebas nuevas: el corte llega a los 8 s (7999 activa, 8000 corta) solo con `elevacionCorteTimerEn`, sin llamar a elevacionActualizar; corte normal seguido de callback tardío; callback tardío que no corta una elevación nueva; envoltura del reloj uint32.
- NO verificado: compilación para ESP32 (`esp_timer.h`, `portMUX`, `esp_timer_create_args_t a = {}` sin probar; PlatformIO está en la Pi) ni el apagado a los 8 s en hardware con loop() bloqueado.

Sugerencias del ejecutor: WP-3.2 debe mantener intacta la llamada a `elevacionIniciarPines()` en `setup()` (ahí se crea el timer); verificar por hardware el apagado a los 8 s con la red caída.
