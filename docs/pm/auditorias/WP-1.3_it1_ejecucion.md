# WP-1.3 it1 — informe de ejecución

Resultado: código terminado; pruebas de aceptación 13 passed (corridas por el orquestador en PowerShell; el hook bloquea pytest en Bash). CA-1.3.9 pendiente de captura humana con broker.

Archivos: backend/__init__.py, backend/koleo/{__init__,ingesta,api,suscriptor}.py (sin commit: el WP quedó bloqueado).

## Desviaciones
| Archivo o criterio | Categoría | Nota |
| --- | --- | --- |
| tablas `robots`, `ordenes`, `eventos_vistos` | aprendizaje | `esquema.sql` no tiene tabla para órdenes ni robots; el WP exige que orden/ack actualice la orden y GET /api/robots. Tablas auxiliares con CREATE TABLE IF NOT EXISTS en backend/. Decidir si el esquema canónico las incluye. |
| `ruta_ejecutada` | aprendizaje | Se guarda el nombre ("RUTA_1"); la línea base no define el formato. |
| `ubicacion_nodo` | aprendizaje | Queda NULL; no hay formato ni dato en el evento. |
| Indicadores (GET /api/indicadores) | aprendizaje | Cálculos no definidos; supuestos: ocupacion = ubicadas/total de tarimas; posicion_robot = última telemetría; tiempo_ciclo_s = ts DROP_OK − ts LIFT_OK; precision_cm = distancia entre última posición telemetrada y destino del DROP_OK; peso_kg = último peso de telemetría; alertas = total de rechazos + 5 recientes. |
| Rechazo SOBREPESO | aprendizaje | coord_x_cm/coord_y_cm salen de la última posición del robot (NULL si no hay); el evento no trae coordenadas. |
| `latencia_red_ms` | aprendizaje | Se guarda cruda (recibido − ts) aunque salga negativa por relojes desfasados; CA-1.3.2 pide ≥ 0. |
| POST /api/ordenes | alcance | No está en la interfaz del WP; prescindible. |
| Pytest en Bash | defecto | Bloqueado por el hook; corrido por el orquestador. |

Variables de entorno nuevas: KOLEO_MQTT_HOST, KOLEO_DB_PATH, KOLEO_API_HOST, KOLEO_API_PORT (reutiliza KOLEO_MQTT_PORT/USER/PASSWORD).

Comando para capturar CA-1.3.9 (Mosquitto corriendo, desde la raíz, PowerShell):
1. `$env:KOLEO_DB_PATH="koleo_demo.db"; .venv\Scripts\python.exe -m backend.koleo.suscriptor --broker localhost`
2. En otra terminal: `.venv\Scripts\python.exe -m simulador.robot_falso --ruta RUTA_1 --peso 8.45 --broker localhost` (luego RUTA_2 11.80 y RUTA_3 6.20).
3. Consultar tarimas, historial_movimientos y registro_rechazos_seguridad de koleo_demo.db.
Guardar salidas en docs/pm/evidencia/WP-1.3/corrida_con_broker.txt.
