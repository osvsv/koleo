# Contrato del ESP32

El ESP32 y la Pi intercambian los mensajes de abajo. Payload JSON UTF-8, validable contra `mensajes.schema.json`; todos con `ts` (ms desde epoch Unix). Los comandos conservan los nombres del enlace original (`LIFT`, `MOVE`, `STOP`, `DROP`).

| Tema | `$defs` | Publicador | QoS | Retenido |
| --- | --- | --- | --- | --- |
| `koleo/robot1/esp32/cmd` | `esp32_cmd` | Raspberry Pi | 1 | no |
| `koleo/robot1/esp32/resp` | `esp32_resp` | ESP32 | 1 | no |
| `koleo/robot1/esp32/sensores` | `esp32_sensores` | ESP32 | 0 | no |
| `koleo/robot1/esp32/evento` | `esp32_evento` | ESP32 | 1 | no |
| `koleo/robot1/esp32/conexion` | `conexion` | ESP32 (y el broker por testamento) | 1 | sí |

`esp32/conexion`: igual que `conexion` en `mqtt.md`: el ESP32 publica `EN_LINEA` retenido al conectarse y registra como testamento `FUERA_DE_LINEA` retenido, QoS 1, en `koleo/robot1/esp32/conexion`.

## Comandos (`esp32/cmd`)
Campos: `ts`, `id_cmd` (texto, obligatorio; un comando sin `id_cmd` es inválido), `cmd` ∈ LIFT, MOVE, STOP, DROP. `peso_kg` (peso declarado en kg, obligatorio si `cmd` es `LIFT`). Opcionales: `id_tarima`, `pwm_izq`, `pwm_der`, `x_cm`, `y_cm`.

| Comando | Campos usados | Respuesta exitosa (`resp`) | Respuestas de error (`resp`, `resultado` ERR) |
| --- | --- | --- | --- |
| `LIFT` | `id_tarima`, `peso_kg` (peso declarado de la tarima) | `ACK` con `codigo` `LIFT_OK` (peso declarado válido, tarima elevada) | `OVERWEIGHT` (peso declarado sobre el límite de 10 kg), `PESO_INVALIDO` (peso declarado ausente, no numérico o no positivo) |
| `MOVE` | `pwm_izq`, `pwm_der` (o `x_cm`, `y_cm` de destino) | `ACK` con `codigo` `MOVE_OK` | `OBSTACULO_CERCANO` (obstáculo en el camino) |
| `STOP` | ninguno | `ACK` con `codigo` `STOP_OK` | (ninguno) |
| `DROP` | `id_tarima`, `x_cm`, `y_cm` | `ACK` con `codigo` `DROP_OK` | (ninguno) |

Códigos de `esp32_resp.codigo`: `LIFT_OK`, `OVERWEIGHT`, `PESO_INVALIDO`, `OBSTACULO_CERCANO`, y los de acuse `MOVE_OK`, `STOP_OK`, `DROP_OK`. `resultado` es `ACK` si se ejecutó y `ERR` si no. La respuesta repite el `id_cmd` del comando.

## Tiempo de espera
La Pi espera la respuesta con el mismo `id_cmd` **1 s** (1000 ms). Sin respuesta con el mismo `id_cmd` en ese plazo, el comando se reporta como error (`TimeoutError` en la Pi), la Pi intenta enviar `STOP` y la misión no continúa. No hay reintento del comando: el error se reporta a 1 s. Si llega una respuesta tardía, se ignora. Si el ESP32 recibe un `id_cmd` ya atendido, no repite la acción y solo reenvía la respuesta.

## Sensores y eventos
- `esp32/sensores`: `ts`, `distancia_obstaculo_cm`, `enc_izq`, `enc_der` (enteros, cuentas de encoder). Periódico.
- `esp32/evento`: `ts`, `codigo` ∈ LIFT_OK, OVERWEIGHT, PESO_INVALIDO, OBSTACULO_CERCANO, DROP_OK; opcionales `id_tarima`, `peso_kg`. Eventos espontáneos (por ejemplo, OBSTACULO_CERCANO durante un MOVE). La Pi los traduce a `evento` de `mqtt.md` (OVERWEIGHT a SOBREPESO, OBSTACULO_CERCANO a OBSTACULO).
