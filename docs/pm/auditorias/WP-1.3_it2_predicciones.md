# Predicciones WP-1.3 — iteración 2

Modo predicciones del auditor (auditoría ciega: solo docs/pm/ y tests/aceptacion/; no abrió backend/ ni contratos/).

**Contaminación declarada por el auditor:** una búsqueda con Grep sobre docs/pm/ le mostró dos líneas del informe de ejecución de it2 ("CA-1.3.9 pendiente de captura humana con broker", "ingesta.py sin cambios", "alertas = 5 rechazos más recientes") y el informe de ejecución de it1. No abrió el log de evidencia de it2. La P-1 se habría formulado igual.
**Iteración:** no existe WP-1.3_it1.md de auditoría (it1 fue bloqueo). Propone tratar it2 como auditoría de alcance completo, sin "hallazgos congelados".

## Predicciones ordenadas por probabilidad
| # | Prob. | Predicción | Cómo se comprueba |
| --- | --- | --- | --- |
| P-1 | Muy alta | CA-1.3.9 sin evidencia: no existe docs/pm/evidencia/WP-1.3/corrida_con_broker.txt; el dictamen no puede ser CONFORME aunque pasen las 19 pruebas. | ls de docs/pm/evidencia/WP-1.3/; si existe, salida real de Mosquitto y suscriptor, id_evento coherentes con una corrida y conteo de filas (2 historial / 1 rechazo). |
| P-2 | Alta | Desvío de alcance sin registrar: dependencias (Flask, jsonschema, paho) en requirements.txt desde el commit de WP-1.3; desviaciones.md sin fila de WP-1.3. | git show --stat e126fe0; git diff de requirements.txt; desviaciones.md. |
| P-3 | Alta | El suscriptor no hace commit por mensaje o no maneja errores (JSON malformado, tema desconocido, on_message sin try/except, QoS 1, recibido_ms de la recepción). | Leer backend/koleo/suscriptor.py. |
| P-4 | Alta | Credenciales o host del broker escritos en el código. | git grep -n -i "password\|passwd\|username_pw_set" -- backend/. |
| P-5 | Media-alta | REQ-F-008 a medias: origen, destino, peso_medido_kg, ruta_ejecutada o fecha_hora en NULL o con nombres heredados. | Leer el INSERT de historial en ingesta.py; examinar la fila de la prueba. |
| P-6 | Media-alta | tiempo_ciclo_s no empareja el LIFT_OK de la misma tarima que el último DROP_OK; precision_cm podría usar la meta de la ruta en vez del destino del último DROP_OK. | Leer api.py (indicadores) y la escritura de robots en ingesta.py. |
| P-7 | Media | peso_kg del indicador sale del DROP_OK y no de la telemetría (la prueba no lo distingue en RUTA_1). | Inspeccionar el origen del valor. |
| P-8 | Media | Duplicados de SOBREPESO/LIFT_OK no cubiertos por pruebas; riesgo de dos filas de rechazo. | Revisar eventos_vistos antes del INSERT de rechazo y en la misma transacción. |
| P-9 | Media | Descarte con efectos laterales (CA-1.3.5/1.3.6): DDL auxiliar o creación de tarima/robots antes de validar. | Orden de operaciones en procesar_mensaje; validación contra contratos/mensajes.schema.json. |
| P-10 | Media | Validación solo para evento; telemetría, conexion u orden/ack inválidos se escriben igual. | Inspección del despacho por tema. |
| P-11 | Media | API sobre BD solo con esquema.sql: /api/robots o /api/rechazos responden 500 por tablas auxiliares ausentes. | Leer crear_app y las rutas. |
| P-12 | Media-baja | Concurrencia SQLite entre suscriptor y API (check_same_thread, busy_timeout, WAL). | Cómo se abren las conexiones. |
| P-13 | Media-baja | Inyección SQL por f-strings con parámetros de consulta. | git grep -n "execute(f\|\" %\|\.format(" -- backend/. |
| P-14 | Media-baja | Aviso de latencia negativa poco específico (la prueba acepta cualquier WARNING). | logger.warning condicionado a latencia < 0 y sin max(0, …) ni abs. |
| P-15 | Baja | Atomicidad: commit parcial o IntegrityError sin rollback. | Manejo de IntegrityError y FK. |
| P-16 | Baja | EJ-016: DROP_OK con destino igual a la posición actual debe crear fila igualmente. | Inspección. |
| P-17 | Baja | Ack de orden con id_orden desconocido. | Rama orden/ack en ingesta.py. |
| P-18 | Baja | Regresión en WP-1.1/1.2 por cambios fuera de backend/. | git diff --stat de contratos/, simulador/, tests/. |

## Por criterio (esperado)
- CA-1.3.1: TAR-101 en UBICADA_DESTINO (150, 120), una fila de historial; también ruta_ejecutada, origen, destino, peso_medido_kg y fecha_hora poblados.
- CA-1.3.2: latencia_red_ms = recibido_ms − ts, entera; si es negativa (−50) se guarda cruda con WARNING específico.
- CA-1.3.3: una fila de rechazo con peso 11.80 y motivo no vacío, TAR-102 BLOQUEADA_SOBREPESO, sin fila de historial; un SOBREPESO reenviado no duplica.
- CA-1.3.4: 2 filas de historial (TAR-101, TAR-103) y 1 rechazo (TAR-102).
- CA-1.3.5: BD idéntica (mismo dump, incluidas auxiliares) y un registro en el log.
- CA-1.3.6: mismo id_evento → 1 fila; id_evento distintos → 2; sin id_evento se descarta, sin crear tarima.
- CA-1.3.7: /api/tarimas con id, estado y coordenadas; /api/historial vacío → [] y 200; también /api/rechazos y /api/robots devuelven 200.
- CA-1.3.8 y CA-1.3.11: seis claves; BD vacía sin 500; tras RUTA_1, ocupacion 1.0, peso_kg 8.45 de la telemetría, precision_cm 0.0, tiempo_ciclo_s (ts DROP − ts LIFT de TAR-101)/1000; alertas es una lista.
- CA-1.3.9: captura real con Mosquitto y simulador; hoy no hay archivo (P-1).
- CA-1.3.10: ruta_ejecutada "RUTA_1" y tarimas.ubicacion_nodo NULL.
- CA-1.3.12: coordenadas del rechazo de la última telemetría del robot, o NULL.

## Riesgos de interpretación
- "Última" telemetría: por orden de llegada o por ts; si es razonable y coherente, Observación.
- Tamaño de alertas: 5 es admisible.
- "Se descarta" en CA-1.3.6: apoyada en EJ-034, implica descarte completo; si crea la tarima, sería Menor.
- it2 sin auditoría previa: aplicar alcance completo (el auditor pide confirmación al orquestador).
- CA-1.3.9 como evidencia humana: sin ella el dictamen sería NO CONFORME.
- Tablas auxiliares creadas por la API y uso de Flask: no son hallazgo (CC-003 y la interfaz del WP).
