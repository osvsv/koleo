# Paquete de revisión externa — G0 (perfil), proyecto KOLEO

## Encargo para el revisor

Revisa este paquete de validación antes de que lo responda. Señala: (a) preguntas que junten dos decisiones; (b) opciones sesgadas o que falten; (c) supuestos de alto impacto que no se preguntan; (d) recomendaciones que no se sostienen. No respondas las preguntas por mí.

## Contexto mínimo

- **Proyecto:** KOLEO, robot móvil a escala (~30×30 cm) que sube, transporta y deposita tarimas de hasta 10 kg y registra cada movimiento en una base de datos por MQTT. Curso de IoT, equipo de 5, entrega el 2-dic-2026 (tres semanas desde el 11-nov).
- **Nivel de rigor propuesto:** Estándar. Modelo incremental con arranque por riesgo, tres incrementos semanales.
- **Punto de validación:** G0 (perfil, antes de generar la línea base).
- **Quién responde:** Osvaldo (coordina el proyecto). El equipo de 5 valida a partir de G1.
- Estado: el robot es un armado básico en banco y "nada ha funcionado bien" todavía.

## Decisiones en juego (tabla "Decisiones del perfil")

| ID | Decisión | Procedencia | Impacto si está mal |
| --- | --- | --- | --- |
| DP-01 | Nivel Estándar | [S] | Medio: sobrecarga o falta de control para 3 semanas |
| DP-02 | Incremental con arranque por riesgo, 3 incrementos semanales | [S] | Alto: define la WBS y los puntos de demo |
| DP-03 | Entrega 2-dic, tres semanas | [D] (Osvaldo, 2026-11-11) | Alto |
| DP-04 | Metas: <15 s para elevar 10 kg, <10 cm de error | [D] (Osvaldo, 2026-11-11) | Alto: el Charter original decía <10 s y <5 cm |
| DP-05 | MQTT con broker, publica la Pi | [D] (Osvaldo, 2026-11-11) | Alto: el ESP32 no se conecta él mismo a la red |
| DP-06 | Tablero React + Vite + Tailwind | [D] (Osvaldo, 2026-11-11) | Medio |
| DP-07 | Validan los 5 del equipo, sesión semanal | [D] (Osvaldo, 2026-11-11) | Medio |
| DP-08 | No segmentar | [S] | Bajo |
| DP-09 | WP físicos los hacen personas; el agente audita evidencia | [S] | Alto: los agentes no pueden armar ni probar el robot |
| DP-10 | Reincorporar fusible de 10 A; sin paro físico | [S] | Alto para seguridad; contradice decisión del equipo del 11-nov |
| DP-11 | HC-SR04 como sensor de paro; RPLIDAR y Coral fuera | [S] | Medio: Osvaldo marcó "aún no decidido" |
| DP-12 | Cierres 20-nov, 27-nov y 30-nov/1-dic | [S] | Medio: el plan importado usaba otras fechas con días de la semana incorrectos |
| DP-13 | Si una meta no se alcanza, se reporta la medición real | [S] | Medio |

## Supuestos que quedan fuera de las preguntas, con su impacto

1. **Reto IoT exige microcontroladores en red.** Con MQTT desde la Pi, el ESP32 no se conecta él mismo. Impacto alto; no se preguntó. ¿Debe entrar?
2. **El profesor no participa en G0/G1.** Se asume que las metas <15 s y <10 cm fueron aceptadas por él. Impacto alto.
3. **Software por pruebas automáticas, hardware por evidencia (foto, video, medición).** Impacto alto en cuántos criterios son verificables por agente.
4. **Sin código de partida:** los fragmentos de firmware, A* y SQL de los documentos se tratan como referencia, no como base. Impacto medio.
5. **El presupuesto de $8,000 ±25 % se mantiene; el fusible lo rompe de forma marginal.** Impacto bajo.
6. **Horas disponibles por persona** y quién tiene cada subsistema: aún no preguntados. Impacto alto en el calendario.

## Recomendaciones del modelo [S]

- [S] Nivel Estándar y no Ligero, porque hay cinco personas, varias integraciones y riesgo físico. Motivo: Ligero es para una persona.
- [S] Tres incrementos con demo semanal, porque en hardware los problemas aparecen al integrar y la fecha es fija.
- [S] Fusible de 10 A. Motivo: LiPo 3S de 25C entrega decenas de amperes y sin fusible un corto puede causar fuego; la prueba de continuidad ayuda, pero no protege en operación.
- [S] HC-SR04 como sensor de paro. Motivo: lo lee el ESP32 directo, frena aunque falle la Pi, y es la base de VAL-05.
- [S] Cierres 20/27-nov y 30-nov/1-dic. Motivo: el calendario importado usa fechas que no coinciden con los días de la semana.

Sin credenciales ni datos personales en este paquete.
