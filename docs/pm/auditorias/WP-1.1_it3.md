# Auditoría WP-1.1 — iteración 3
Dictamen: CONFORME
Commit: d17df56400529808879ec63e8ff256efc5f570cd
Evidencia: docs/pm/evidencia/WP-1.1_it3_aceptacion_d17df56.log
Archivos auditados: contratos/mensajes.schema.json, contratos/estados.json, contratos/esquema.sql, contratos/mqtt.md, contratos/esp32.md

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| Interfaz (schema 2020-12 y los 9 `$defs`) | Cumple | mensajes.schema.json:2 y :10-127. test_interfaz_defs_presentes pasa: el log no tiene ninguna falla de test_wp_1_1.py |
| CA-1.1.1 | Cumple | telemetria (:10-23) y evento (:24-47) no cambiaron desde it2. Log (commit d17df56): "51 failed, 73 passed". Las 51 fallas están todas en test_wp_3_2, 4_1, 4_2, 4_3 y 5_2 (líneas 29-893 del log) y ninguna en test_wp_1_1.py |
| CA-1.1.2 | Cumple | orden, orden_ack y conexion (:48-79) no cambiaron. Sus pruebas pasan |
| CA-1.1.3 | Cumple | Sus pruebas pasan (test_wp_1_1.py:109, :116) |
| CA-1.1.4 | Cumple | contratos/estados.json no cambió (`git diff --stat 7229b5e..HEAD -- contratos` solo muestra esp32.md y mensajes.schema.json). Su prueba pasa |
| CA-1.1.5 | Cumple | contratos/esquema.sql no cambió. Sus pruebas pasan |
| CA-1.1.6 | Cumple (inspección) | contratos/mqtt.md no cambió desde la inspección de it1. Búsqueda de SCALE_FAIL, NO_LOAD, HX711, VL53, calibra, celda, PESO_SIM y báscula en contratos/: ninguna referencia |
| CA-1.1.7 | Cumple | esp32.md:7-11 tiene los 5 temas. :16 define `id_cmd` obligatorio y `peso_kg` obligatorio en LIFT. :18-23 tiene LIFT, MOVE, STOP y DROP. :20 y :25 tienen LIFT_OK, OVERWEIGHT, PESO_INVALIDO (ausente, no numérico o no positivo, como REQ-F-003 y EJ-005/006) y OBSTACULO_CERCANO; SCALE_FAIL y NO_LOAD se retiraron. :28 tiene el tiempo de espera de 1 s. test_ca_1_1_7_esp32_cmd_sin_id_cmd_es_invalido (test_wp_1_1.py:183) pasa |
| CA-1.1.8 | Cumple | `esp32_cmd`: :80-96, con `peso_kg` y un if/then que lo exige cuando cmd=LIFT (:94-95). `esp32_resp`: `codigo` incluye PESO_INVALIDO (:104). `esp32_sensores`: exige solo ts, distancia_obstaculo_cm, enc_izq y enc_der (:109). `esp32_evento`: el enum es exactamente {LIFT_OK, OVERWEIGHT, PESO_INVALIDO, OBSTACULO_CERCANO, DROP_OK} (:123), con id_tarima y peso_kg opcionales. Las condiciones de evento DROP_OK y SOBREPESO están en :41-46. Las pruebas de :189, :203, :212, :222, :230, :239, :245, :252 y :259 pasan |

## Hallazgos
No hay hallazgos. La iteración 1 fijó el alcance y desde la iteración 2 los hallazgos quedan congelados. No hay ningún hallazgo nuevo de severidad Mayor.

Nota (no es hallazgo; iteración congelada y no llega a Mayor): `esp32_sensores` sigue declarando `peso_kg` como propiedad opcional (mensajes.schema.json:112), mientras esp32.md:31 ya no lo menciona. No incumple CA-1.1.8, que solo exige que el campo no sea obligatorio, y el esquema no usa `additionalProperties: false`. Se puede quitar en un trabajo posterior.

## Alcance, integridad y regresión
- Alcance: `git show --stat e96ab71` muestra solo contratos/esp32.md y contratos/mensajes.schema.json, dentro de `contratos/**`. Ningún otro commit posterior a it2 (fc54e11) toca contratos/.
- Integridad: e96ab71 no toca `docs/pm/` ni `tests/`. El cambio de test_wp_1_1.py entre 7229b5e y HEAD viene del commit de línea base e87bfb8 (CC-004): adapta las pruebas (LIFT exige peso_kg, entra PESO_INVALIDO, pruebas negativas para SCALE_FAIL y NO_LOAD, sensores sin peso). No debilita lo que ya se verificaba.
- Evidencia: el log corresponde a HEAD (d17df56), con "Árbol limpio: no" por archivos sin seguimiento ajenos al WP en la raíz (`$defs`, `` ` ``, `` numpy.ndarray` `` y `ui/`), restos de comandos de shell mal formados. No afectan a contratos/ ni a las pruebas de WP-1.1.
- Regresión: no hay. Las 51 fallas son ModuleNotFoundError o ImportError de módulos `pi.*` aún no implementados (WP-3.2, 4.1, 4.2 y 4.3), más las 8 de WP-5.2, idénticas a las del log de WP-1.3 it3. test_wp_1_2, test_wp_1_3 y test_wp_4_4 no tienen fallas. Las fallas suben de 48 a 51 por pruebas que CC-004 agregó a WP pendientes.
- Credenciales: el diff no tiene ninguna.

## Hallazgos de iteraciones previas: cerrados / persistentes
- H-1 de it1 [Menor] Reintento que contradecía el error a 1 s: sigue CERRADO. esp32.md:28 no cambió.
- H-2 de it1 [Observación] `esp32_resp.codigo` de texto libre: sigue CERRADO. El enum de :104 se mantiene y ahora se ajusta a CC-004.
