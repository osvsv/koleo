# WP-1.1 — informe de ejecución, iteración 3 (reapertura por CC-004)

Resultado: TERMINADO

Archivos creados o modificados:
- `contratos/mensajes.schema.json`:
  - `esp32_cmd`: propiedad `peso_kg` y `if/then` que la exige cuando `cmd` es LIFT.
  - `esp32_resp.codigo`: LIFT_OK, OVERWEIGHT, PESO_INVALIDO, OBSTACULO_CERCANO, MOVE_OK, STOP_OK, DROP_OK.
  - `esp32_sensores`: `peso_kg` ya no es obligatorio.
  - `esp32_evento.codigo`: LIFT_OK, OVERWEIGHT, PESO_INVALIDO, OBSTACULO_CERCANO, DROP_OK.
- `contratos/esp32.md`: documenta `peso_kg` como peso declarado, obligatorio en LIFT; LIFT usa PESO_INVALIDO sin mención de celda de carga; DROP sin errores (antes NO_LOAD); listas de códigos y campos de sensores actualizadas.
- `contratos/mqtt.md`: sin cambios (su `peso_kg` es el de la telemetría de robot).

Autoverificación (del ejecutor):
- grep de SCALE_FAIL y NO_LOAD en `contratos/`: 0 coincidencias.
- pytest filtrado con `-k "1_1"`: 39 pruebas de `test_wp_1_1.py`, 0 fallas. Las 2 fallas de la corrida completa son de `test_wp_4_1.py` (`pi.puente_mqtt` aún no existe), de otro WP.

Desviaciones: ninguna.
Bloqueos o contradicciones con la línea base: ninguno.
Variables de entorno nuevas: ninguna.

Sugerencias fuera de alcance:
- Observación H-2 (`esp32_resp.codigo` es texto libre): no se atendió; el ejecutor no tenía su texto. Si se quiere, se estrecha por comando con `if/then`.
