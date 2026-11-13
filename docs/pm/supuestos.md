# Registro de supuestos

Actualizado en G1 (2026-11-11). Estados: Pendiente · Confirmado · Corregido. Ordenado por Dependientes.

| ID | Supuesto | Afecta a | Dependientes | Estado | Validado en |
| --- | --- | --- | --- | --- | --- |
| SUP-016 | El trabajo se reparte por tareas, sin dueños por subsistema (todos pueden trabajar en todo); la capacidad es de 4 a 6 h por semana por persona (≈ 60 a 90 h de equipo hasta el 2-dic), menor que la supuesta y insuficiente para el plan completo sin recortes | WP-1.1, WP-1.2, WP-1.3, WP-2.1, WP-2.2, WP-2.3, WP-2.4, WP-3.1, WP-3.2, WP-3.3, WP-4.1, WP-4.2, WP-4.3, WP-4.4, WP-5.1, WP-5.2, WP-6.1, WP-6.2, WP-6.3 | 19 | Corregido | G1 V-01 y V-02 (Osvaldo, 2026-11-11) |
| SUP-008 | El hardware del BOM del 11-nov está completo y en poder del equipo | WP-2.1, WP-2.2, WP-2.3, WP-2.4, WP-3.1, WP-3.3, WP-6.1, WP-6.2, WP-6.3 | 9 | Confirmado | G1 V-03 (Osvaldo, 2026-11-11) |
| SUP-019 | Los WP físicos los ejecutan personas, con evidencia guardada que el auditor inspecciona (DP-09) | WP-2.1, WP-2.2, WP-2.3, WP-2.4, WP-3.1, WP-3.3, WP-6.1, WP-6.2, WP-6.3 | 9 | Pendiente | — |
| SUP-007 | El lenguaje de backend, Pi y simulador es Python | WP-1.2, WP-1.3, WP-3.2, WP-4.1, WP-4.2, WP-4.3, WP-4.4, WP-5.2 | 8 | Confirmado | G1 V-04 (Osvaldo, 2026-11-11) |
| SUP-020 | pytest es el framework de pruebas; las versiones de los paquetes se fijan en el primer WP que los use | WP-1.2, WP-1.3, WP-3.2, WP-4.1, WP-4.2, WP-4.3, WP-4.4, WP-5.2 | 8 | Pendiente | — |
| SUP-006 | El backend es Flask con SQLite y corre en la Pi o en una laptop (por definir) | REQ-F-008, REQ-F-011, WP-1.3, WP-4.1, WP-5.1, WP-5.2 | 6 | Pendiente | — |
| SUP-001 | El ESP32 y la Pi se conectan ambos a la red por Wi-Fi; no hay UART entre ellos; los comandos y datos del ESP32 viajan por MQTT y la Pi los consolida hacia los temas del contrato | REQ-F-005, REQ-F-009, REQ-NF-006, WP-1.1, WP-3.2, WP-4.1 | 6 | Confirmado | G1 V-06 (Osvaldo, 2026-11-11) |
| SUP-010 | El límite de sobrepeso es 10 kg, inclusivo (10.0 se acepta), y se verifica con el peso declarado de la tarima (CC-004), sin cargar físicamente más de 100 g | REQ-F-001, REQ-F-002, REQ-NF-009, WP-1.2, WP-3.1, WP-6.1 | 6 | Corregido | G1 V-11 y aclaración (Osvaldo, 2026-11-11) |
| SUP-005 | El HC-SR04 es el sensor de paro; RPLIDAR y Google Coral quedan fuera (DP-11) | REQ-F-004, REQ-F-006, WP-2.4, WP-3.3, WP-4.3 | 5 | Confirmado | G1 V-07 (Osvaldo, 2026-11-11) |
| SUP-009 | El mapa 5×6, las celdas de 30 cm y las tres rutas son de referencia, no criterio de evaluación; piso liso | REQ-F-006, REQ-NF-001, WP-4.2, WP-4.3, WP-6.2 | 5 | Corregido | G1 V-10 (Osvaldo, 2026-11-11) |
| SUP-012 | La telemetría se publica a 2 Hz en los cinco temas `koleo/robot1/*` del plan importado | REQ-F-009, WP-1.1, WP-1.2, WP-4.1, WP-5.1 | 5 | Pendiente | — |
| SUP-002 | Las metas oficiales son <15 s y <10 cm, con carga de demostración de 100 g | REQ-NF-001, REQ-NF-002, WP-6.1, WP-6.2 | 4 | Confirmado | G1 V-17 (Osvaldo, 2026-11-11) |
| SUP-013 | Los siete estados del robot del plan importado (INACTIVO, EN_MISION, ELEVANDO, EN_RUTA, DEPOSITANDO, DETENIDO_OBSTACULO, ERROR) son los correctos | REQ-F-010, WP-1.1, WP-1.3, WP-5.1 | 4 | Pendiente | — |
| SUP-023 | Una tarima queda UBICADA_DESTINO tras depositarse y EN_PISO cuando solo está registrada | REQ-F-008, REQ-F-010, WP-1.1, WP-1.3 | 4 | Confirmado | G1 V-14 (Osvaldo, 2026-11-11) |
| SUP-024 | El broker Mosquitto corre en la Raspberry Pi | WP-1.3, WP-3.2, WP-4.1, WP-5.1 | 4 | Confirmado | G1 V-05 (Osvaldo, 2026-11-11) |
| SUP-003 | El umbral de paro por obstáculo es 15 cm | REQ-F-004, WP-3.3, WP-6.1 | 3 | Confirmado | G1 V-09 (Osvaldo, 2026-11-11) |
| SUP-011 | La latencia se mide desde que la Pi envía el comando `DROP` hasta que la fila queda en la BD | REQ-NF-003, WP-4.1, WP-6.1 | 3 | Corregido | Osvaldo, CC-004 (2026-11-13); antes, desde que la celda detectaba la tarima suelta (G1 V-15) |
| SUP-014 | Sin QR legible, la misión no inicia; el formato `TAR-NNN` es un criterio adicional del modelo | REQ-F-007, WP-4.4, WP-4.3 | 3 | Confirmado | G1 V-16 (Osvaldo, 2026-11-11), solo el comportamiento sin lectura |
| SUP-015 | El tablero se actualiza por consulta cada 1 s y no por WebSocket | REQ-F-012, WP-5.1, WP-5.2 | 3 | Pendiente | — |
| SUP-018 | Solo la entrega final tiene fecha (tentativa 2-dic); no hay revisiones parciales del profesor y los cierres de incremento son internos | Incrementos 1, 2 y 3 | 3 | Corregido | G1 V-19 (Osvaldo, 2026-11-11) |
| SUP-022 | La respuesta de paro ante un obstáculo es menor a 200 ms | REQ-NF-011, WP-3.3, WP-6.1 | 3 | Pendiente | — |
| SUP-027 | Retirado por CC-004: `PESO_SIM` ya no existe; el rechazo por sobrepeso se prueba con el peso declarado en el comando `LIFT` (SUP-029) | REQ-F-002, WP-3.1, WP-6.1 | 0 | Corregido | Osvaldo, CC-004 (2026-11-13) |
| SUP-029 | El peso declarado de cada tarima es el que se registra en el tablero (`POST /api/tarimas`); al iniciar una misión la Pi lo lee de `GET /api/tarimas` y lo envía en `LIFT`, y el ESP32 rechaza lo que pasa de 10 kg o no es válido | REQ-F-001, REQ-F-002, REQ-F-003, WP-3.1, WP-3.2, WP-4.1, WP-4.3 | 4 | Pendiente | — |
| SUP-030 | El `ts` del evento DROP_OK que publica la Pi es la marca del comando `DROP` que lo originó, para que `latencia_red_ms` del backend mida desde el comando sin cambiar el WP-1.3 | REQ-NF-003, WP-4.1, WP-1.3 | 3 | Pendiente | — |
| SUP-004 | Fusible de 10 A en la línea de la batería y sin paro de emergencia físico (DP-10); decisión abierta | REQ-NF-005, WP-2.3 | 2 | Pendiente | G1 V-08 quedó pendiente (Osvaldo, 2026-11-11) |
| SUP-017 | La reductora da 515 pulsos por vuelta y la rueda mide 65 mm | REQ-F-006, WP-4.2 | 2 | Pendiente | — |
| SUP-025 | El ESP32 sigue alimentado por un cable USB desde la Pi, solo como energía (sin datos) | WP-2.3, WP-3.2 | 2 | Pendiente | — |
| SUP-026 | Retirado por CC-004: ya no hay báscula, calibración ni detección de "sin carga" | WP-3.1 | 0 | Corregido | Osvaldo, CC-004 (2026-11-13) |
| SUP-028 | Si falta tiempo, el orden de recorte es WP-5.2 (control y gestión), WP-4.4 (QR) y rutas 2 y 3 | WP-5.2, WP-4.4 | 2 | Pendiente | — |
