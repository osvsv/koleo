# WP-1.1 — Informe del ejecutor, iteración 1

Resultado: COMPLETO

## Archivos creados (alcance `contratos/**`)
- `contratos/mensajes.schema.json`: JSON Schema 2020-12 con los 9 `$defs` de la interfaz y auxiliares `ts`, `texto` y `estado_robot`.
- `contratos/estados.json`: 7 estados de robot y 4 de tarima.
- `contratos/esquema.sql`: `tarimas`, `historial_movimientos` y `registro_rechazos_seguridad`.
- `contratos/mqtt.md`
- `contratos/esp32.md`

## Pruebas
`test_wp_1_1.py`: 37 passed, 0 failed (autoverificación del ejecutor; el orquestador regenera la evidencia).

## Autoverificación por criterio
- CA-1.1.1: `telemetria` con 8 campos obligatorios y `ts` entero; `evento` con `tipo` en {LIFT_OK, SOBREPESO, OBSTACULO, DROP_OK, ERROR}, `id_evento` e `id_tarima`.
- CA-1.1.2: `orden` exige `ts`, `id_orden`, `tipo`; INICIAR exige además `ruta` e `id_tarima` (`if/then`); `orden_ack` y `conexion` con sus enums.
- CA-1.1.3: sin `ts` o con `tipo` desconocido es inválido.
- CA-1.1.4: `estados.json` con exactamente los estados pedidos.
- CA-1.1.5: tres tablas con las columnas de §10.2; `historial_movimientos.id_evento` UNIQUE y NOT NULL; claves foráneas a `tarimas`.
- CA-1.1.6: por inspección de `mqtt.md`: 5 temas con publicador, suscriptor y QoS (telemetria 0, el resto 1); `conexion` retenida con testamento (tema, QoS 1, retain, payload FUERA_DE_LINEA); idempotencia de `id_evento`.
- CA-1.1.7: por inspección de `esp32.md` y del esquema: 5 temas `esp32/*`, comandos LIFT/MOVE/STOP/DROP con `id_cmd`, respuestas LIFT_OK, OVERWEIGHT, SCALE_FAIL, NO_LOAD, OBSTACULO_CERCANO y tiempo de espera de 1 s; `esp32_cmd` sin `id_cmd` es inválido.
- CA-1.1.8: `esp32_cmd`, `esp32_resp`, `esp32_sensores`, `esp32_evento` con los campos y enums del criterio; DROP_OK exige los 6 campos extra y SOBREPESO exige `peso_kg` (`allOf` con `if/then`).

## Desviaciones
Ninguna.

## Bloqueos o contradicciones con la línea base
Ninguno.

## Ambigüedades de la línea base reportadas por el ejecutor
1. `esp32_resp.codigo` no tiene vocabulario cerrado más allá de los cinco códigos del criterio; se dejó como texto libre. En `esp32.md` se añadieron los acuses `MOVE_OK`, `STOP_OK` y `DROP_OK` y se asignó qué código de error corresponde a cada comando (decisión del ejecutor).
2. QoS elegidos por el ejecutor: 0 para telemetría y sensores, 1 para el resto (sin fuente).
3. Política de reintento propuesta por el ejecutor: un reintento con el mismo `id_cmd`, luego ERROR (la fuente solo fija el tiempo de espera de 1 s).
4. Tipos SQL según lo "mostrado" en §10.2; el ejecutor añadió un CHECK de `tarimas.estado` contra los 4 estados y `PRAGMA foreign_keys = ON`.
5. `telemetria.estado` restringido al enum de estados de robot.

## Variables de entorno nuevas
Ninguna.

## Sugerencias fuera de alcance
`robot_id` debería distinguir Pi de ESP32 cuando se publiquen `esp32/conexion` y `conexion`; el esquema reutiliza el mismo `$defs` `conexion`.
