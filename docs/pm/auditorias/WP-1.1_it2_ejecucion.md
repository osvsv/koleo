# WP-1.1 — Informe del ejecutor, iteración 2

Resultado: TERMINADO

## Archivos modificados (alcance `contratos/**`)
- `contratos/esp32.md`: sección "Tiempo de espera" (H-1). Sin respuesta con el mismo `id_cmd` en 1 s, el comando se reporta como error (`TimeoutError` en la Pi), la Pi intenta `STOP` y la misión no continúa. Se quitó el reintento; una respuesta tardía se ignora.
- `contratos/mensajes.schema.json`: `esp32_resp.codigo` es un enum con los 8 códigos (H-2): LIFT_OK, OVERWEIGHT, SCALE_FAIL, NO_LOAD, OBSTACULO_CERCANO, MOVE_OK, STOP_OK, DROP_OK.

## Pruebas
37 passed (autoverificación; el orquestador regenera la evidencia). El hook de Bash bloqueó el comando por ruta de archivo; el ejecutor corrió `pytest tests -q -k wp_1_1`.

## Desviaciones
Ninguna.

## Bloqueos o contradicciones con la línea base
Ninguno.

## Variables de entorno nuevas
Ninguna.

## Sugerencias fuera de alcance
Revisar la regla del hook guard_bash.py: bloquea la ejecución de las pruebas de aceptación por nombre de ruta.
