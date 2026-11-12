# Auditoría WP-1.3 — iteración 2
Dictamen: NO CONFORME
Commit: 39e1607fb7eb29fa1baa89afe4f532517082ec2e
Evidencia: docs/pm/evidencia/WP-1.3_it2_aceptacion_39e1607.log
Archivos auditados: backend/__init__.py, backend/koleo/__init__.py, backend/koleo/api.py, backend/koleo/ingesta.py, backend/koleo/suscriptor.py, .env.example

**Resumen:** 11 de los 12 criterios se cumplen y no hay regresión. El dictamen es NO CONFORME por un solo hallazgo Menor (H-1, CA-1.3.12): si el evento SOBREPESO trae `x_cm`/`y_cm`, el código usa esas coordenadas en vez de las de la última telemetría, que es la fuente que aprobó CC-003. Se corrige con un cambio de 2 líneas o con una solicitud de cambio que apruebe la preferencia por las coordenadas del evento.

**Límite de la auditoría:** no se pudo leer `.env.example` (lo bloquea una regla de permisos y no se rodeó). Solo se vio que el commit afd042b modifica ese archivo y nada más (+6/−1), y que tiene su fila en desviaciones.md. **No se puede afirmar que no tenga valores reales de credenciales.** Las credenciales solo están verificadas en `backend/`. El usuario debe confirmar que `.env.example` contiene solo nombres de variables, sin valores.

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-1.3.1 | Cumple | Log: el resumen da "48 failed, 68 passed" y ninguna línea FAILED es de test_wp_1_3.py. test_ca_1_3_1 pasa. ingesta.py:166-182: INSERT en historial y UPDATE de la tarima a UBICADA_DESTINO con x_cm/y_cm del evento |
| CA-1.3.2 | Cumple | test_ca_1_3_2 [37, 0] y la prueba de latencia negativa pasan. ingesta.py:172 calcula `recibido_ms - ts` sin recortarlo. ingesta.py:176-178 registra un WARNING propio ("latencia negativa … relojes desfasados") solo si el valor es < 0 |
| CA-1.3.3 | Cumple | La prueba pasa. ingesta.py:150-160 escribe el rechazo con peso_kg y motivo "SOBREPESO", deja la tarima BLOQUEADA_SOBREPESO y no escribe historial. eventos_vistos (139-142) evita duplicar un reenvío en la misma transacción |
| CA-1.3.4 | Cumple | La prueba pasa (2 filas de historial y 1 de rechazo). Se repite en la corrida con broker (ver CA-1.3.9) |
| CA-1.3.5 | Cumple | test_ca_1_3_5 [sin_ts, tipo_desconocido] pasa. ingesta.py:94-108 valida contra el contrato y registra en el log antes de `asegurar_tablas` (109), así que un mensaje inválido no crea ni tablas auxiliares (el iterdump queda igual) |
| CA-1.3.6 | Cumple | Las 3 pruebas pasan. Un DROP_OK repetido se ignora por INSERT OR IGNORE con `id_evento UNIQUE` (ingesta.py:167-175). Un DROP_OK sin id_evento no pasa el esquema y no se crea la tarima |
| CA-1.3.7 | Cumple | Las 2 pruebas pasan. api.py:27-33 |
| CA-1.3.8 | Cumple | La prueba pasa. api.py:51-59 devuelve las seis claves |
| CA-1.3.9 | Cumple (evidencia humana) | corrida_con_broker.txt, revisado contra el código de e126fe0 y el simulador. Detalle en "Coherencia de la evidencia de CA-1.3.9" |
| CA-1.3.10 | Cumple | La prueba pasa. ingesta.py:171 guarda `p["ruta"]` en ruta_ejecutada; ninguna escritura toca ubicacion_nodo |
| CA-1.3.11 | Cumple | Las 2 pruebas pasan (BD vacía y RUTA_1). ocupacion = ubicadas/total, 0 si no hay tarimas (api.py:52). peso_kg sale de la telemetría (ingesta.py:126-130). tiempo_ciclo_s y precision_cm se calculan al llegar el DROP_OK (ingesta.py:184-190). alertas = 5 rechazos más recientes |
| CA-1.3.12 | Se cumple en lo probado; diverge en un caso que el contrato permite | Las 2 pruebas pasan, pero ingesta.py:157 usa `p.get("x_cm", x), p.get("y_cm", y)`. Ver H-1 |

