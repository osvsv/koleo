# Registro de supuestos

| ID | Supuesto | Afecta a | Dependientes | Estado | Validado en |
| --- | --- | --- | --- | --- | --- |
| SUP-016 | La asignación de dueños por subsistema (Álvaro mecánica, Miranda electrónica, Leo firmware, Elías Pi, Osvaldo datos y tablero) y las horas disponibles por persona alcanzan para las 3 semanas; ambas cosas están sin confirmar | WP-1.1, WP-1.2, WP-1.3, WP-2.1, WP-2.2, WP-2.3, WP-2.4, WP-3.1, WP-3.2, WP-3.3, WP-4.1, WP-4.2, WP-4.3, WP-4.4, WP-5.1, WP-5.2, WP-6.1, WP-6.2, WP-6.3 | 19 | Pendiente | — |
| SUP-008 | El hardware del BOM del 11-nov está disponible y los WP físicos los ejecutan personas, con evidencia guardada (DP-09) | WP-2.1, WP-2.2, WP-2.3, WP-2.4, WP-3.1, WP-3.3, WP-6.1, WP-6.2, WP-6.3 | 9 | Pendiente | — |
| SUP-007 | El lenguaje de backend, Pi y simulador es Python, con pytest; las versiones de paquetes se fijan en el primer WP que las use | WP-1.2, WP-1.3, WP-3.2, WP-4.1, WP-4.2, WP-4.3, WP-4.4, WP-5.2 | 8 | Pendiente | — |
| SUP-006 | Backend en Flask con SQLite; broker Mosquitto (dónde corre, Pi o laptop, está por definir) | REQ-F-008, REQ-F-011, WP-1.3, WP-4.1, WP-5.1, WP-5.2 | 6 | Pendiente | — |
| SUP-001 | La Raspberry Pi cuenta como "microcontrolador en red" para el Reto IoT; el ESP32 no se conecta por Wi-Fi | REQ-F-009, REQ-F-011, REQ-NF-006, WP-1.3, WP-4.1 | 5 | Pendiente | — |
| SUP-005 | El HC-SR04 es el sensor de paro; RPLIDAR y Google Coral quedan fuera (DP-11) | REQ-F-004, REQ-F-006, WP-2.4, WP-3.3, WP-4.3 | 5 | Pendiente | — |
| SUP-009 | Mapa 5×6, celdas de 30 cm, rutas RUTA_1..3 de la Documentación General §8, piso liso | REQ-F-006, REQ-NF-001, WP-4.2, WP-4.3, WP-6.2 | 5 | Pendiente | — |
| SUP-010 | El límite de 10 kg es inclusivo: 10.0 kg se acepta y 10.1 kg se rechaza | REQ-F-001, REQ-F-002, WP-1.2, WP-3.1, WP-6.1 | 5 | Pendiente | — |
| SUP-012 | La telemetría se publica a 2 Hz en los cinco temas `koleo/robot1/*` del plan importado | REQ-F-009, WP-1.1, WP-1.2, WP-4.1, WP-5.1 | 5 | Pendiente | — |
| SUP-002 | El profesor acepta las metas <15 s y <10 cm que decidió Osvaldo | REQ-NF-001, REQ-NF-002, WP-6.1, WP-6.2 | 4 | Pendiente | — |
| SUP-013 | Los estados unificados del plan importado (robot y tarima) son los correctos | REQ-F-010, WP-1.1, WP-1.3, WP-5.1 | 4 | Pendiente | — |
| SUP-003 | El umbral de paro es 15 cm con respuesta <200 ms (la presentación decía 12 cm, el plan importado 15 cm) | REQ-F-004, WP-3.3, WP-6.1 | 3 | Pendiente | — |
| SUP-011 | La latencia se mide desde que la celda detecta la tarima suelta hasta que la fila queda en la BD | REQ-NF-003, WP-1.3, WP-6.1 | 3 | Pendiente | — |
| SUP-014 | Sin QR legible o con formato distinto de `TAR-NNN`, la misión no inicia | REQ-F-007, WP-4.4, WP-4.3 | 3 | Pendiente | — |
| SUP-015 | El tablero se actualiza por consulta cada 1 s y no por WebSocket | REQ-F-012, WP-5.1, WP-5.2 | 3 | Pendiente | — |
| SUP-018 | Los cierres de incremento son 20-nov, 27-nov y 30-nov/1-dic (DP-12) | Incrementos 1, 2 y 3 | 3 | Pendiente | — |
| SUP-004 | Fusible de 10 A en la línea de la batería y sin paro de emergencia físico (DP-10) | REQ-NF-005, WP-2.3 | 2 | Pendiente | — |
| SUP-017 | La reductora da 515 pulsos por vuelta y la rueda mide 65 mm | REQ-F-006, WP-4.2 | 2 | Pendiente | — |
