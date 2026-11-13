# WP-5.1 — informe de ejecución, iteración 2

Resultado: TERMINADO (falta evidencia gráfica)

Archivos modificados (todos en `ui/src/`):
- `usePolling.js`: consulta solo `/api/robots`, `/api/indicadores` y `/api/historial` cada 1 s; se quitó `/api/ordenes`. Si una consulta falla, se vacía el estado (conectado=false).
- `App.jsx`: Flotilla ya no recibe las alertas globales; Monitoreo ya no recibe órdenes.
- `Flotilla.jsx`: muestra id, conexión, estado y `r.alertas` de cada robot ("Sin alertas" si está vacío); se eliminó el umbral de 20 cm.
- `Monitoreo.jsx`: peso declarado frente a 10 kg, `velocidad_cm_s`, `ruta_actual` (null → "sin ruta en curso") e historial reciente de `/api/historial`.
- `Indicadores.jsx`: sin cambios (usa `/api/indicadores`, incluido el conteo de alertas globales como indicador).

Autoverificación:
- CA-5.1.1: `npm run build` en `ui/` sin errores (31 módulos, 562 ms).
- CA-5.1.2 a CA-5.1.4: BD temporal en el scratchpad, sembrada con `contratos/esquema.sql` y `procesar_mensaje` alimentado con `generar_mision`; Flask con `crear_app` y `npm run dev`, consultas con curl a http://localhost:5173/api/*. Con RUTA_1 (8.45 kg) y RUTA_2 (11.80 kg): robot1 INACTIVO, EN_LINEA, velocidad 0.0, `ruta_actual` null, alertas [TAR-102, 11.8, SOBREPESO]; `/api/historial` con TAR-101, RUTA_1, 8.45; `/api/indicadores` con los 6 campos. Con RUTA_1 a medias y una INICIAR aceptada: EN_RUTA, velocidad 20.0, peso 8.45, `ruta_actual` "RUTA_1". Verifica que el proxy entrega los campos que usa el tablero; no se abrió el tablero en un navegador, así que no se comprobó el render.
- CA-5.1.5: solo por lectura de código y prueba parcial: con el backend detenido el proxy de Vite devolvió HTTP 500 en `/api/robots`, que `fetch` trata como error y pone conectado=false, y `App` muestra "Sin conexión" sin datos. No se vio en pantalla.

Evidencia que falta (no hay herramienta para generarla; no se inventó): `flotilla.png`, `monitoreo.png`, `indicadores.mp4` y `sin_conexion.png` en `docs/pm/evidencia/WP-5.1/`. `build.txt` lo genera el orquestador.

Desviaciones: ninguna. Bloqueos: ninguno.

Limpieza: scripts de siembra, BD temporal y logs quedaron en el scratchpad; sin procesos de Flask ni de Vite escuchando. Un `taskkill` general fue denegado y no se ejecutó; terminó solo su proceso de Vite tras confirmar que era node.exe.

Sugerencia fuera de alcance: `latencia_red_ms` salió -5512 en `/api/historial` con el simulador; el log de ingesta avisa "relojes desfasados" porque el simulador genera `ts` en el futuro al sembrar sin broker. No afecta al tablero.
