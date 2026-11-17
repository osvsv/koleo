# Predicciones WP-3.1 — iteración 2
(Escritas por el auditor antes de ver el código corregido; guardadas por el orquestador.)

- CA-3.1.1: pines.h sin cambios; elevacionIniciarPines() sigue en setup() con GPIO 14 en LOW. Riesgo: que al tocar main.cpp se pierda o reordene esa llamada.
- CA-3.1.2: PESO_INVALIDO para NULL, vacío, "abc", "5x", 0, negativos, NaN e inf. Riesgos del cambio a double: firmas pesoValido/excedeLimite cambiadas a double (desvío de interfaz); saltarse isfinite o > 0; "1e-50" (0.0f en float) y "1e40" (inf en float) tratados de forma incoherente; buffer `linea` acotado que procese un prefijo truncado como peso válido, off-by-one y '\r' pegado.
- CA-3.1.6: un LIFT válido con la elevación activa no debe reasignar g_inicioMs; comparación `ahora - inicio >= 8000UL` en unsigned long; el apagado por tiempo pone g_activa=false y el pin en LOW; sin delay() nuevo; prueba interna de LIFT en t=0, LIFT en t=5000 y apagado en 8000.
- Interfaz: responder OVERWEIGHT o PESO_INVALIDO a un LIFT válido con elevación activa contradiría la Interfaz; un código nuevo sería desvío.
- Alcance: el commit debe tocar solo firmware/esp32/**; Wi-Fi/MQTT o credenciales en el código serían hallazgo Mayor.
- H-1 y H-2: trasladados a WP-3.2 por CC-010; evidencia de banco inventada sería hallazgo Mayor.
- Regresión: se espera 43 failed y 90 passed, con fallas solo en test_wp_3_2 y test_wp_4_x; cualquier falla nueva en WP-1.x, 4.4 o 5.x sería Mayor.
- Compilación ESP32: probablemente siga sin verificarse (Observación).
