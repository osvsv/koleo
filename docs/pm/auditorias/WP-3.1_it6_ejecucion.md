# Ejecución WP-3.1 — iteración 6 (reabierto por CC-016)
Resultado: TERMINADO (sin compilar: `pio` no está instalado en este equipo)

## Archivos modificados
- firmware/esp32/src/pines.h: reescrito con el pinout real (CC-016).
- firmware/esp32/src/main.cpp: `PIN_MI_ENA` -> `PIN_MI_EN`, `PIN_MD_ENB` -> `PIN_MD_EN`; comentario de setup actualizado (GPIO 14 y 27 en LOW).
- firmware/esp32/src/elevacion.cpp: `elevacionIniciarPines()` pone en OUTPUT/LOW los dos enables (14 y 27).

## Pines finales
- Actuador BTS7960: RPWM=18 (sube), LPWM=19 (baja).
- Motor izquierdo L293D: EN=14, IN1=26, IN2=25.
- Motor derecho L293D: EN=27, IN3=33, IN4=32.
- UART con la Pi: RX2=16, TX2=17.
- HC-SR04 y encoders: sin asignar (SUP-040). Sin pines de VL53L1X ni HX711 (CC-004). Sin referencias a L298N/ENA/ENB en firmware/.

## Autoverificación
- CA-3.1.1: lectura de pines.h; GPIO 14, 18, 19, 25, 26, 27, 32, 33, 16, 17 sin duplicados. Compilación NO verificada.
- Estado seguro al inicio: RPWM, LPWM, EN izq. y EN der. en LOW (elevacionIniciarPines), luego IN1..IN4 en LOW (setup). Solo por lectura de código.
- CA-3.1.2 y CA-3.1.6: `evaluarLift` y la lógica de millis/8 s no cambiaron.
- pytest: 111 pasan, 49 fallan (test_wp_4_1, 4_2, 4_3; no leen el firmware). test_wp_3_2 no falla.

## Desviaciones
Ninguna. Sin bloqueos ni contradicciones con la línea base. Sin variables de entorno nuevas.

## Sugerencias fuera de alcance
- Asignar pines de HC-SR04 y encoders en WP-2.4.
- Compilar con PlatformIO cuando haya una máquina con `pio`.
- Confirmar en el prototipo que 25/26 y 32/33 dan el sentido de giro esperado.
