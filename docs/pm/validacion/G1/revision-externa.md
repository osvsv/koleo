# Paquete de revisión externa — G1 (línea base), proyecto KOLEO

## Encargo para el revisor

Revisa este paquete de validación antes de que lo responda. Señala: (a) preguntas que junten dos decisiones; (b) opciones sesgadas o que falten; (c) supuestos de alto impacto que no se preguntan; (d) recomendaciones que no se sostienen. No respondas las preguntas por mí.

## Contexto mínimo

- **Proyecto:** KOLEO, robot móvil a escala (~30×30 cm) que sube, transporta y deposita tarimas de hasta 10 kg y registra cada movimiento en una base de datos vía MQTT. Curso de IoT, equipo de 5, entrega el 2-dic-2026.
- **Nivel de rigor:** Estándar; modelo incremental con tres cierres semanales (20-nov, 27-nov, 30-nov/1-dic).
- **Punto de validación:** G1 (aprobación de la línea base: requisitos, 19 paquetes de trabajo y sus criterios).
- **Quién responde:** los 5 integrantes del equipo (≈ 10 min cada uno, 19 preguntas); Osvaldo consolida. El profesor no responde.
- **Estado físico:** el robot es un armado básico y aún nada ha funcionado bien.

## Decisiones en juego

| ID | Formato | Pregunta | Decide | Impacto |
| --- | --- | --- | --- | --- |
| V-01 | Sí/No/Corregir | Dueños propuestos por subsistema | Quién es dueño de cada subsistema | Alto (afecta 19 paquetes) |
| V-02 | Sí/No/Corregir | ≥ 10 h por semana por persona | Disponibilidad mínima | Alto (19) |
| V-03 | Sí/No/Corregir | ¿Hardware del listado final del 11-nov completo? | Si el hardware está completo | Alto (9) |
| V-04 | Sí/No/Corregir | Python para backend, Pi y simulador | Lenguaje | Alto (8) |
| V-05 | A/B/C | Dónde corre el broker MQTT | Ubicación del broker | Alto (6) |
| V-06 | A/B/C | ¿La Pi cuenta como dispositivo en red del Reto IoT? | Aceptación de la arquitectura | Alto (5) |
| V-07 | A/B/C | Sensor(es) de paro | Sensor(es) | Alto (5) |
| V-08 | A/B | Fusible de 10 A sí/no | Fusible | Alto, seguridad (2) |
| V-09 | A/B/C | Distancia de paro: 12, 15 o 20 cm | Umbral | Medio (3) |
| V-10 | Sí/No/Corregir | Mapa 5×6 y tres rutas de evaluación | Mapa y rutas | Alto (5) |
| V-11 | Ejemplo | 10.0 kg exactos se levantan | Límite inclusivo | Medio (5) |
| V-12 | Ejemplo | 0.0 kg válidos: no sube y avisa "sin carga" | Comportamiento con 0 kg | Medio (3) |
| V-13 | Ejemplo | Sensor de paro sin lectura: el robot se detiene | Fallo seguro | Alto, seguridad (3) |
| V-14 | A/B | Estado de la tarima tras el depósito | Nombre del estado | Medio (4) |
| V-15 | A/B | Inicio del conteo de latencia de 2 s | Instante de inicio | Alto (3) |
| V-16 | A/B/C | Sin QR: no inicia / ID de ruta / ID manual | Comportamiento sin QR | Medio (3) |
| V-17 | A/B | Metas oficiales: <15 s y <10 cm, o <10 s y <5 cm | Metas ante el profesor | Alto (4) |
| V-18 | Ejemplo | Evento repetido no duplica el historial | Idempotencia | Medio (3) |
| V-19 | Sí/No/Corregir | Fechas de cierre 20-nov, 27-nov, 30-nov/1-dic | Calendario | Medio (3) |

## Supuestos que quedan fuera del paquete, con su impacto

1. **Backend en Flask con SQLite** (afecta 4 paquetes). Bajo riesgo: si alguien lo objeta, se cambia con una solicitud de cambio.
2. **Telemetría a 2 Hz** (afecta 4). Bajo.
3. **Lista de 7 estados del robot** (afecta 3). Bajo-medio; la lista de estados de tarima sí entra (V-14).
4. **Tablero por consulta cada 1 s en vez de WebSocket** (afecta 2). Bajo.
5. **515 pulsos por vuelta de encoder y rueda de 65 mm** (afecta 1 paquete): se mide durante la calibración.
6. **Los trabajos físicos los hacen personas y el agente solo audita la evidencia** (decisión DP-09; afecta 7 paquetes). Es una decisión del método, no del equipo.
7. **Reportar la medición real si una meta no se alcanza** (DP-13; afecta el reporte final). Medio.
8. **Sin paro de emergencia físico** (solo STOP por software y desconectar el conector T de la batería). Se mantiene aunque V-08 acepte el fusible. Medio-alto en seguridad. ¿Debería entrar como pregunta?
9. **Fuera del alcance: RPLIDAR, Google Coral, SLAM, replanificación tras un obstáculo.** Si algo de eso debía entregarse, está fuera.

## Recomendaciones del modelo (separadas de las preguntas) [S]

- [S] **V-08: instalar el fusible.** Motivo: una LiPo 3S de 25C puede entregar decenas de amperes en un corto; la prueba de continuidad antes de energizar no protege durante la operación; el costo es mínimo.
- [S] **V-07: solo HC-SR04 (A).** Motivo: lo lee el ESP32 directamente y frena aunque falle la Pi; el RPLIDAR no está integrado al código y el tiempo es corto.
- [S] **V-16: no iniciar sin QR (A).** Motivo: usar el ID por defecto de la ruta puede asociar una carga equivocada (riesgo señalado en la documentación original).
- [S] **V-09: 15 cm.** Motivo: es el valor del plan de trabajo; 12 cm queda justo con la inercia y 20 cm reduce el espacio útil en celdas de 30 cm.
- [S] **V-17: confirmar con el profesor antes de dar por fijas las metas.** Motivo: el documento original decía <10 s y <5 cm; la decisión del 11-nov las relajó sin constancia del profesor.
- [S] **V-06: preguntar al profesor antes del 17-nov.** Motivo: si el ESP32 debe estar en red, cambia el diseño del puente MQTT.

Sin credenciales ni datos personales en este paquete (los nombres de pila son los de los integrantes que responden).
