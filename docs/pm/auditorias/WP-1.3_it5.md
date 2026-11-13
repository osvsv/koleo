# Auditoría WP-1.3 — iteración 5
Dictamen: CONFORME CON OBSERVACIONES
Commit: 0dfbfae274667cf126373566f30b3e045399c8f1
Evidencia: docs/pm/evidencia/WP-1.3_it5_aceptacion_0dfbfae.log
Archivos auditados: backend/__init__.py, backend/koleo/__init__.py, backend/koleo/api.py, backend/koleo/ingesta.py, backend/koleo/suscriptor.py, .env.example
Tipo: reverificación

**Resumen:** El único cambio en los archivos auditados desde edc885c es 2805a96 (WP-5.2) sobre `backend/koleo/api.py`, y solo añade cosas: un import (`request`, `ordenes as ord_`) y tres rutas nuevas (`POST /api/ordenes`, `GET /api/ordenes/<id_orden>`, `POST /api/tarimas`). No cambia ninguna línea de los endpoints GET de WP-1.3 ni de `conectar` o `consulta`. La suite completa no tiene fallas en test_wp_1_x. CA-1.3.1 a CA-1.3.13 se siguen cumpliendo. Lo único nuevo es una Observación (un docstring que el cambio dejó desactualizado). Siguen abiertas O-1, O-2 y O-3 de dictámenes anteriores, por eso el dictamen va "con observaciones".

**Validez del log:** el JSON (`docs/pm/evidencia/WP-1.3_it5_aceptacion_0dfbfae.json`) registra commit 0dfbfae274667cf126373566f30b3e045399c8f1, que es HEAD, y el comando `.venv\Scripts\python.exe -m pytest tests/aceptacion -q`. Marca `arbol_limpio: false` por los mismos tres archivos de 0 bytes sin seguimiento en la raíz (`$defs`, `` ` ``, `` numpy.ndarray` ``), descritos en la it4, más el propio log y el JSON de esta corrida. Nada de eso es código. No se regeneró el log.

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-1.3.1 a CA-1.3.6, CA-1.3.10, CA-1.3.12 (ingesta) | Siguen cumpliéndose | `git diff --stat edc885c..HEAD -- backend tests contratos` solo muestra api.py (+35/−1) y ordenes.py (nuevo). ingesta.py no cambió. Log, línea 807: "43 failed, 86 passed"; las líneas FAILED (764 a 806) son todas de test_wp_3_2, 4_1, 4_2 y 4_3, ninguna de test_wp_1_3.py |
| CA-1.3.7 (`GET /api/tarimas`, `GET /api/historial`) | Sigue cumpliéndose | api.py:30-36 queda igual que en edc885c. `POST /api/tarimas` (api.py:101-110) es otra ruta para el mismo path; Flask la separa por método y no toca el handler GET |
| CA-1.3.8 (`GET /api/indicadores`) | Sigue cumpliéndose | api.py:58-73 sin cambios; el log no tiene fallas en test_wp_1_3 |
| CA-1.3.9 (corrida con broker real) | Sigue en pie | El diff no toca ingesta.py ni suscriptor.py, que son la ruta de la evidencia humana en docs/pm/evidencia/WP-1.3/corrida_con_broker.txt |
| CA-1.3.11 | Sigue cumpliéndose | No hay fallas de test_wp_1_3 en el log, y el diff no toca código de ingesta |
| CA-1.3.13 (`GET /api/robots`) | Sigue cumpliéndose | api.py:42-56 sin cambios. `ordenes.crear_orden` inserta con estado 'pendiente' (ordenes.py:50-53), así que una orden sin ack aceptado no entra en `ruta_actual`, que filtra por estado 'aceptada' (api.py:47); se conserva la semántica |
| `GET /api/rechazos` y `GET /api/ordenes` | Sin cambios | api.py:38-40 y api.py:75-77 son idénticos. `GET /api/ordenes/<id_orden>` es otra regla que no choca con `/api/ordenes` |

## Cambios reverificados
- **2805a96 [WP-5.2] it1**, `backend/koleo/api.py` (+35/−1). Efecto: el import pasa a `from flask import Flask, jsonify, request`, se añade `from . import ordenes as ord_` y se añaden tres rutas nuevas. Cada ruta abre y cierra su propia conexión con `conectar()`, que sigue llamando a `asegurar_tablas`. Ninguna ruta de WP-1.3 cambia. El archivo está en el Alcance de archivos de WP-5.2, así que no es una desviación. El nuevo módulo `backend/koleo/ordenes.py` no es un archivo auditado de WP-1.3: escribe en `ordenes` y `tarimas` con las columnas que ya existen y no altera esquemas.
- **5c9acfa [pm]** y **0dfbfae [pm]**: solo tocan `docs/pm/` (bloqueos, desviaciones, informe de ejecución de WP-5.2 y estado.md). No afectan a WP-1.3.

## Hallazgos
### H-1 [Observación] El docstring de `crear_app` quedó desactualizado tras 2805a96
- Criterio o requisito afectado: ninguno de CA-1.3.x; mantenibilidad.
- Evidencia: api.py:14 sigue diciendo "`publicador(topic, payload_dict)` se conserva para el WP-5.2 (publicacion de ordenes); aqui no se usa.", pero api.py:83 ya lo usa en `POST /api/ordenes`.
- Qué tendría que ser cierto para cerrarlo: que el docstring describa el uso actual. Nace del cambio de WP-5.2, así que lo puede corregir ese WP.

## Alcance, integridad y regresión
- Alcance: 2805a96 toca `backend/koleo/api.py` y `backend/koleo/ordenes.py`, dentro del alcance de WP-5.2. Toca también `ui/**`, y `ui/src/App.jsx` está registrado en `docs/pm/desviaciones.md` (5c9acfa). Nada de eso es de WP-1.3.
- Integridad: entre edc885c y HEAD ningún commit toca `tests/`. `tests/aceptacion/test_wp_1_3.py` no cambió, así que no hay pruebas debilitadas. Los cambios en `docs/pm/` van solo en commits `[pm]`.
- Regresión: la it4 cerró con 78 passed y 51 failed, y la it5 con 86 passed y 43 failed (129 pruebas en ambas). Las 8 pruebas que antes fallaban y ahora pasan son de test_wp_5_2. Las 43 fallas restantes son de WP pendientes (3.2, 4.1, 4.2 y 4.3). Ninguna prueba que pasaba antes falla ahora: no hay regresión.
- Credenciales: el diff no añade literales sensibles. `.env.example` no cambió (no aparece en el diff edc885c..HEAD) y sigue con el mismo límite de lectura que en la it4.

## Hallazgos de iteraciones previas: cerrados / persistentes
- H-1 [Menor] de la it2: sigue cerrado, porque ingesta.py no cambió.
- O-1 [Observación], persistente y sin reabrir: `tiempo_ciclo_s` no comprueba que el LIFT_OK sea de la misma tarima.
- O-2 [Observación], persistente y sin reabrir: el suscriptor registra un WARNING por cada mensaje de `esp32/*`.
- O-3 [Observación], persistente y sin reabrir: `executescript` en `asegurar_tablas` confirma las transacciones pendientes de quien llama.
