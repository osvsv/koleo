# Auditoría WP-1.3 — iteración 6
Dictamen: CONFORME CON OBSERVACIONES
Commit: 7528a9105a1027dd19cdc192058a299505cf4421
Evidencia: docs/pm/evidencia/WP-1.3_it6_aceptacion_7528a91.log
Archivos auditados: backend/__init__.py, backend/koleo/__init__.py, backend/koleo/api.py, backend/koleo/ingesta.py, backend/koleo/suscriptor.py, .env.example
Tipo: reverificación

**Resumen:** Desde el dictamen anterior (0dfbfae), un solo commit toca archivos auditados: fc59f1f (WP-5.2), sobre `backend/koleo/api.py`. Solo añade: `import json`, la función `crear_publicador(env, cliente=None)` y, en `main()`, pasa `crear_publicador(os.environ)` a `crear_app`. Además corrige el docstring de `crear_app`. No cambia ninguna ruta GET de WP-1.3 ni `conectar`. Ningún test de WP-1.3 falla; CA-1.3.1 a CA-1.3.13 se siguen cumpliendo. Con este cambio se cierra la observación H-1 de la it5. El dictamen es "con observaciones" porque siguen abiertas O-1, O-2 y O-3 de dictámenes anteriores.

**Validez del log:** el JSON registra el commit 7528a9105a1027dd19cdc192058a299505cf4421 (HEAD), `arbol_limpio: true` y el comando `.venv\Scripts\python.exe -m pytest tests/aceptacion -q`. La corrida es de toda la suite (43 failed, 90 passed); ninguna falla es de `test_wp_1_3.py`.

## Verificación por criterio
| Criterio | Resultado | Evidencia |
| --- | --- | --- |
| CA-1.3.1 a 1.3.6, 1.3.10, 1.3.12 (ingesta) | Siguen cumpliéndose | Ningún commit posterior toca ingesta.py, suscriptor.py ni backend/__init__.py; sin fallas de test_wp_1_3 en el log |
| CA-1.3.7, 1.3.8, 1.3.13 (GET /api/*) | Siguen cumpliéndose | El diff no toca los handlers GET |
| CA-1.3.9 (broker real) | Sigue en pie | El diff no toca la ruta de la evidencia humana |
| CA-1.3.11 | Sigue cumpliéndose | Código de ingesta sin cambios |
| Arranque de la API (`main`, `crear_app`) | Sin efecto sobre WP-1.3 | `crear_app(db_path, publicador=None)` mantiene firma y valor por defecto; sin `KOLEO_MQTT_HOST` no hay publicador y la API arranca como antes |

## Cambios reverificados
- **fc59f1f [WP-5.2] it2** en `backend/koleo/api.py` (+27/−2): docstring de `crear_app`, `crear_publicador` (credenciales solo desde el entorno, qos=1) e inyección en `main()`. Autorizado por CC-008; `api.py` está en el alcance de WP-5.2. No es desviación.
- Los demás commits solo tocan `docs/pm/` o `tests/aceptacion/test_wp_5_2.py` (CC-008).

## Hallazgos
Sin hallazgos nuevos.

## Alcance, integridad y regresión
- `tests/aceptacion/test_wp_1_3.py` no cambió desde 0dfbfae: no hay pruebas debilitadas.
- It5: 86 passed / 43 failed (129); it6: 90 passed / 43 failed (133). Las 4 nuevas son de CA-5.2.6 y pasan; las 43 fallas son las mismas de WP pendientes (3.2, 4.1, 4.2, 4.3). Sin regresión.
- Sin literales sensibles nuevos; `.env.example` no cambió.

## Hallazgos de iteraciones previas
- H-1 [Observación] it5 (docstring de `crear_app` desactualizado): **cerrada** por fc59f1f.
- H-1 [Menor] it2: sigue cerrado.
- O-1 [Observación], persistente: `tiempo_ciclo_s` no comprueba que el LIFT_OK sea de la misma tarima.
- O-2 [Observación], persistente: el suscriptor registra un WARNING por cada mensaje de `esp32/*`.
- O-3 [Observación], persistente: `executescript` en `asegurar_tablas` confirma las transacciones pendientes de quien llama.
