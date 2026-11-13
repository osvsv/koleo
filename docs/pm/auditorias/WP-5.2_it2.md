# Auditoría WP-5.2 — iteración 2
Dictamen: CONFORME CON OBSERVACIONES
Commit: 525905aaa9f3f2f5a1f161fe78be542606fd1e98
Evidencia: docs/pm/evidencia/WP-5.2_it2_aceptacion_525905a.log
Archivos auditados: backend/koleo/api.py, backend/koleo/ordenes.py, ui/src/control/Control.jsx, ui/src/control/api.js, ui/src/logistica/Logistica.jsx, ui/src/logistica/useTarimas.js, ui/src/App.jsx

Sobre la evidencia: el log indicado por el orquestador era de 0a00d2b; el auditor volvió a correr `run_acceptance.py --wp WP-5.2 --iter 2` en HEAD 525905a (90 passed, 43 failed, igual que antes; entre 0a00d2b y HEAD solo cambió `docs/pm/`). "Árbol limpio: no" por tres archivos basura de la raíz (`$defs`, `` ` ``, `numpy.ndarray`).

## Verificación por criterio
| Criterio | Resultado | Evidencia |
| --- | --- | --- |
| CA-5.2.1 | Cumple | `test_ca_5_2_1_*` no está entre los FAILED (133 pruebas; fallos solo de test_wp_3_2/4_1/4_2/4_3). ordenes.py:42-55, tema `koleo/robot1/orden` (ordenes.py:11), api.py:83-94 responde 202 |
| CA-5.2.2 | Cumple | `test_ca_5_2_2_*[id_tarima]` y `[ruta]` pasan. Validación antes de publicar (ordenes.py:37-38, :44, :49) |
| CA-5.2.3 | Cumple | `test_ca_5_2_3_*[aceptada\|rechazada]` pasan. Ack por `ingesta.procesar_mensaje`, lectura con `GET /api/ordenes/<id>` (api.py:96-103) |
| CA-5.2.4 | Cumple | `test_ca_5_2_4_*` pasan. ordenes.py:66-71, regex `^TAR-\d{3}$` y `0 < peso <= 999.99` |
| CA-5.2.5 | Cumple (ver O-1) | `control.png` (JPEG 1536x702) muestra INICIAR, CANCELAR, PARO y la orden `ORD-b062a8d4b907` en "aceptada". Formulario de registro en `logistica_registro.png`. Control.jsx:16-31 y :62-64 |
| CA-5.2.6 | Cumple | 4 pruebas `test_ca_5_2_6_*` pasan. api.py:139-141 cablea `crear_publicador(os.environ)`; credenciales de `env` (api.py:121, 127, 129, 130). `orden_mosquitto.txt`: 202 `{"id_orden":"ORD-32b0b9763eb2"}` y el mismo id en `koleo/robot1/orden` |

## Hallazgos
### O-1 [Observación] La evidencia nombrada para CA-5.2.5 no muestra el formulario de registro
`control.png` solo muestra Control; el formulario está en `logistica_registro.png`, que el diccionario no nombra. El ack se inyectó con `procesar_mensaje` (sin robot), aceptable porque el criterio pide reflejar el ack. No bloquea; en futuras líneas base, nombrar las dos capturas.

### O-2 [Observación] `orden_mosquitto.txt` se capturó sobre un árbol sin commit
Cabecera: "commit base 5908fde + cambios sin commit"; 14 s antes de fc59f1f. La salida es coherente con api.py en HEAD. No bloquea; capturar evidencia física sobre el commit de código ya creado.

### O-3 [Observación] Archivos basura sin seguimiento en la raíz
`$defs`, `` ` ``, `numpy.ndarray`` hacen que los logs salgan con "Árbol limpio: no". Borrarlos.

### O-4 [Observación] Si el broker no está disponible al arrancar, la API no levanta
api.py:130 llama a `cliente.connect(...)` de forma síncrona; con host definido y broker caído, la excepción sube en `main()`. Mejora opcional: `connect_async` o degradar a 503.

## Alcance, integridad y regresión
- Alcance: 2805a96 toca api.py, ordenes.py, ui/src/control/**, ui/src/logistica/** (en alcance) y ui/src/App.jsx (desviación registrada en docs/pm/desviaciones.md). fc59f1f solo toca api.py. `crear_publicador(env, cliente=None)` coincide con WBS v1.8 y CC-008.
- Integridad: los commits de código no tocan `docs/pm/`; los de evidencia solo añaden `docs/pm/evidencia/` y el informe de ejecución. Sin cambios en `ui/` ni `ordenes.py` desde 2805a96; build.txt (it1, 35 módulos) sigue vigente.
- Regresión: 43 fallos, todos en test_wp_3_2, 4_1, 4_2 y 4_3 (módulos `pi` ausentes, WP Pendientes; nunca pasaron). Ningún WP conforme falla. api.py es archivo auditado de WP-1.3 y App.jsx de WP-5.1: deben reverificarse.
- Credenciales: ninguna en el código del WP. `.env.example` sin cambios. Se encontró `const char* WIFI_PASSWORD = "password123";` en `docs/pm/importado/KOLEO_todo.md:1105` (documento fuente importado, anterior al WP; no es hallazgo de WP-5.2): el usuario debe confirmar que es un marcador.
- Primera auditoría del WP (la it1 quedó bloqueada); las observaciones entran como iniciales.

## Hallazgos de iteraciones previas: cerrados / persistentes
- WP-1.3 H-1 [Observación], docstring de `crear_app`: cerrado (api.py:15-18).
- Desviación de aprendizaje de la it1 (`main()` sin publicador): resuelta con CC-008 y CA-5.2.6.
