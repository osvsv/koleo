# Auditoría WP-3.1 — iteración 6
Dictamen: CONFORME CON OBSERVACIONES
Commit: 5a2e0b5c530a0d38b6ab922d404b24fbf4be96b9
Evidencia: docs/pm/evidencia/WP-3.1_it6_aceptacion_0001959.log
Archivos auditados: firmware/esp32/platformio.ini, firmware/esp32/src/elevacion.cpp, firmware/esp32/src/elevacion.h, firmware/esp32/src/main.cpp, firmware/esp32/src/pines.h, firmware/esp32/test/test_elevacion.cpp

CC-016 reabrió el WP y cambió CA-3.1.1. El trabajo está en el commit a356f12. El log se generó sobre 0001959. Entre 0001959 y HEAD (5a2e0b5) solo cambian archivos de docs/pm/ (predicciones, log y json), por lo que el log vale para HEAD. El log indica "Árbol limpio: sí".

## Verificación por criterio
| Criterio | Resultado | Evidencia |
| --- | --- | --- |
| CA-3.1.1 [D] | Cumple | pines.h:1 menciona el driver L293D; sin referencias a L298 en firmware/. Motor izq. EN=14, IN1=26, IN2=25 (pines.h:10-12); der. EN=27, IN3=33, IN4=32 (pines.h:15-17), coinciden con CC-016 y los pares no están invertidos. Actuador RPWM=18 sube, LPWM=19 baja (pines.h:6-7). Sin `#define` de VL53L1X ni HX711 (solo la nota de CC-004, pines.h:2). HC-SR04 y encoders solo como comentario, sin `#define` ni centinela (pines.h:23-26), con la prohibición de repetir {14,18,19,25,26,27,32,33}. GPIO definidos 18, 19, 14, 26, 25, 27, 33, 32, 16, 17, sin duplicados. Búsqueda de `PIN_[A-Z0-9_]+` en firmware/: elevacion.cpp y main.cpp solo usan constantes existentes; no queda PIN_MI_ENA, PIN_MD_ENB, PIN_ENC_* ni PIN_US_*. |
| CA-3.1.2 [D] | Cumple (sin cambios) | El diff de a356f12 en elevacion.cpp solo toca `elevacionIniciarPines()`. `evaluarLift` igual (elevacion.cpp:26-37): rechaza con PESO_INVALIDO NULL o vacío, no numérico, no finito o ≤ 0. main.cpp:100 sin cambios. |
| CA-3.1.6 [S] | Cumple (sin cambios) | Corte por esp_timer one-shot de `ELEVACION_MAX_MS*1000` µs (elevacion.cpp:113-116); comparación segura ante desbordamiento `(uint32_t)(ahora - g_inicioMs)` (elevacion.cpp:62); `actuadorSube` usa PIN_ACT_RPWM/LPWM (elevacion.cpp:49-50); sin `delay()` en firmware/. |
| CA-3.1.3, 3.1.5 | No aplica | Movidos a WP-3.2 por CC-010. |
| CA-3.1.4, 3.1.7, 3.1.8 | No aplica | Retirados por CC-004. |

## Predicciones frente a lo observado
- Pinout y nombres: se cumple lo predicho (L293D, roles de IN correctos, RPWM=18 sube, LPWM=19 baja, sin VL53L1X ni HX711).
- HC-SR04: se predijo que seguirían TRIG/ECHO en 18/19; no ocurrió. Quedaron sin asignar y no se preasignaron candidatos de SUP-040 ni hay centinela.
- Renombrado a medias: no lo hay; las referencias cruzadas están completas. La compilación sigue sin verificarse (H-5).
- Estado seguro al inicio: `setup()` llama primero a `elevacionIniciarPines()` (main.cpp:130), que pone OUTPUT/LOW 18, 19, 14 y 27 (elevacion.cpp:81-87); luego 26, 25, 33 y 32 (main.cpp:132-135), todo antes de `redIniciar` (main.cpp:136). El PWM de GPIO 14 en el arranque ya existía con el pinout anterior; por la regla de hallazgos congelados no se agrega.
- Restos del pinout anterior: ninguno en los archivos versionados de firmware/.
- Alcance y docs/pm: se cumplen.

## Hallazgos
Esta iteración no genera hallazgos nuevos (desde la it2 solo cuentan los nuevos de severidad Mayor).

## Alcance, integridad y regresión
- Alcance: a356f12 solo toca firmware/esp32/src/pines.h, main.cpp y elevacion.cpp, dentro de `firmware/esp32/**`. No toca el sketch del prototipo ni `importado/`. main.cpp también es del alcance de WP-3.2; el cambio es un renombrado de constantes y un comentario, sin efecto en la lógica MQTT. reverificar.py --impacto: ninguno.
- Integridad: a356f12 no modifica docs/pm/. Los commits [pm] 0001959 y 5a2e0b5 solo agregan informe de ejecución, predicciones y evidencia.
- Regresión: 49 failed, 111 passed (it5: 37 y 96; la suite creció con las pruebas de CC-014 y WP-4.4). Las 49 fallas son `ModuleNotFoundError`/`ImportError` en test_wp_4_1, 4_2 y 4_3 (módulos de WP pendientes). WP-4.4 y WP-3.2 sin fallas. No hay regresión.
- Credenciales: el diff no agrega ninguna; secrets.h sigue sin versionarse.

## Hallazgos de iteraciones previas
- H-1 [Mayor] it3 (corte de 8 s dependiente de `loop()`): cerrado; el esp_timer no cambió.
- H-3 it1 (LIFT repetido reiniciaba el límite): cerrado (elevacion.cpp:102-111).
- H-4 it1 (precisión float en 10 kg): atendido (elevacion.cpp:33).
- H-1 y H-2 it1 (evidencia de banco): trasladados a WP-3.2 (CA-3.2.7 y CA-3.2.8).
- **H-5 [Observación] (compilación para ESP32 sin verificar): persiste.** Pesa más porque el commit renombra constantes. PlatformIO no está instalado y no hay log de `pio run -e esp32dev` en docs/pm/evidencia/. Se cierra con ese log sobre el commit vigente. Conviene confirmar en banco el sentido de giro de 26/25 y 33/32 y que RPWM=18 sube.
- Nota it2 sobre docs/pm/evidencia/hw/WP-3.1/LEEME.md (menciona CA-3.1.3 y 3.1.5): sigue abierta.
