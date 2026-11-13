# WP-3.1 — informe de ejecución, iteración 1

Resultado: TERMINADO (evidencia de banco pendiente; sin compilación para ESP32)

Archivos creados: `firmware/esp32/platformio.ini`, `src/pines.h` (§9 sin HX711 ni VL53L1X), `src/elevacion.h` y `elevacion.cpp` (`pesoValido`, `excedeLimite`, `evaluarLift`, `elevacionSolicitar`, `elevacionActualizar`; código Arduino bajo `#ifdef ARDUINO`), `src/main.cpp` (monitor serie `LIFT <peso>`, GPIO 14 en LOW al inicio), `test/test_elevacion.cpp` (prueba interna en PC, no cuenta como evidencia).

Autoverificación (del ejecutor):
- CA-3.1.1: comparado con §9 al escribirlo; sin segunda revisión.
- CA-3.1.2: `evaluarLift` da PESO_INVALIDO con peso NULL, vacío, no numérico, "nan", 0 o negativo (prueba interna).
- CA-3.1.3 y 3.1.5: lógica probada en PC (11.8 y 10.1 OVERWEIGHT; 10.0 y 0.1 LIFT_OK). Falta evidencia de banco `peso_invalido.txt` y `umbral.txt`.
- CA-3.1.6: `millis()`, sin `delay()`, `ELEVACION_MAX_MS` 8000 (la prueba interna lo apaga a 8000, no a 7999).
- `g++ -I src test/test_elevacion.cpp src/elevacion.cpp` compila y pasa. NO verificado: compilación para ESP32 (sin PlatformIO) ni hardware.

Desviaciones:
| Archivo o criterio | Categoría | Nota |
| --- | --- | --- |
| docs/pm/evidencia/hw/WP-3.1/LEEME.md | alcance | El hook bloquea escribir en docs/pm a los agentes; lo creó el orquestador |

Bloqueos con la línea base: ninguno. Variables de entorno nuevas: ninguna.

Sugerencias fuera de alcance:
- Tiempo de elevación igual al máximo de 8 s por falta de final de carrera; fijar el tiempo real en banco.
- El BTS7960 suele necesitar R_EN/L_EN; §9 no les asigna pin, revisar si van a 3.3 V.
- `contratos/esp32.md` lo actualizó WP-1.1 (it3).
