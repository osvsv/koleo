# WP-1.3 it2 — informe de ejecución

Resultado: LISTO. Pruebas de aceptación de WP-1.3: 19 passed (corridas por el orquestador en PowerShell; el hook bloquea pytest en Bash). CA-1.3.9 pendiente de captura humana con broker.

Cambios en backend/koleo/api.py: se quitó POST /api/ordenes (pertenece a WP-5.2); /api/indicadores reescrito según CA-1.3.11 (ocupacion = fracción, 0 si vacía; posicion_robot, tiempo_ciclo_s, precision_cm, peso_kg desde la tabla robots; alertas = 5 rechazos más recientes). ingesta.py sin cambios (ya cumplía CA-1.3.2, 1.3.10 y 1.3.12). Alcance: solo backend/**.
Desviaciones: ninguna.
Variables de entorno: KOLEO_MQTT_HOST, KOLEO_DB_PATH, KOLEO_API_HOST, KOLEO_API_PORT (más KOLEO_MQTT_PORT/USER/PASSWORD del simulador). Deben figurar sin valores en .env.example (lo gestiona el usuario).
