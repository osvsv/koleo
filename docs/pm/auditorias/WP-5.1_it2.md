# Auditoría WP-5.1 — iteración 2
Dictamen: CONFORME CON OBSERVACIONES
Commit: 99a97630e549b3c43043f66f38e3e83dfbf38479
Evidencia: docs/pm/evidencia/WP-5.1_it2_aceptacion_99a9763.log
Archivos auditados: ui/package.json, ui/package-lock.json, ui/vite.config.js, ui/index.html, ui/.gitignore, ui/src/main.jsx, ui/src/index.css, ui/src/App.jsx, ui/src/usePolling.js, ui/src/Flotilla.jsx, ui/src/Monitoreo.jsx, ui/src/Indicadores.jsx, docs/pm/evidencia/WP-5.1/build.txt, docs/pm/evidencia/WP-5.1/flotilla.png, docs/pm/evidencia/WP-5.1/monitoreo.png, docs/pm/evidencia/WP-5.1/indicadores_antes.png, docs/pm/evidencia/WP-5.1/indicadores_despues.png, docs/pm/evidencia/WP-5.1/sin_conexion.png, docs/pm/evidencia/WP-5.1/LEEME.md

Base usada: docs/pm/03-wbs.md v1.7 (WP-5.1, riesgo medio), REQ-F-012 (EJ-023 y EJ-024), SUP-015, SUP-031, CC-005, CC-006 y CC-007. La profundidad corresponde a riesgo medio: todos los pasos, sin predicciones.

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-5.1.1 [S] `npm run build` sin errores | Cumple | docs/pm/evidencia/WP-5.1/build.txt: "✓ 31 modules transformed … ✓ built in 597ms", sin errores. El JS mide 148.37 kB y en la it1 medía 148.68 kB; cuadra con un build del código de la it2 (2ca1bc6), que quitó líneas. El archivo se archivó en cb6f762, después de 2ca1bc6. `git diff 99a9763 -- ui` está vacío, así que el árbol coincide con lo que se compiló. No pudo regenerarse porque el hook de lectura bloquea `npm run build` (ver Alcance). |
| CA-5.1.2 [S] Flotilla: id, conexión, estado y alertas por robot de /api/robots | Cumple | ui/src/Flotilla.jsx:14-22 muestra `robot_id`, `conexion` (EN_LINEA en verde y lo demás en rojo), `estado` y `r.alertas`, el campo por robot de CC-005. Ya no usa alertas globales ni el umbral de obstáculo de la it1 (diff de 2ca1bc6). En flotilla.png se ve "robot1 / EN_LINEA / EN_RUTA / TAR-102: SOBREPESO (11.8 kg)". backend/koleo/api.py:51-52 entrega `alertas` con `id_tarima, peso_detectado_kg, motivo, fecha_hora`, los mismos nombres que consume la UI. |
| CA-5.1.3 [S] Monitoreo: peso frente a capacidad, `velocidad_cm_s`, `ruta_actual` e historial | Cumple | ui/src/Monitoreo.jsx:16-21 muestra el peso declarado con barra frente a 10 kg, `r.velocidad_cm_s` y `r.ruta_actual` ("sin ruta en curso" si es nula, conforme a SUP-031). Las líneas 26-33 muestran el historial de `/api/historial`. En monitoreo.png se ve "Peso declarado: 8.45 kg de 10 kg", "Velocidad: 20 cm/s", "Ruta: RUTA_1" y "Historial reciente: TAR-101 — ruta RUTA_1". |
| CA-5.1.4 [D] ≥5 indicadores que cambian tras publicar (capturas antes y después; los 2 s no se cronometran, CC-007) | Cumple | ui/src/Indicadores.jsx:7-14 tiene seis indicadores: ocupación, posición, tiempo de ciclo, peso, precisión y alertas. indicadores_antes.png muestra posición (0, 90) cm, peso 8.4 kg y velocidad 20 cm/s. indicadores_despues.png muestra (90, 120) cm, 6.2 kg y 35 cm/s. La consulta es cada 1000 ms (ui/src/usePolling.js:3, 27), conforme a SUP-015, y por diseño queda dentro de 2 s. Ver H-1 y H-2. |
| CA-5.1.5 [S] backend detenido: "sin conexión" y sin datos viejos | Cumple | ui/src/usePolling.js:22-23: si falla una consulta, se vacía todo el estado y `conectado=false`. ui/src/App.jsx:22-28 muestra el banner y solo pinta los datos cuando `conectado` es verdadero. sin_conexion.png muestra "Sin conexión con el backend. No hay datos actuales que mostrar." y ningún indicador ni tabla. Ver H-3. |
| Interfaz (CC-005 y SUP-015) | Cumple | usePolling.js:18-20 consulta solo `/api/robots`, `/api/indicadores` y `/api/historial`, sin `/api/ordenes`. Se eliminó el umbral de obstáculo de 20 cm de la it1. |

## Hallazgos
No hay hallazgos Mayores, Menores ni de Línea base.

Nota sobre el régimen de iteración: la it1 terminó en bloqueo y no tuvo auditoría (docs/pm/auditorias/WP-5.1_it1_ejecucion.md), así que no hay hallazgos congelados. Esta auditoría se trató como la primera evaluación completa e incluye observaciones.

