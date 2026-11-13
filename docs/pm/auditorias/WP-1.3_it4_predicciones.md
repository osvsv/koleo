# Predicciones WP-1.3 — iteración 4

(Redactadas por el auditor antes de la auditoría; no son dictamen. Fuente: criterios, SUP-031 y el informe de ejecución; no abrió backend/, tests/ ni contratos/.)

## Por criterio
- **CA-1.3.1 a CA-1.3.12 (congelados, solo regresión):** deberían seguir pasando. Tres sitios de riesgo: (1) la regex del tema en lugar del prefijo `koleo/robot1/` (CA-1.3.5 debe seguir descartando inválidos y el sufijo debe reconocer `telemetria`, `evento` y `orden/ack`); (2) el `ALTER TABLE` en `asegurar_tablas` (`executescript` confirma transacciones; posible efecto en la idempotencia de CA-1.3.6); (3) `alertas` de `/api/indicadores` (CA-1.3.11) debe seguir siendo global, no filtrada por robot. Esperado en el log: línea base de it3 más las 5 pruebas `test_ca_1_3_13_*` en verde; ninguna falla en test_wp_1_1, 1_2 ni 1_3.
- **CA-1.3.9:** la captura con broker de e126fe0 no ejerce los cambios; vale si la ruta de `robot1` no cambió de comportamiento (se comprueba leyendo el diff).
- **CA-1.3.13 (nuevo, se evalúa entero):** `velocidad_cm_s` 12.5 numérica y `ruta_actual` "RUTA_1" con EN_RUTA y orden aceptada; todas las claves de la interfaz presentes; `ruta_actual` null en INACTIVO (y por SUP-031 en DETENIDO_OBSTACULO y ERROR) y sin orden aceptada; una orden rechazada no cuenta y con varias cuenta la última; `alertas` con id_tarima, peso_detectado_kg, motivo y fecha_hora, máximo 5, más reciente primero, sin cruzarse con robot2, `[]` si no hay (no null), orden estable con `fecha_hora` igual; BD vacía `[]` con 200; telemetría `koleo/robot2/…` crea robot2 y se descartan `esp32/*` y temas fuera de formato; migración idempotente sin "duplicate column" y sin perder filas.

## Riesgos de interpretación (por probabilidad)
1. `robot_id` del tema frente al del payload en `rechazos_robot` y telemetría (la línea base no dice cuál manda).
2. Valor de "aceptada" guardado por el manejador del ack frente a la consulta de `ruta_actual` (podría salir siempre null en la ruta real aunque la prueba pase si siembra la BD).
3. Pruebas débiles en el máximo de 5 y el orden (Menor si el código falla; nota si solo falta ejercerlo).
4. Rechazos anteriores a la migración no tienen fila en `rechazos_robot` (la línea base no lo exige).
5. "Última" por `ts_ack` con valores iguales o nulos podría no ser determinista.
6. Alcance e integridad: fab2c41 solo debe tocar `backend/**`, sin `docs/pm/` ni `test_wp_1_3.py`.
7. Credenciales: ninguna esperada; sigue sin poderse leer `.env.example`.
8. Regla de congelación: CA-1.3.13 es alcance nuevo por cambio de línea base; admite Menores y Observaciones solo sobre lo añadido; 1.3.1 a 1.3.12 solo por regresión o Mayor nuevo.
9. Modo: la delegación es auditoría completa (hubo trabajo nuevo, fab2c41), no reverificación.
