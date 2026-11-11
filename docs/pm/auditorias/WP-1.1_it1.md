# Auditoría WP-1.1 — iteración 1
Dictamen: NO CONFORME
Commit: 92ff22d1f8833ecf4accd0a7f5321c7894be1ca9
Evidencia: docs/pm/evidencia/WP-1.1_it1_aceptacion_92ff22d.log
Archivos auditados: contratos/mensajes.schema.json, contratos/estados.json, contratos/esquema.sql, contratos/mqtt.md, contratos/esp32.md

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| Interfaz ($schema 2020-12 y los 9 `$defs`) | Cumple | test_interfaz_defs_presentes PASSED; mensajes.schema.json:2, 10-124 |
| CA-1.1.1 | Cumple | 6 pruebas test_ca_1_1_1_* PASSED. telemetria:12 tiene los 8 campos obligatorios y `ts` es entero (:7). En evento:26 el enum de `tipo` (:30) son los 5 valores e `id_evento` es texto de longitud mínima 1 |
| CA-1.1.2 | Cumple | 8 pruebas test_ca_1_1_2_* PASSED. orden:50-59 (if/then de INICIAR exige `ruta` e `id_tarima`); orden_ack:63,67; conexion:73,77 |
| CA-1.1.3 | Cumple | test_ca_1_1_3_sin_ts_es_invalido y test_ca_1_1_3_tipo_desconocido_es_invalido PASSED |
| CA-1.1.4 | Cumple | test_ca_1_1_4_estados_exactos PASSED; estados.json:2-3 trae exactamente 7 estados de robot y 4 de tarima, sin duplicados |
| CA-1.1.5 | Cumple | 6 pruebas test_ca_1_1_5_* PASSED. Comparé esquema.sql:4-38 con docs/pm/importado/KOLEO_Documentacion_General.md:399-433 (§10.2): coinciden columnas y tipos, y se agrega `id_evento VARCHAR(64) NOT NULL UNIQUE` (:18). Hay claves foráneas a `tarimas` (:19, :32) |
| CA-1.1.6 | Cumple (inspección) | mqtt.md:5-11: tabla con los 5 temas, cada uno con publicador, QoS (telemetria 0, el resto 1) y retención (`conexion` = sí). mqtt.md:25-30: testamento en el CONNECT con tema, QoS 1, retain=true y payload FUERA_DE_LINEA; publica EN_LINEA retenido al conectarse |
| CA-1.1.7 | Cumple, pero frágil (ver H-1) | test_ca_1_1_7_esp32_cmd_sin_id_cmd_es_invalido PASSED. esp32.md:7-11 tiene los 5 temas esp32/*; :16 `id_cmd` obligatorio; :18-23 LIFT/MOVE/STOP/DROP con su respuesta ACK y sus errores; :25 los códigos LIFT_OK, OVERWEIGHT, SCALE_FAIL, NO_LOAD y OBSTACULO_CERCANO; :28 tiempo de espera de 1 s (1000 ms). El esquema relaciona esp32/conexion con `$defs/conexion` (mensajes.schema.json:5) |
| CA-1.1.8 | Cumple | 12 pruebas test_ca_1_1_8_* PASSED. esp32_cmd:82-91, esp32_resp:96-101, esp32_sensores:106-112, esp32_evento:117-122; evento allOf:41-46 (DROP_OK exige 6 campos, SOBREPESO exige `peso_kg`) |

Resultado de las pruebas: el log del orquestador (commit 92ff22d, árbol limpio) termina en "62 failed, 37 passed, 8 errors" y no tiene ninguna línea FAILED ni ERROR de test_wp_1_1.py. Ese archivo tiene exactamente 37 casos. Como el log está en modo -q y no nombra los casos que pasan, se confirmó con `python -m pytest tests/aceptacion/test_wp_1_1.py -v -p no:cacheprovider`: "collected 37 items ... 37 passed in 0.19s". Los fallos de otros WP son ModuleNotFoundError (`simulador`, `backend`, `pi`) porque esos módulos aún no existen; no son atribuibles a este WP.

## Hallazgos

### H-1 [Menor] La política de tiempo de espera de esp32.md permite un reintento que contradice el error a 1 s de la línea base
- Criterio o requisito afectado: CA-1.1.7 (tiempo de espera de 1 s). También choca con REQ-F-005 ("si la Pi no recibe respuesta a un comando en 1 s, lo reporta como error"), EJ-009 ("a 1 s hay un error de tiempo de espera y no continúa la misión"), CA-3.2.2 (sin respuesta en 1 s se lanza `TimeoutError` y se intenta `STOP`) y CA-4.3.6 (con TimeoutError la misión se aborta con `STOP`).
- Evidencia: contratos/esp32.md:28 dice: "Sin respuesta en ese plazo, considera el comando fallido y puede reintentar con el mismo `id_cmd` una vez [...] Tras el segundo fallo la Pi pasa el robot a `ERROR`." Por contrato, el error queda en unos 2 s y la misión puede seguir después del primer vencimiento. Además, el contrato no menciona el `STOP` al vencer el plazo. Este documento es la fuente que consumen WP-3.2 y WP-4.3, así que un ejecutor que lo siga puede apartarse de esos criterios.
- Qué tendría que ser cierto para cerrarlo: esp32.md debe decir que, sin respuesta con el mismo `id_cmd` en 1 s, el comando se reporta como error (TimeoutError en la Pi), se intenta `STOP` y la misión no continúa. Hay que quitar el reintento o dejarlo explícitamente fuera del plazo de 1 s, sin retrasar el reporte del error.

### H-2 [Observación] `esp32_resp.codigo` es texto libre en el esquema
- Criterio o requisito afectado: CA-1.1.7 y CA-1.1.8 (no se incumplen: CA-1.1.8 solo exige que `codigo` sea obligatorio).
- Evidencia: mensajes.schema.json:101 usa `$ref texto` y deja la lista de códigos solo en la descripción. Un código mal escrito, por ejemplo "OVERWIEGHT", valida igual.
- Qué tendría que ser cierto para cerrarlo (opcional): un `enum` con los 8 códigos de esp32.md:25 (LIFT_OK, OVERWEIGHT, SCALE_FAIL, NO_LOAD, OBSTACULO_CERCANO, MOVE_OK, STOP_OK, DROP_OK).

## Alcance, integridad y regresión
- Alcance: `git show --stat 2b70ef2` muestra solo 5 archivos, todos dentro de `contratos/**`, que es el Alcance de archivos del WP. No se tocó nada fuera de alcance.
- Integridad: el commit del WP no toca `docs/pm/` ni `tests/`. El commit posterior 92ff22d ("[pm] ejecucion WP-1.1 it1") solo agrega docs/pm/auditorias/WP-1.1_it1_ejecucion.md y es del orquestador. HEAD es 92ff22d, el mismo commit que registra el log, con árbol limpio según el log.
- Coherencia con supuestos: SUP-012 (telemetría a 2 Hz) coincide con mqtt.md:7. SUP-013 (7 estados) coincide con estados.json. SUP-001 (ESP32 por MQTT, sin UART) coincide con los temas esp32/*. SUP-023 coincide con el CHECK de `tarimas.estado` (esquema.sql:12).
- Regresión: no hay. Es el primer WP implementado y ninguna prueba que antes pasara falla ahora.
- Credenciales: no hay ninguna en los archivos del commit.

## Hallazgos de iteraciones previas: cerrados / persistentes
No aplica (iteración 1).