### H-1 [Observación] LEEME.md de la evidencia quedó desactualizado frente a CC-007
- Criterio o requisito afectado: CA-5.1.4 (documentación de la evidencia)
- Evidencia: docs/pm/evidencia/WP-5.1/LEEME.md dice "CA-5.1.4 pide `indicadores.mp4` y no existe… Falta que una persona grabe el video, o que se acepte la sustitución con un cambio de criterio" y marca las capturas como "(parcial)". CC-007 ya aprobó las capturas como evidencia [D].
- Qué tendría que ser cierto para cerrarlo: el LEEME debe citar CC-007 y dejar de presentar CA-5.1.4 como parcial o pendiente de video.

### H-2 [Observación] No consta el origen de la telemetría "después" ni el uso del simulador como publicador
- Criterio o requisito afectado: CA-5.1.2 ("con el simulador") y CA-5.1.4 ("tras publicar el simulador"); EJ-023
- Evidencia: según LEEME.md, la BD se sembró con `simulador.robot_falso.generar_mision` alimentando `procesar_mensaje`, sin broker. Para la telemetría nueva (posición (90, 120), peso 6.2 kg, velocidad 35 cm/s) no dice si salió del simulador o se armó a mano. CC-007 solo exige "publicar una telemetría nueva", así que el criterio se cumple.
- Qué tendría que ser cierto para cerrarlo: el LEEME debe indicar con qué se generó la telemetría "después", y que el camino MQTT del simulador al tablero queda para la integración.

### H-3 [Observación] La consulta no tiene timeout ni protege contra respuestas fuera de orden
- Criterio o requisito afectado: CA-5.1.5 y EJ-024, fuera del caso que verifica el criterio
- Evidencia: ui/src/usePolling.js:6 usa `fetch` sin `AbortController` ni timeout, y la línea 27 usa `setInterval` sin descartar ciclos anteriores. Con el backend detenido, el proxy responde con error enseguida y el criterio se cumple, como muestra la captura. Si el backend se cuelga sin cerrar la conexión, el último estado bueno quedaría en pantalla como actual; una respuesta exitosa tardía podría sobrescribir un `conectado=false` posterior.
- Qué tendría que ser cierto para cerrarlo: un timeout menor que el período, o abortar el ciclo anterior, y descartar respuestas de ciclos viejos. No es exigible por la línea base actual.

## Alcance, integridad y regresión
- Alcance: el commit 327f25a (it1) solo toca `ui/**` (12 archivos) y el 2ca1bc6 (it2) solo toca ui/src/App.jsx, Flotilla.jsx, Monitoreo.jsx y usePolling.js. La evidencia (cb6f762 para build.txt y aa5dea9 para capturas y LEEME) está en `docs/pm/evidencia/WP-5.1/**`. Todo dentro del Alcance de archivos del WP. La desviación de la it1 (`ui/.env.example` no creado) no dejó ningún archivo fuera de alcance.
- Integridad: ningún commit del WP (327f25a, 2ca1bc6) modifica `docs/pm/`. Los cambios a la línea base (03-wbs.md y cambios.md por CC-007) son del commit del método, separado del trabajo del ejecutor. `git diff 99a9763 -- ui docs/pm/evidencia/WP-5.1` está vacío.
- Credenciales: ninguna en ui/ fuera de package-lock.json, que solo trae nombres e integridad de paquetes. `KOLEO_API_URL` es opcional y no es secreta (ui/vite.config.js:7).
- Regresión: el log de 99a9763 da "51 failed, 78 passed". El conjunto de fallas es idéntico, por archivo, al de docs/pm/evidencia/WP-1.3_it4_aceptacion_edc885c.log (test_wp_3_2: 6, 4_1: 18, 4_2: 8, 4_3: 11, 5_2: 8; 51 en total), todos de WP Pendientes. Ninguna prueba que antes pasaba falla ahora. El log marca "Árbol limpio: no" por archivos sin seguimiento en la raíz (`$defs`, `` ` ``, `` numpy.ndarray` ``), ajenos a `ui/` y a las pruebas.
- Límite de la auditoría: no pudo volver a ejecutarse `npm run build` porque el hook de lectura del auditor lo rechaza (no está en `docs/pm/config.json`). CA-5.1.1 se dictamina con build.txt y con la comprobación de que el árbol de `ui/` no cambió desde el código que lo produjo.

## Hallazgos de iteraciones previas: cerrados / persistentes
No hubo auditoría en la it1. Las desviaciones de aprendizaje que bloquearon la it1 se resolvieron así:
- Velocidad no disponible: cerrada. Monitoreo usa `velocidad_cm_s` (CC-005).
- Ruta deducida del historial o de `/api/ordenes`: cerrada. Usa `ruta_actual` y ya no consume `/api/ordenes`.
- Alertas globales y umbral de obstáculo propio: cerrada. Usa `alertas` por robot y no hay umbral.
- Falta de evidencia: cerrada. Están build.txt y las cinco capturas, y CA-5.1.4 se resolvió con CC-007.
