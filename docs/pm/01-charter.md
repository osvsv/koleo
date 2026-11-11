# Project Charter — KOLEO
Versión: 1.0 (borrador previo a G1)

## Propósito y justificación

Prototipo de robot móvil semiautónomo que sube, transporta y deposita tarimas de hasta 10 kg en un almacén de prueba a escala y registra cada movimiento en una base de datos, para reducir la diferencia entre la ubicación física de las tarimas y su registro digital. Se entrega como reto del curso Implementación de Internet de las Cosas (gpo 501, Tec de Monterrey, Campus Guadalajara). [S]

## Objetivos medibles

| ID | Objetivo | Indicador | Procedencia |
| --- | --- | --- | --- |
| OBJ-01 | Elevar una tarima de hasta 10 kg | Tiempo de elevación < 15 s | [D] |
| OBJ-02 | Llegar al destino de forma autónoma | Error de llegada < 10 cm | [D] |
| OBJ-03 | Registrar la nueva ubicación al depositar | Latencia depósito → base de datos < 2 s, medida extremo a extremo | [S] |
| OBJ-04 | Ejecutar rutas predefinidas | RUTA_1, RUTA_2 y RUTA_3 sin colisión | [S] |
| OBJ-05 | Operar de forma sostenida | Traslado de 3 min sin reinicio ni corte de energía | [S] |
| OBJ-06 | Cumplir el Reto IoT | ≥ 2 sensores y ≥ 2 actuadores en red, base de datos con Web API, ≥ 5 indicadores en tiempo real | [N] Descripción del Reto IoT (`importado/KOLEO_todo.md` §3) |

## Alcance

**Incluido:** chasis con tracción diferencial y elevación por un actuador lineal; báscula con rechazo por sobrepeso; parada por obstáculo (HC-SR04); firmware ESP32; Raspberry Pi 5 con planificador A*, lectura QR y puente MQTT; contratos MQTT/UART/estados/SQL; backend (MQTT → SQLite → API); tablero React con flotilla, monitoreo, control y gestión logística; robot simulado; pruebas VAL-01 a VAL-08 con evidencia; reporte final. [S]

**Excluido explícitamente:** integración del RPLIDAR al mapa y Google Coral (fuera por DP-11); localización SLAM; replanificación automática tras un obstáculo; operación en almacenes arbitrarios o con cargas de más de 10 kg; autenticación de usuarios en la API; almacenamiento offline y reintentos ante pérdida de Wi-Fi. [S]

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
| Osvaldo Sierra | Coordina la planeación; dueño propuesto de contratos, backend y tablero | G0 y G1 (con el equipo) |
| Miranda Henry, Elías Tamez, Leonardo Alfonzo, Alvaro Alcaraz | Equipo; dueños propuestos por subsistema (SUP-016) | Demos semanales |
| Profesor del curso | Evalúa la entrega del 2-dic | Entrega final; no participa en G0/G1 |

## Supuestos y restricciones

- Fecha de entrega 2-dic-2026 [D].
- Presupuesto $8,000 MXN ±25 %, tope $10,000 MXN [S] (Charter original, importado).
- BOM final al 11-nov-2026 sin piezas nuevas, salvo el fusible de 10 A (DP-10) [S].
- Canal de datos MQTT con broker, publicado por la Raspberry Pi [D].
- Tablero en React + Vite + Tailwind [D].
- Supuestos de impacto en `supuestos.md` (SUP-001 a SUP-018).

## Riesgos iniciales

Ver `05-riesgos.md`. Principales: estado físico del robot, navegación sin lazo cerrado, báscula que devuelve 0 si falla, batería sin protección, tiempo.

## Criterios de cierre

1. VAL-01 a VAL-08 con resultado medido y evidencia enlazada (si una meta no se alcanza, se reporta la medición real, DP-13).
2. Demo completa grabada el 30-nov o 1-dic.
3. Reporte final con evidencia, gasto final y bitácora del robot.
4. Todos los WP de la WBS con dictamen CONFORME, o desviación aceptada por Osvaldo.