## Coherencia de la evidencia de CA-1.3.9
- **Hora:** el suscriptor conecta a las 12:26:12 −06:00 (18:26:12 UTC). Los registros son de 18:27:42 a 18:27:55 UTC. Todo es posterior al commit e126fe0 (12:23:14 −06:00), y backend/ no cambió después (git diff 3940943..39e1607).
- **Identificadores de evento:** `EV-…-DROP_OK-13` para RUTA_1 y `-11` para RUTA_3 coinciden con el índice que calcula `generar_mision`: RUTA_1: 2 telemetrías + LIFT_OK + 9 celdas + DEPOSITANDO, así que el DROP_OK es el mensaje 13; RUTA_3: 2 + 1 + 7 + 1, así que es el 11.
- **Coordenadas:** TAR-103 queda en (120, 90), la meta (3, 4) de CA-1.2.7. El rechazo de TAR-102 queda en (0, 0), que es la telemetría ELEVANDO previa al SOBREPESO; el evento del simulador no trae coordenadas, así que coincide con CA-1.3.12.
- **Latencias (628 y 624 ms):** cuadran con publicar por broker real. El simulador fija los `ts` al generar la misión y luego espera 500 ms tras cada telemetría, así que la latencia es unos 500 ms más el tiempo de conexión. Son un artefacto del simulador, no del backend. REQ-NF-003 (< 2 s físico) corresponde a VAL-07, fuera de este WP.
- **Formato:** `fecha_hora` y `motivo` tienen el formato de `_iso` y "SOBREPESO", y los conteos son 2 de historial y 1 de rechazo. Todo coincide con el informe WP-1.3_it2_captura.md.
- **Límite:** la captura no incluye los comandos ni la salida de Mosquitto. Que haya un broker real se deduce de la línea "conectado al broker (Success)" de paho y de las latencias, que solo aparecen en modo `--broker`. No se registra como hallazgo porque el criterio no exige más.

## Predicciones frente a lo observado
| # | Predicción | Observado |
| --- | --- | --- |
| P-1 | Falta la evidencia de CA-1.3.9 | Refutada: el archivo existe y es coherente |
| P-2 | Dependencias sin registrar en requirements.txt | Refutada: requirements.txt no cambió. Flask, jsonschema y paho ya estaban (CC-001 / WP-1.2). `.env.example` está en desviaciones.md |
| P-3 | El suscriptor no hace commit por mensaje o no maneja errores | Refutada (suscriptor.py:38-51): JSON inválido se registra en el log, hay un cerrojo, commit por mensaje, rollback y log.exception; QoS 1; recibido_ms se toma al recibir |
| P-4 | Credenciales en el código | Refutada en backend/: usuario, clave, host y puerto salen del entorno. `.env.example` no es verificable |
| P-5 | Columnas de historial en NULL | Refutada: las 10 columnas se llenan (ingesta.py:168-172) |
| P-6 | El ciclo no empareja la tarima | Parcial: ts_lift_ms se guarda por robot y no se comprueba la tarima (O-1). precision_cm usa la última telemetría al momento del DROP_OK, una lectura razonable del criterio |
| P-7 | peso_kg sale del DROP_OK | Refutada: sale de la telemetría |
| P-8 | Duplicados de SOBREPESO o LIFT_OK | Refutada: eventos_vistos se escribe en la misma transacción |
| P-9 | Efectos laterales al descartar | Refutada: se valida antes de cualquier DDL o DML |
| P-10 | Solo se validan eventos | Refutada: se validan los 5 temas |
| P-11 | La API falla con 500 si faltan las tablas auxiliares | Refutada: `conectar()` llama a `asegurar_tablas` |
| P-12 | Problemas de concurrencia | Mitigada: WAL y timeout=5 en el suscriptor, timeout=5 en la API |
| P-13 | Inyección SQL | Refutada: todas las consultas son parametrizadas |
| P-14 | El aviso de latencia negativa es genérico | Refutada: es específico y condicionado a valor < 0 |
| P-15 | Falta atomicidad | Correcta en el suscriptor. Hay un matiz de `executescript` (O-3) |
| P-16 | EJ-016 | Cumple: la inserción no depende de la posición previa |
| P-17 | Ack de una orden desconocida | Se registra un WARNING (ingesta.py:203-204) |
| P-18 | Regresión | Refutada |
| (nueva) | Precedencia de coordenadas en el rechazo | No predicha: el informe de it1 suponía "el evento no trae coordenadas". Es H-1 |

