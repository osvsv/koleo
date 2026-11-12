# WP-1.2 it1 — informe de ejecución

Resultado: LISTO, con CA-1.2.6 pendiente de captura humana.

Archivos: simulador/__init__.py, simulador/robot_falso.py, simulador/__main__.py (innecesario).
Pruebas: `pytest -q -k ca_1_2` → 9 passed (CA-1.2.1 a CA-1.2.5).
CA-1.2.6: pendiente; no hay broker. Falta captura en docs/pm/evidencia/WP-1.2/captura_mosquitto.txt.

## Desviaciones
| Archivo o criterio | Categoría | Nota |
| --- | --- | --- |
| robot_falso.py (RUTAS) | aprendizaje | La línea base no fija las metas de RUTA_2 y RUTA_3 (mapa de WP-4.3). Se supuso RUTA_1→TAR-101 meta (4,5), RUTA_2→TAR-102 meta (2,3), RUTA_3→TAR-103 meta (3,4); x=col*30, y=fila*30. |
| simulador/.env.example | alcance | Write denegado por permisos; nombres de variables en el docstring. |
| simulador/__main__.py | defecto | Archivo innecesario. |

Variables de entorno nuevas: KOLEO_MQTT_PORT, KOLEO_MQTT_USER, KOLEO_MQTT_PASSWORD.
Sugerencias: paho-mqtt en requirements.txt; .env.example; alinear rutas con pi.mapa.RUTAS (WP-4.3).
