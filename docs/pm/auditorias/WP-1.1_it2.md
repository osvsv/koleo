# Auditoría WP-1.1 — iteración 2
Dictamen: CONFORME
Commit: 7229b5ec1cecbbc8501c5a71c3fc6362c8e3b175
Evidencia: docs/pm/evidencia/WP-1.1_it2_aceptacion_7229b5e.log
Archivos auditados: contratos/mensajes.schema.json, contratos/estados.json, contratos/esquema.sql, contratos/mqtt.md, contratos/esp32.md

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| Interfaz ($schema 2020-12 y los 9 `$defs`) | Cumple | test_interfaz_defs_presentes está en los 37 casos que pasan. El commit fc54e11 no toca la estructura de `$defs`: solo cambia mensajes.schema.json:101 |
| CA-1.1.1 | Cumple | Log, línea 1360: "62 failed, 37 passed, 8 errors". El log no tiene ninguna línea FAILED ni ERROR de test_wp_1_1.py, y la línea 8 empieza con 37 puntos, que son los casos de test_wp_1_1.py, el primer archivo de la colección. telemetria y evento no cambiaron desde la iteración 1 |
| CA-1.1.2 | Cumple | Igual que en la fila anterior: orden, orden_ack y conexion no cambiaron |
| CA-1.1.3 | Cumple | Igual que en la fila anterior |
| CA-1.1.4 | Cumple | contratos/estados.json no cambió (git diff 92ff22d..HEAD --stat). Sus pruebas pasan |
| CA-1.1.5 | Cumple | contratos/esquema.sql no cambió. Sus pruebas pasan |
| CA-1.1.6 | Cumple (inspección) | contratos/mqtt.md no cambió desde la inspección de la iteración 1 |
| CA-1.1.7 | Cumple | esp32.md:7-11 tiene los 5 temas. :16 tiene `id_cmd` obligatorio. :18-23 tiene LIFT, MOVE, STOP y DROP. :25 tiene los códigos. :28 tiene ahora el tiempo de espera de 1 s, sin reintento: TimeoutError, intento de `STOP` y la misión no continúa. test_ca_1_1_7_esp32_cmd_sin_id_cmd_es_invalido pasa |
| CA-1.1.8 | Cumple | mensajes.schema.json:94-103: `esp32_resp` sigue exigiendo ts, id_cmd, resultado y codigo, y `codigo` es ahora un enum de 8 valores (:101). test_wp_1_1.py:22 y :207 usan LIFT_OK y OVERWEIGHT, que están en el enum. Las 12 pruebas de CA-1.1.8 pasan |

No pude volver a ejecutar las pruebas en modo -v porque el hook solo permite el comando exacto de config.json. Me basé en el log del orquestador: commit 7229b5e, árbol limpio, misma cuenta que en la iteración 1 (37 passed) y ningún fallo de test_wp_1_1.py. tests/ no cambió entre 92ff22d y HEAD.

## Hallazgos
No hay hallazgos nuevos. Desde la iteración 2, los hallazgos quedan congelados: no encontré nada nuevo de severidad Mayor.

## Alcance, integridad y regresión
- Alcance: `git show --stat fc54e11` muestra solo contratos/esp32.md y contratos/mensajes.schema.json, con una línea cambiada en cada uno. Los dos están dentro de `contratos/**`.
- Integridad: el commit del WP (fc54e11) no toca `docs/pm/` ni `tests/`. Los commits entre la auditoría it1 y HEAD que tocan docs/pm son del orquestador: 8fcedb6 (auditoría it1), 0b4210d (CC-001), cb873be (estado), 7229b5e (agrega solo docs/pm/auditorias/WP-1.1_it2_ejecucion.md). HEAD es 7229b5e, el mismo commit que registra el log. Lo único sin seguimiento son el propio log y su .json de evidencia.
- Regresión: no hay. El log tiene 70 líneas `E`, y las 70 son ModuleNotFoundError (`simulador`, `backend`, `pi`) de WP que todavía no se implementan. Mismo resultado que en la iteración 1 (62 failed, 37 passed, 8 errors).
- El enum nuevo de `esp32_resp.codigo` no rompe pruebas de otros WP: test_wp_4_1.py:40 usa `LIFT_OK`, que está en el enum. Los dobles de test_wp_3_2.py:13 y test_wp_4_3.py:15 usan `"codigo": "OK"`, pero esas respuestas no se validan contra `esp32_resp`; test_wp_3_2 solo valida `esp32_cmd` (:67 y :78).
- Credenciales: no hay ninguna en el diff.

## Hallazgos de iteraciones previas: cerrados / persistentes
- H-1 [Menor] Reintento que contradice el error a 1 s: **CERRADO**. contratos/esp32.md:28 dice ahora que sin respuesta con el mismo `id_cmd` el comando se reporta como error (`TimeoutError` en la Pi), la Pi intenta enviar `STOP` y la misión no continúa, sin reintento. Concuerda con REQ-F-005, EJ-009, CA-3.2.2 y CA-4.3.6.
- H-2 [Observación] `esp32_resp.codigo` de texto libre: **CERRADO**. contratos/mensajes.schema.json:101 tiene ahora un `enum` con los 8 códigos de esp32.md:25.