## Hallazgos
### H-1 [Menor] El rechazo prefiere las coordenadas del evento a las de la última telemetría
- **Criterio afectado:** CA-1.3.12 [D] (CC-003): "toma coord_x_cm y coord_y_cm de la última telemetría del robot, o NULL si no hubo".
- **Evidencia:** en backend/koleo/ingesta.py:157 la línea `p.get("x_cm", x), p.get("y_cm", y)` hace lo siguiente: si el evento SOBREPESO trae `x_cm`/`y_cm`, usa esos valores y no los de la telemetría; si no hubo telemetría, guarda esos valores en vez de NULL, lo que contradice la segunda parte del criterio. El caso es real: `contratos/mensajes.schema.json:34-35` permite `x_cm`/`y_cm` opcionales en `evento`; la interfaz de WP-4.1 (`consolidar_esp32`) recibe esas coordenadas en `contexto`, así que el puente real puede emitir un SOBREPESO con coordenadas. Ninguna prueba cubre este caso. La regla aprobada en CC-003 venía del supuesto de it1, "el evento no trae coordenadas".
- **Para cerrarlo, una de dos:** las coordenadas salen solo de la fila `robots` (última telemetría), o NULL si no la hay, aunque el evento traiga `x_cm`/`y_cm`; o se aprueba la preferencia por las coordenadas del evento mediante `/pm-cambio` sobre CA-1.3.12.

### O-1 [Observación] tiempo_ciclo_s no comprueba que el LIFT_OK sea de la misma tarima
- **Criterio relacionado:** CA-1.3.11 ("LIFT_OK de la misma tarima").
- **Evidencia:** ingesta.py:149 guarda `ts_lift_ms` por robot sin `id_tarima`, e ingesta.py:186 lo resta sin comparar la tarima. Con un robot que lleva una tarima a la vez y una secuencia conforme, el resultado es correcto. Solo difiere en secuencias anómalas (un LIFT_OK de X seguido de un DROP_OK de Y): ahí da un tiempo cruzado en vez de nulo.
- **Mejora sugerida:** guardar también la tarima del LIFT_OK y calcular el ciclo solo si coincide.

### O-2 [Observación] El suscriptor recibe los temas esp32/* y registra un WARNING por cada mensaje
- **Evidencia:** suscriptor.py:36 se suscribe a `koleo/#`, e ingesta.py:98-101 registra un WARNING ("tema sin manejador") por cada `koleo/robot1/esp32/*`. Con el robot real, los sensores del ESP32 inundarán el log.
- **Mejora sugerida:** suscribirse solo a los 5 temas del contrato, o bajar ese registro a DEBUG.

### O-3 [Observación] `asegurar_tablas` confirma transacciones pendientes de quien llama
- **Evidencia:** ingesta.py:3 dice "procesar_mensaje no hace commit". Pero ingesta.py:63 usa `executescript`, que primero hace COMMIT de la transacción pendiente. Hoy no afecta: el suscriptor y las pruebas confirman mensaje a mensaje, y el DDL corre antes de las escrituras del mensaje. Un llamador que agrupe varios mensajes en una transacción perdería la atomicidad.
- **Mejora sugerida:** crear las tablas con `execute` por sentencia, o una sola vez al abrir la BD.

## Alcance, integridad y regresión
- **Alcance:** e126fe0 solo añade `backend/__init__.py` y `backend/koleo/{__init__,api,ingesta,suscriptor}.py`, todos dentro de `backend/**`. afd042b solo modifica `.env.example`, registrado en docs/pm/desviaciones.md:7 (fila WP-1.3). `git diff --stat 3940943 39e1607` no muestra cambios en contratos/, simulador/, tests/ ni requirements.txt. `GET /api/ordenes` (api.py:61-63) es una lectura adicional dentro de backend/**; no está prohibida y POST no se implementó, como pide CC-003.
- **Integridad de docs/pm:** los commits de trabajo (e126fe0, afd042b) no tocan docs/pm/. Los cambios en docs/pm/ están en commits `[pm]`. El informe `WP-1.3_it3_ejecucion.md` se renombró a `WP-1.3_it2_captura.md` (solo cambio de nombre).
- **Regresión:** log anterior (WP-1.2_it3_aceptacion_b7c751b.log): 49 passed, 53 failed, 8 errors. Log actual (39e1607, árbol limpio): 68 passed, 48 failed. 68 = 49 + las 19 pruebas de test_wp_1_3.py. No hay ninguna línea FAILED de test_wp_1_1.py, test_wp_1_2.py ni test_wp_1_3.py. Los fallos restantes son de WP pendientes: el módulo `pi` no existe (WP-3.2, 4.1 a 4.4), y test_wp_5_2.py da 405 porque los POST pertenecen a WP-5.2. Antes también fallaban, así que no son regresión. El auditor no pudo volver a correr pytest (el hook lo bloquea en Bash) y usó el log indicado.
- **Credenciales:** en backend/ no hay ninguna escrita. El usuario y la clave MQTT salen de KOLEO_MQTT_USER/PASSWORD (suscriptor.py:68-69), y una búsqueda de patrones de credenciales en backend/ no encontró nada. El límite sobre `.env.example` está explicado al principio.

## Hallazgos de iteraciones previas: cerrados / persistentes
No hay auditorías anteriores de WP-1.3: la it1 terminó en bloqueo, resuelto por CC-003. Por eso esta iteración se auditó con alcance completo, sin congelar hallazgos.
