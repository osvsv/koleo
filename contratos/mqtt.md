# Contrato MQTT (Pi, backend, tablero)

Prefijo de todos los temas: `koleo/robot1/`. Payload: JSON UTF-8 validable contra `mensajes.schema.json` (`$defs` indicado). Todo mensaje lleva `ts` (entero, milisegundos desde epoch Unix UTC); con él se mide la latencia extremo a extremo (VAL-07). Los estados salen de `estados.json`; las tablas, de `esquema.sql`.

| Tema | `$defs` | Publicador | Suscriptor | QoS | Retenido |
| --- | --- | --- | --- | --- | --- |
| `koleo/robot1/telemetria` | `telemetria` | Raspberry Pi, 2 veces por segundo | backend, tablero | 0 | no |
| `koleo/robot1/evento` | `evento` | Raspberry Pi | backend, tablero | 1 | no |
| `koleo/robot1/orden` | `orden` | Backend o tablero | Raspberry Pi | 1 | no |
| `koleo/robot1/orden/ack` | `orden_ack` | Raspberry Pi | backend, tablero | 1 | no |
| `koleo/robot1/conexion` | `conexion` | Raspberry Pi (y el broker, por testamento) | backend, tablero | 1 | **sí** |

## telemetria
Campos: `ts`, `robot_id`, `x_cm`, `y_cm`, `velocidad_cm_s`, `estado` (estado de robot), `peso_kg`, `distancia_obstaculo_cm`. Es periódica; perder un mensaje no importa (QoS 0).

## evento
`tipo` ∈ LIFT_OK, SOBREPESO, OBSTACULO, DROP_OK, ERROR. Campos comunes: `ts`, `robot_id`, `tipo`, `id_evento` (texto único), `id_tarima`.
- `DROP_OK` exige además `peso_kg`, `x_cm`, `y_cm` (destino), `ruta`, `origen_x_cm`, `origen_y_cm`.
- `SOBREPESO` exige además `peso_kg`.
- Idempotencia (REQ-F-017): cada entrega lleva un `id_evento` único. Por QoS 1 puede haber reenvíos con el mismo `id_evento`; el backend los descarta (`UNIQUE` en `historial_movimientos.id_evento`). Dos entregas de la misma tarima con `id_evento` distintos generan dos filas. Un DROP_OK sin `id_evento` es inválido y se descarta.

## orden y orden/ack
`orden`: `ts`, `id_orden`, `tipo` ∈ INICIAR, CANCELAR, PARO. INICIAR exige además `ruta` e `id_tarima`. Cada orden tiene un `id_orden` y la Pi responde en `orden/ack` con `id_orden` y `resultado` ∈ aceptada, rechazada (`motivo` opcional). Una orden sin ack se considera no confirmada.

## conexion (retenido con testamento)
Mensaje `conexion`: `ts`, `robot_id`, `estado` ∈ EN_LINEA, FUERA_DE_LINEA.
- Al conectarse al broker, la Pi publica `EN_LINEA` en `koleo/robot1/conexion` con retención activa (`retain=true`) y QoS 1.
- **Testamento (Last Will)** registrado en el CONNECT de la Pi: tema `koleo/robot1/conexion`, QoS 1, `retain=true`, payload `{"ts": <ts al conectar>, "robot_id": "robot1", "estado": "FUERA_DE_LINEA"}`. Si la Pi cae sin desconexión limpia, el broker publica `FUERA_DE_LINEA` retenido.
- Un suscriptor nuevo recibe de inmediato el último estado retenido.
- En desconexión limpia la Pi publica `FUERA_DE_LINEA` retenido antes de cerrar.

## Temas del ESP32
Los temas `koleo/robot1/esp32/*` están en `esp32.md`.
