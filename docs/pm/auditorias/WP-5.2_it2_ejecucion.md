# Informe de ejecución WP-5.2 — iteración 2
Resultado: TERMINADO
Commits: fc59f1f (código), 5029fbd y 0a00d2b (evidencia)

- `backend/koleo/api.py`: `import json`; nueva `crear_publicador(env, cliente=None)` (None sin `KOLEO_MQTT_HOST`; paho `CallbackAPIVersion.VERSION2` como suscriptor.py; usuario/contraseña de `KOLEO_MQTT_USER`/`KOLEO_MQTT_PASSWORD`; `publish(topic, json.dumps(payload), qos=1)`); `main()` la usa y la pasa a `crear_app`; docstring de `crear_app` corregido (observación WP-1.3 H-1).
- Pruebas: `tests/aceptacion/test_wp_5_2.py` 12 passed (incluye 4 `test_ca_5_2_6_*`).
- Evidencia: `orden_mosquitto.txt` (broker real en 127.0.0.1:18830, 202 y mensaje en `koleo/robot1/orden`), `control.png` (orden pendiente → aceptada; el ack se inyectó con `procesar_mensaje`, sin robot) y `logistica_registro.png` (alta de TAR-104). Los .png son JPEG con extensión .png.
- Nota del orquestador: el hook bloqueó al ejecutor escribir `orden_mosquitto.txt` en `docs/pm/`; el orquestador repitió la captura con los mismos comandos y guardó la salida real.
- Desviaciones: ninguna de alcance. `.env.example` no se modificó (variables `KOLEO_MQTT_*` ya nombradas).
- Impacto: `backend/koleo/api.py` es archivo auditado de WP-1.3 (queda en reverificación; en alcance de WP-5.2).
