# Auditoría WP-1.3 — iteración 4
Dictamen: CONFORME CON OBSERVACIONES
Commit: edc885c83b47615beb2e0501412f2b08fc4e8bb9
Nota del orquestador: el auditor trabajó con HEAD 5cb77de, que solo añade a edc885c el log, su .json, las predicciones y estado.md (sin cambios de código); la línea Commit se alineó con el commit de la evidencia (edc885c) para cumplir pm_check [1].
Evidencia: docs/pm/evidencia/WP-1.3_it4_aceptacion_edc885c.log
Archivos auditados: backend/__init__.py, backend/koleo/__init__.py, backend/koleo/api.py, backend/koleo/ingesta.py, backend/koleo/suscriptor.py, .env.example

**Resumen:** CA-1.3.13 (alcance nuevo de CC-005, con la nota de CC-006) se cumple. Sus 5 pruebas pasan y el código hace lo que pide el criterio. CA-1.3.1 a CA-1.3.12 siguen cumpliéndose y no hay regresión en test_wp_1_1, test_wp_1_2 ni test_wp_1_3. No hay hallazgos Mayores, Menores ni de Línea base. Siguen abiertas las observaciones O-1, O-2 y O-3 de la it2, por eso el dictamen lleva "con observaciones".

**Validez del log:** el log es de edc885c. HEAD (5cb77de) solo añade el propio log, su .json, las predicciones y estado.md: `git diff --stat edc885c HEAD` no toca código. Además, `git diff --stat fab2c41 edc885c -- backend tests contratos` sale vacío. Por eso el log vale para el código auditado y no se regeneró. El JSON marca "arbol_limpio": false por tres archivos sin seguimiento en la raíz (`$defs`, `` ` `` y `` numpy.ndarray` ``), todos de 0 bytes y creados entre las 07:47 y las 07:54, antes de fab2c41 (08:06). No son código y no influyen en la suite.

**Límites de la auditoría:**
- El hook no dejó ejecutar pytest en modo detallado (-v) sobre los archivos 1.x. El log -q no lista las pruebas que pasan una a una. Que pasan se deduce de que ninguna línea FAILED es de test_wp_1_1, test_wp_1_2 ni test_wp_1_3, y de que la barra de progreso no muestra pruebas omitidas.
- `.env.example` sigue sin poder leerse por una regla de permisos, y no se rodeó. No cambió desde la it3: no aparece en `git diff --stat ff00514..HEAD`. Sigue pendiente que el usuario confirme que solo contiene nombres de variables.

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-1.3.1 a CA-1.3.8, CA-1.3.10 a CA-1.3.12 | Siguen cumpliéndose (congelados, solo se revisa regresión) | El log termina en "51 failed, 78 passed in 2.34s" (línea 946). Las 51 líneas FAILED (895-945) son todas de test_wp_3_2, 4_1, 4_2, 4_3 y 5_2; ninguna de test_wp_1_3.py. fab2c41 no cambia DROP_OK, LIFT_OK, la latencia, `/api/indicadores` (que sigue con alertas globales, api.py:62-63) ni la toma de coordenadas del rechazo (ingesta.py:164-170) |
| CA-1.3.5 | Se cumple (revisado por el cambio de tema) | ingesta.py:21 y :106-114: los temas que no casan con `^koleo/robot[0-9A-Za-z_-]*/(.+)$` se descartan con un aviso. Si el sufijo no está en `_TEMA_A_DEF`, también se descarta con aviso. La validación con el esquema (ingesta.py:118-121) va antes de `asegurar_tablas` y de cualquier escritura |
| CA-1.3.9 | Se cumple (la evidencia humana de e126fe0 sigue siendo válida) | En la ruta de `robot1` el sufijo sale igual que antes. Lo único nuevo es escribir `velocidad_cm_s`, que el contrato hace obligatorio (mensajes.schema.json:12) y que el simulador emite (simulador/robot_falso.py:64), y una fila en `rechazos_robot`. Las tablas canónicas reciben las mismas filas |
| CA-1.3.13 | Se cumple | Pruebas `test_ca_1_3_13_*` (5), sin fallas en el log. Velocidad en ingesta.py:139-143 y api.py:43-45. `ruta_actual` en api.py:46-50: última INICIAR con estado 'aceptada', solo en EN_MISION, ELEVANDO, EN_RUTA y DEPOSITANDO (api.py:9, igual que SUP-031). Alertas en api.py:51-54: JOIN con `rechazos_robot` filtrado por robot, `id_alerta DESC` con `LIMIT 5`, con id_tarima, peso_detectado_kg, motivo y fecha_hora. La relación se escribe en ingesta.py:171-172. Con la BD vacía responde `[]` con 200, porque `conectar` crea las tablas (api.py:19). Multirobot (CC-006): ingesta.py:21 y :106 |

