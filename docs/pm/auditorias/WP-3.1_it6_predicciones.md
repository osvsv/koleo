# Predicciones WP-3.1 — iteración 6

Fuentes leídas (solo de `docs/pm/`): sección WP-3.1 de 03-wbs.md, fila CC-016 de cambios.md, SUP-010, SUP-032 y SUP-040 de supuestos.md, y REQ-F-001, 002, 003 y NF-009 de 02-requisitos.md. No se abrió el informe de ejecución.

## Por criterio

- **CA-3.1.1 [D]** (reabierto por CC-016). En `firmware/esp32/src/pines.h` debería verse:
  - Mención explícita del driver L293D; sin nombres ni comentarios de L298N.
  - Motor izquierdo EN=14, IN1=26, IN2=25; derecho EN=27, IN3=33, IN4=32. Revisar que los pares IN no estén invertidos.
  - Actuador BTS7960: RPWM=18 sube, LPWM=19 baja.
  - Sin pines de VL53L1X ni HX711, tampoco como comentario.
  - HC-SR04 y encoders sin asignar (centinela o comentados), sin repetir {14, 25, 26, 27, 32, 33, 18, 19}. Lo probable es que sigan TRIG/ECHO en 18/19 del pines.h anterior. Si se preasignaron candidatos de SUP-040, contradice "sin asignar hasta WP-2.4".
  - Coherencia: ningún archivo de `src/` debe usar constantes viejas que ya no existan; un renombrado a medias deja el firmware sin compilar.
- **CA-3.1.2 [D]** (no cambia). `LIFT` sin `peso_kg`, no numérico, 0, negativo o no finito responde `PESO_INVALIDO`. Frágil: `doc["peso_kg"] | 0.0f` sin validar antes. Riesgo: que al tocar los pines se haya alterado el orden de validación en `elevacion.cpp`.
- **CA-3.1.6 [S]**. Sin `delay()` en la elevación, `millis()` con tope de 8000 ms que apaga RPWM y LPWM. Al pasar el actuador a 18/19, el PWM debe apuntar a las constantes nuevas. Comparación segura ante desbordamiento de `millis()`.
- **Interfaz**: `excedeLimite(10.0)` falso y `excedeLimite(10.01)` verdadero (SUP-010); `pesoValido` falso para ≤ 0 y no finitos.
- **Estado seguro al inicio**: `setup()` pone OUTPUT/LOW EN 14/27, IN 25/26/32/33 y RPWM/LPWM 18/19 antes de Wi-Fi/MQTT. GPIO 14 emite PWM durante el arranque del ESP32; a lo sumo una Observación para WP-2.3/2.4.

## Riesgos de interpretación
1. Pares IN y sentido del actuador invertidos (el conjunto de GPIO coincide, los roles no).
2. HC-SR04 "reasignado" en lugar de "sin asignar".
3. Centinela que cuenta como repetición (0 o un número prohibido); `pinMode(-1, ...)` sin protección.
4. Sin PlatformIO no se puede afirmar que compila; solo grep cruzado entre `pines.h` y `src/`. La afirmación "compila" no es verificable.
5. Alcance: `main.cpp`, `red_mqtt.*` y `platformio.ini` son también de WP-3.2; ningún archivo del sketch ni de `importado/` debe aparecer en el diff.
6. Restos del pinout anterior en comentarios o documentación de `firmware/`.
7. El commit del WP no debe tocar `docs/pm/`.
8. Iteración 6: solo cierre de hallazgos previos, regresiones y Mayores nuevos; lo nuevo de CA-3.1.1 sí es evaluable por CC-016.
