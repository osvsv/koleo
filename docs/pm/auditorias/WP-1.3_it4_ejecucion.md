# WP-1.3 — informe de ejecución, iteración 4 (reapertura por CC-005)

Resultado: BLOQUEADO por desviaciones de aprendizaje (implementación terminada, sin auditar)

Archivos modificados:
- `backend/koleo/ingesta.py`: la tabla `robots` tiene `velocidad_cm_s`, con migración `ALTER TABLE` en `asegurar_tablas` si falta; la telemetría guarda la velocidad; nueva tabla `rechazos_robot(id_alerta, robot_id)`, llenada en cada SOBREPESO con el `lastrowid` del rechazo; el tema se valida con la regex `koleo/robot<id>/<sufijo>` en vez del prefijo fijo `koleo/robot1/`.
- `backend/koleo/api.py`: `GET /api/robots` devuelve además `velocidad_cm_s`, `ruta_actual` (ruta de la última orden INICIAR con estado `aceptada`, solo si el robot está en EN_MISION, ELEVANDO, EN_RUTA o DEPOSITANDO; si no, null) y `alertas` (hasta 5 rechazos de ese robot, el más reciente primero); BD vacía → `[]` con 200.

Autoverificación (pytest, no lectura manual): `.venv/Scripts/python.exe -m pytest -q -k "1_3 or 1_1 or 1_2"`, 75 pasan y 12 fallan; los 12 son de `test_wp_4_1.py` (`ModuleNotFoundError: pi.ordenes`, WP-4.1). Pasan todas las de WP-1.1, 1.2 y 1.3, incluidas las 5 nuevas `test_ca_1_3_13_*`. No se ejecutó CA-1.3.9 (broker real).

Desviaciones:
| Archivo o criterio | Categoría | Nota |
| --- | --- | --- |
| backend/koleo/ingesta.py, validación de tema | aprendizaje | `contratos/mqtt.md` fija el prefijo `koleo/robot1/`. `test_ca_1_3_13_robots_alertas_por_robot` publica telemetría en `koleo/robot2/telemetria` y espera ver `robot2`; con el prefijo fijo la ingesta la descartaba. Se aceptó `koleo/robot<id>/…`; los temas `esp32/*` siguen descartados. Conviene que el plan o el contrato reflejen este soporte multirobot |
| `ruta_actual` | aprendizaje | `orden_ack` no trae `robot_id`: no se puede ligar una orden a un robot. Se usa la última INICIAR aceptada global (por `ts_ack`) para cualquier robot en misión. Correcto con un solo robot; con varios daría la misma ruta a todos |

Bloqueos: ninguno. Variables de entorno nuevas: ninguna.