## Predicciones frente a lo observado
- **Regex del tema:** coincide con lo previsto. Siguen reconociéndose `telemetria`, `evento` y `orden/ack`. Los temas `esp32/*` y los que tienen niveles de más se descartan.
- **Migración con `ALTER TABLE`:** coincide. Se comprueba con `PRAGMA table_info` antes de alterar (ingesta.py:72-74): idempotente, sin "duplicate column" en una sola conexión, y `ADD COLUMN` no borra filas. Queda una carrera teórica entre suscriptor y API la primera vez; sin rango de hallazgo porque la línea base no exige concurrencia.
- **Alertas de `/api/indicadores` globales:** coincide (api.py:62-63, sin cambios).
- **Riesgo 1, `robot_id` del tema frente al del payload:** el código usa siempre el del payload. La línea base no dice cuál manda, y CA-1.3.12 y CA-1.3.13 hablan "del robot que emitió", que es el del payload. No es hallazgo.
- **Riesgo 2, valor de "aceptada":** `_ack` guarda `p["resultado"]` (ingesta.py:216); el contrato solo admite "aceptada" o "rechazada" (mensajes.schema.json:67) y la consulta filtra por 'aceptada'. La prueba no siembra la BD: pasa por `procesar_mensaje`. Una orden rechazada no cuenta.
- **Riesgo 3, pruebas débiles en máximo y orden:** no se cumplió. `test_ca_1_3_13_robots_alertas_maximo_5_mas_reciente_primero` siembra 6 rechazos y exige [5, 4, 3, 2, 1].
- **Riesgo 4, rechazos anteriores a la migración:** no tienen fila en `rechazos_robot` y no aparecen por robot. La línea base no lo exige; no es hallazgo.
- **Riesgo 5, empates en `ts_ack`:** desempate por `rowid DESC` (api.py:47), determinista.
- **Riesgos 6 y 7:** sin divergencia (ver última sección).
- **`ruta_actual` nula en DETENIDO_OBSTACULO, ERROR y sin orden aceptada:** coincide por lectura del código (api.py:49); la suite solo ejerce INACTIVO, que es lo único que exige el criterio.

## Hallazgos
No hay hallazgos nuevos.

Nota sin rango: `PREFIJO = "koleo/robot1/"` (ingesta.py:20) quedó sin uso tras el cambio a la regex.

## Alcance, integridad y regresión
- Alcance: el commit de trabajo fab2c41 solo modifica `backend/koleo/api.py` (+15/−2) y `backend/koleo/ingesta.py` (+21/−6), dentro de `backend/**`. Las dos desviaciones de aprendizaje (temas `koleo/robot<id>/` y `ruta_actual` global) están aprobadas por CC-006: WBS v1.6, CA-1.3.13 y SUP-031. No son hallazgo.
- Integridad de docs/pm y de las pruebas: fab2c41 no toca `docs/pm/` ni `tests/`. La última modificación de `tests/aceptacion/test_wp_1_3.py` es 6182431, un commit `[pm]` de CC-005. Los commits posteriores (3999733, 95db1d4, edc885c y 5cb77de) son `[pm]` y solo tocan `docs/pm/`.
- Regresión: la it3 (ff00514) terminó con 68 passed y 48 failed; la it4 con 78 passed y 51 failed. Ninguna línea FAILED es de test_wp_1_1, test_wp_1_2 ni test_wp_1_3. Las 51 fallas son de WP pendientes (test_wp_3_2, 4_1, 4_2 y 4_3 por módulos de `pi` ausentes; test_wp_5_2 porque los POST no existen). No hay regresión.
- Credenciales: una búsqueda en `backend/` (password, secret, token, clave, api_key) solo encuentra lecturas de variables de entorno (suscriptor.py:4, 27, 31 y 69). `.env.example`: ver el límite indicado al principio.
- Iteraciones: config.json fija `max_iteraciones: 3`. Esta es la it4, abierta por CC-005 y CC-006 y no por un dictamen NO CONFORME.

## Hallazgos de iteraciones previas: cerrados / persistentes
- H-1 [Menor] de la it2: sigue cerrado. ingesta.py:164-170 toma las coordenadas solo de `robots`.
- O-1 [Observación], persistente: `tiempo_ciclo_s` no comprueba que el LIFT_OK sea de la misma tarima.
- O-2 [Observación], persistente: el suscriptor registra un WARNING por cada mensaje de los temas `esp32/*`. La regex nueva sigue descartándolos con aviso.
- O-3 [Observación], persistente: `executescript` en `asegurar_tablas` confirma las transacciones pendientes de quien llama.
