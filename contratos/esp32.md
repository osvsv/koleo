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
Campos: `ts`, `id_cmd` (texto, obligatorio; un comando sin `id_cmd` es inválido), `cmd` ∈ LIFT, MOVE, STOP, DROP. Opcionales: `id_tarima`, `pwm_izq`, `pwm_der`, `x_cm`, `y_cm`.

| Comando | Campos usados | Respuesta exitosa (`resp`) | Respuestas de error (`resp`, `resultado` ERR) |
| --- | --- | --- | --- |
| `LIFT` | `id_tarima` | `ACK` con `codigo` `LIFT_OK` (celda leída, carga válida, elevada) | `OVERWEIGHT` (peso sobre el límite de 10 kg), `SCALE_FAIL` (la celda no responde o lectura inválida), `NO_LOAD` (no hay carga en la plataforma) |
| `MOVE` | `pwm_izq`, `pwm_der` (o `x_cm`, `y_cm` de destino) | `ACK` con `codigo` `MOVE_OK` | `OBSTACULO_CERCANO` (obstáculo en el camino) |
| `STOP` | ninguno | `ACK` con `codigo` `STOP_OK` | (ninguno) |
| `DROP` | `id_tarima`, `x_cm`, `y_cm` | `ACK` con `codigo` `DROP_OK` | `NO_LOAD` |

Códigos de `esp32_resp.codigo`: `LIFT_OK`, `OVERWEIGHT`, `SCALE_FAIL`, `NO_LOAD`, `OBSTACULO_CERCANO`, y los de acuse `MOVE_OK`, `STOP_OK`, `DROP_OK`. `resultado` es `ACK` si se ejecutó y `ERR` si no. La respuesta repite el `id_cmd` del comando.

## Tiempo de espera
La Pi espera la respuesta con el mismo `id_cmd` **1 s** (1000 ms). Sin respuesta en ese plazo, considera el comando fallido y puede reintentar con el mismo `id_cmd` una vez; el ESP32 no repite la acción si recibe un `id_cmd` ya atendido, solo reenvía la respuesta. Tras el segundo fallo la Pi pasa el robot a `ERROR`.

## Sensores y eventos
- `esp32/sensores`: `ts`, `peso_kg`, `distancia_obstaculo_cm`, `enc_izq`, `enc_der` (enteros, cuentas de encoder). Periódico.
- `esp32/evento`: `ts`, `codigo` ∈ LIFT_OK, OVERWEIGHT, SCALE_FAIL, NO_LOAD, OBSTACULO_CERCANO, DROP_OK; opcionales `id_tarima`, `peso_kg`. Eventos espontáneos (por ejemplo, OBSTACULO_CERCANO durante un MOVE). La Pi los traduce a `evento` de `mqtt.md` (OVERWEIGHT a SOBREPESO, OBSTACULO_CERCANO a OBSTACULO).
