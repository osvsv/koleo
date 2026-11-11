# Cambios a la línea base

| ID | Fecha | Carril | Origen | Descripción | Impacto | Decisión | Reabre | Versión |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CC-001 | 2026-11-11 | Menor | Entorno Python del proyecto (.venv); regulariza el commit b3fede4 | Los comandos de prueba de `docs/pm/config.json` usan `.venv\Scripts\python.exe` (aceptación, caracterización y lectura extra) y se añade `requirements.txt` con versiones fijadas | Ninguno en requisitos, WP, criterios ni pruebas; solo cambia el intérprete con que corren | Aprobado (revisión en lote) | Ninguno | config.json sin cambio de versión de línea base |
