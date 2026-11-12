# WP-1.3 it3 — informe de ejecución

Resultado: LISTO. Pruebas de aceptación de WP-1.3: 19 passed (corridas por el orquestador en PowerShell; el hook bloquea pytest en Bash).

Cambio (H-1, Menor): backend/koleo/ingesta.py, rechazo SOBREPESO: coord_x_cm/coord_y_cm salen solo de la última telemetría (fila robots), NULL si no hubo; se quitó la preferencia por x_cm/y_cm del evento. El DROP_OK sigue usando las coordenadas del evento (CA-1.3.1). Sin desviaciones ni variables nuevas.
Sugerencia del ejecutor: falta una prueba del caso H-1 (SOBREPESO con x_cm/y_cm distintos de la telemetría). No se añadió: las pruebas solo cambian por /pm-cambio.
La captura de CA-1.3.9 es de e126fe0; el cambio de it3 solo afecta a eventos SOBREPESO que traigan coordenadas, que el simulador no emite.
