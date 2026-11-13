# WP-5.1 — informe de ejecución, iteración 1

Resultado: BLOQUEADO por desviaciones de aprendizaje (código y build terminados; sin evidencia archivada)

Archivos creados (bajo `ui/`): `package.json` (React 18, Vite 6, Tailwind 4), `vite.config.js` (proxy de /api, `KOLEO_API_URL`, por defecto http://127.0.0.1:5000), `index.html`, `.gitignore`, `package-lock.json`, `src/main.jsx`, `src/index.css`, `src/App.jsx`, `src/usePolling.js` (consulta cada 1000 ms a /api/robots, /api/indicadores, /api/historial y /api/ordenes; si una falla, descarta los datos y marca conectado=false), `src/Flotilla.jsx`, `src/Monitoreo.jsx`, `src/Indicadores.jsx` (6 indicadores).

Build: `npm install` y `npm run build` en `ui/` terminaron con código 0 (31 módulos, JS 148.68 kB, CSS 9.85 kB). Sin verificar contra backend ni simulador; no se midió el tiempo de actualización de 2 s.

Desviaciones:
| Archivo o criterio | Categoría | Nota |
| --- | --- | --- |
| CA-5.1.3 (velocidad) | aprendizaje | `GET /api/robots` no devuelve velocidad; la tabla `robots` de `backend/koleo/ingesta.py` no la guarda aunque el simulador la publica. Monitoreo muestra "no disponible en la API" |
| CA-5.1.3 (ruta e historial) | aprendizaje | `/api/robots` no trae ruta ni historial. Se consultan además `/api/historial` y `/api/ordenes` (existen, pero la interfaz del WP solo nombra `/api/robots` y `/api/indicadores`). La "ruta" es la última del historial o de la última orden, no la ruta en curso |
| CA-5.1.2 (alertas por robot) | aprendizaje | La API no relaciona alertas con robot; se muestran las últimas 5 globales y "Obstáculo a X cm" si la distancia < 20 cm (umbral del ejecutor) |
| ui/.env.example | alcance | No se pudo crear (regla de permisos); variable `KOLEO_API_URL` documentada aquí |
| evidencia CA-5.1.* | defecto | Faltan build.txt, flotilla.png, monitoreo.png, indicadores.mp4 y sin_conexion.png; los hooks bloquean a los agentes escribir en docs/pm y no hay herramienta de captura |

Variables de entorno nuevas: `KOLEO_API_URL` (opcional, sin credenciales).

Sugerencias: añadir `velocidad_cm_s` a la tabla `robots` y a `/api/robots`, y asociar alertas a un robot (backend). Para la evidencia, con backend y simulador corriendo, `npm run dev` en `ui/` y capturar; para CA-5.1.5, detener el backend.
