# Predicciones WP-3.1 — iteración 1

Generadas por auditor-conformidad (modo predicciones) antes de auditar, solo con docs/pm/.

- CA-3.1.1: pines.h solo declara números; GPIO 14 en bajo al inicio debe estar en `setup()`. No se pudo contrastar `importado/KOLEO_todo.md` §9 (fuera de docs/pm/).
- CA-3.1.2: riesgos: valor por defecto de ArduinoJson o `atof` (equivale "sin peso" a 0), `strtof` sin `endptr` ("10abc"), falta de `isfinite` (NaN pasa `excedeLimite`), `peso_kg` como string JSON.
- CA-3.1.3: predicho NO CUMPLE en it1: la evidencia de banco `peso_invalido.txt` está pendiente (Mayor si no existe).
- CA-3.1.5: predicho NO CUMPLE en it1: falta `umbral.txt`. En código: `kg > 10.0f` estricto.
- CA-3.1.6: riesgos: `delay()`, `while (millis()...)` bloqueante, timeout que no corta el pin, `LIFT` nuevo que reinicia el contador.
- Interfaz: firmas exactas, códigos literales `LIFT_OK` | `OVERWEIGHT` | `PESO_INVALIDO`, sin Wi-Fi/MQTT (WP-3.2).
- Riesgos: compilación para ESP32 sin verificar; ningún criterio apunta a tests/aceptacion (el log sirve solo como regresión); `main.cpp` compartido con WP-3.2 (reverificación futura); posible contradicción de §9 con la línea base.
