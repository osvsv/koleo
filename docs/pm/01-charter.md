# Project Charter — KOLEO
Versión: 1.1 (G1, respuestas de Osvaldo aplicadas)

## Propósito y justificación

Prototipo de robot móvil semiautónomo que sube, transporta y deposita tarimas de hasta 10 kg en un almacén de prueba a escala y registra cada movimiento en una base de datos, para reducir la diferencia entre la ubicación física de las tarimas y su registro digital. Se entrega como reto del curso Implementación de Internet de las Cosas (gpo 501, Tec de Monterrey, Campus Guadalajara). [S]

## Objetivos medibles

| ID | Objetivo | Indicador | Procedencia |
| --- | --- | --- | --- |
| OBJ-01 | Elevar la carga de demostración (100 g; capacidad de diseño de referencia 10 kg) | Tiempo de elevación < 15 s | [D] |
| OBJ-02 | Llegar al destino de forma autónoma | Error de llegada < 10 cm | [D] |
| OBJ-03 | Registrar la nueva ubicación al depositar | Latencia depósito → base de datos < 2 s, medida extremo a extremo | [S] |
| OBJ-04 | Ejecutar las rutas de referencia | RUTA_1, RUTA_2 y RUTA_3 sin colisión (referencia, no criterio de evaluación) | [D] |
| OBJ-05 | Operar de forma sostenida | Traslado de 3 min sin reinicio ni corte de energía | [S] |
| OBJ-06 | Cumplir el Reto IoT | ≥ 2 sensores y ≥ 2 actuadores en red, base de datos con Web API, ≥ 5 indicadores en tiempo real | [N] Descripción del Reto IoT (`importado/KOLEO_todo.md` §3) |

## Alcance

**Incluido:** chasis con tracción diferencial y elevación por un actuador lineal; báscula con rechazo por sobrepeso; parada por obstáculo (HC-SR04); firmware ESP32; Raspberry Pi 5 con planificador A*, lectura QR y consolidación MQTT; contratos MQTT/comandos del ESP32/estados/SQL; backend (MQTT → SQLite → API); tablero React con flotilla, monitoreo, control y gestión logística; robot simulado; pruebas VAL-01 a VAL-08 con evidencia; reporte final. [S]

**Excluido explícitamente:** integración del RPLIDAR al mapa y Google Coral (fuera por DP-11); localización SLAM; replanificación automática tras un obstáculo; operación en almacenes arbitrarios o con cargas de más de 10 kg; cargas físicas superiores a 100 g en las demostraciones; autenticación de usuarios en la API; almacenamiento offline y reintentos ante pérdida de Wi-Fi. [S]

## Entregables principales

1. Robot físico funcionando (chasis, elevación, tracción, sensores, energía).
2. Firmware ESP32 y software de la Raspberry Pi.
3. Contratos, backend con base de datos y Web API, robot simulado.
4. Tablero web.
5. Evidencia de VAL-01 a VAL-08 y reporte final.
6. Demo del 2-dic-2026.

## Partes interesadas y quién aprueba

| Parte | Papel | Aprueba |
| --- | --- | --- |
| Osvaldo Sierra | Coordina la planeación | G0 y G1 (con el equipo) |
| Miranda Henry, Elías Tamez, Leonardo Alfonzo, Alvaro Alcaraz | Equipo; el trabajo se reparte por tareas, sin dueños por subsistema (SUP-016) | Demos semanales |
| Profesor del curso | Evalúa la entrega final (tentativa 2-dic) con una demostración de cómo se mueve el robot y cómo carga el peso; no hace revisiones parciales | Entrega final |

## Supuestos y restricciones

- Entrega final tentativa el 2-dic-2026; el profesor no hace revisiones parciales ni ha fijado fechas intermedias [D].
- Capacidad del equipo: 4 a 6 h por semana por persona (≈ 60 a 90 h de equipo hasta el 2-dic) [D].
- Presupuesto $8,000 MXN ±25 %, tope $10,000 MXN [S] (Charter original, importado).
- BOM final al 11-nov-2026 sin piezas nuevas, salvo el fusible de 10 A (DP-10) [S].
- Canal de datos MQTT con el broker en la Raspberry Pi; el ESP32 y la Pi se conectan a la red y no hay cable de datos entre ellos [D].
- Carga de demostración de 100 g; el límite de sobrepeso sigue en 10 kg y se verifica con peso simulado [D].
- Tablero en React + Vite + Tailwind [D].
- Supuestos de impacto en `supuestos.md` (SUP-001 a SUP-018).

## Riesgos iniciales

Ver `05-riesgos.md`. Principales: estado físico del robot, navegación sin lazo cerrado, báscula que devuelve 0 si falla, batería sin protección, tiempo.

## Criterios de cierre

1. VAL-01 a VAL-08 con resultado medido y evidencia enlazada (si una meta no se alcanza, se reporta la medición real, DP-13).
2. Demo completa grabada antes de la entrega final, que muestra cómo se mueve el robot y cómo carga el peso.
3. Reporte final con evidencia, gasto final y bitácora del robot.
4. Todos los WP de la WBS con dictamen CONFORME, o desviación aceptada por Osvaldo.
