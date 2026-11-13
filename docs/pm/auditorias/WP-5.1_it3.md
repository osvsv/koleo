# Auditoría WP-5.1 — iteración 3
Dictamen: CONFORME CON OBSERVACIONES
Commit: 0dfbfae274667cf126373566f30b3e045399c8f1
Evidencia: docs/pm/evidencia/WP-5.1_it3_aceptacion_0dfbfae.log
Archivos auditados: ui/package.json, ui/package-lock.json, ui/vite.config.js, ui/index.html, ui/.gitignore, ui/src/main.jsx, ui/src/index.css, ui/src/App.jsx, ui/src/usePolling.js, ui/src/Flotilla.jsx, ui/src/Monitoreo.jsx, ui/src/Indicadores.jsx, docs/pm/evidencia/WP-5.1/build.txt, docs/pm/evidencia/WP-5.1/flotilla.png, docs/pm/evidencia/WP-5.1/monitoreo.png, docs/pm/evidencia/WP-5.1/indicadores_antes.png, docs/pm/evidencia/WP-5.1/indicadores_despues.png, docs/pm/evidencia/WP-5.1/sin_conexion.png, docs/pm/evidencia/WP-5.1/LEEME.md
Tipo: reverificación

Base usada: docs/pm/03-wbs.md v1.7 (WP-5.1, riesgo medio; CA-5.1.4 según CC-007), el dictamen vigente docs/pm/auditorias/WP-5.1_it2.md (commit 99a9763) y docs/pm/desviaciones.md (fila de WP-5.2 sobre ui/src/App.jsx). El WP no se reabrió por una solicitud de cambio, sino por el commit de WP-5.2. Es la iteración 3 y rige la congelación de hallazgos: solo se evalúan regresiones y hallazgos Mayores nuevos que nazcan del diff.

## Cambios reverificados
| Commit | WP de origen | Archivo auditado | Efecto |
| --- | --- | --- | --- |
| 2805a96 | WP-5.2 (it1, bloqueado) | ui/src/App.jsx (+13/-4) | Importa `Control`, `Logistica` y `useTarimas`. Agrega el estado `asignada` y dos pestañas, Control y Logística. Cambia el ternario Flotilla/Monitoreo por cuatro renderizados condicionales (`vista === ...`). Llama a `useTarimas(d.conectado === true)`, que consulta `GET /api/tarimas` cada 1 s mientras haya conexión. La desviación está registrada en docs/pm/desviaciones.md:10. |

`git diff 99a9763..HEAD --stat -- ui docs/pm/evidencia/WP-5.1` muestra que en `ui/` cambiaron solo App.jsx (el archivo auditado) y cuatro archivos nuevos del Alcance de WP-5.2 (ui/src/control/**, ui/src/logistica/**). usePolling.js, Flotilla.jsx, Monitoreo.jsx, Indicadores.jsx, la configuración (package.json, vite.config.js, etc.) y la evidencia de WP-5.1 no cambiaron. El commit 2805a96 no toca `docs/pm/`.

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-5.1.1 [S] `npm run build` sin errores | Cumple, con límite | El build.txt es anterior al cambio: reporta "31 modules transformed" y un JS de 148.37 kB. El árbol de `ui/` sí cambió desde entonces (cinco archivos), así que build.txt ya no corresponde a HEAD. El hook impide ejecutar `npm run build`, por lo que se verificó leyendo el código. Los imports nuevos de App.jsx:6-8 se resuelven: `Control.jsx` y `Logistica.jsx` tienen `export default function`, y `useTarimas.js` exporta `useTarimas` con nombre. Los nombres que usan desde `control/api.js` (`RUTAS`, `enviarJson`, `obtenerJson`) también existen allí con nombre. El JSX de los cuatro archivos nuevos está bien formado y no usa dependencias fuera de package.json, que no cambió. Los hooks de App.jsx:11-14 se llaman sin condiciones, así que se respeta el orden de hooks. No se ve nada que impida compilar. |
| CA-5.1.2 [S] Flotilla: id, conexión, estado y alertas por robot | Cumple | Flotilla.jsx no cambió. En App.jsx:36, `vista === "flotilla" && <Flotilla robots={d.robots} />` le pasa la misma prop que antes, y "flotilla" sigue siendo la vista inicial (App.jsx:12). |
| CA-5.1.3 [S] Monitoreo: peso frente a capacidad, velocidad, ruta e historial | Cumple | Monitoreo.jsx no cambió. App.jsx:37 le pasa las mismas props, `robots` y `historial`, de `useTablero`. |
| CA-5.1.4 [D] ≥5 indicadores que cambian tras publicar (capturas, CC-007) | Cumple | Indicadores.jsx y usePolling.js no cambiaron, con sus 6 indicadores y su período de 1000 ms. App.jsx:35 sigue mostrando `<Indicadores ind={d.indicadores} />` arriba de cualquier pestaña. |
| CA-5.1.5 [S] backend detenido: "sin conexión" y sin datos viejos | Cumple | Las líneas App.jsx:27-33 (banner con `d.conectado === false`, "Conectando..." con `null` y `<main>` solo cuando `d.conectado` es verdadero) quedaron iguales a las de la it2. `d.conectado` lo sigue fijando solo useTablero. Si falla `/api/tarimas`, useTarimas vacía su lista y no toca `conectado`, así que no puede encender ni apagar el banner. Sin conexión, todo `<main>` se oculta, incluidas las pestañas nuevas, y no se pinta ningún dato. |
| Interfaz: consulta cada 1 s solo a /api/robots, /api/indicadores y /api/historial; sin /api/ordenes (CC-005, SUP-015) | Cumple para los módulos de WP-5.1 | usePolling.js:18-20 no cambió. Flotilla, Monitoreo e Indicadores siguen recibiendo datos solo de `useTablero`, sin `/api/ordenes` ni umbrales propios. Las consultas nuevas son de los módulos de WP-5.2: `GET /api/tarimas` desde useTarimas, que App.jsx monta, y `GET /api/ordenes/<id>` desde Control.jsx:19-28, solo en la pestaña Control y con órdenes pendientes. WP-5.2 las exige (CA-5.2.5 "refleja el ack" y el formulario de registro) y no alimentan ningún dato de Flotilla, Monitoreo ni Indicadores. Ver la nota 2. |

### Capturas de docs/pm/evidencia/WP-5.1/
Son anteriores al cambio. Lo único visible que el cambio altera es la barra de navegación del encabezado, que ahora tiene cuatro botones en vez de dos. El contenido que verifican los criterios no cambió en el código, así que las capturas siguen representando la UI de esos criterios: tabla de Flotilla, panel de Monitoreo, bloque de indicadores y banner de "sin conexión" con el `<main>` oculto. No hace falta volver a capturarlas para estos criterios.

## Hallazgos
El diff no produce hallazgos Mayores, Menores ni de Línea base. Por la congelación de la iteración 3, no se agregan observaciones nuevas. Dos notas para quien coordina; no son hallazgos de WP-5.1:

1. **build.txt desactualizado frente a HEAD.** La evidencia de CA-5.1.1 se generó antes de que 2805a96 agregara cuatro módulos a `ui/`. La lectura del código no muestra errores de compilación, pero un build real es la evidencia que pide el criterio. Conviene volver a generar `docs/pm/evidencia/WP-5.1/build.txt` (el número de módulos y el tamaño cambiarán) cuando WP-5.2 cierre su iteración, o como parte de su evidencia. Si sale con errores, sería un hallazgo Mayor de regresión atribuible a WP-5.2.
2. **Redacción de la Interfaz de WP-5.1.** "Consume ... por consulta cada 1 s; no consume `/api/ordenes`" se lee de forma natural como una regla de los módulos de WP-5.1. Leída sobre toda la aplicación, ya no se cumpliría, porque la app ahora consulta `/api/tarimas` cada 1 s en todas las pestañas y Control consulta `/api/ordenes/<id>`. Ambas cosas las exige WP-5.2. Se dictamina con la primera lectura. Si el usuario prefiere eliminar la ambigüedad, puede aclararla con `/pm-cambio`; no bloquea. Además, para WP-5.2, no para WP-5.1: useTarimas no vacía `tarimas` cuando `activo` pasa a falso; al reconectarse, Control y Logística podrían mostrar la lista anterior hasta la primera consulta, que se hace enseguida.

## Alcance, integridad y regresión
- Alcance: el cambio a ui/src/App.jsx viene de WP-5.2, cuyo Alcance de archivos no incluye ese archivo, y está registrado en docs/pm/desviaciones.md:10. El resto de los archivos de 2805a96 en `ui/` cae en ui/src/control/** y ui/src/logistica/**, que sí son del Alcance de WP-5.2.
- Integridad: 2805a96 no modifica `docs/pm/` (backend/koleo/api.py, backend/koleo/ordenes.py y los cinco archivos de ui).
- Credenciales: los archivos nuevos y el diff de App.jsx solo usan rutas relativas `/api/...` y no contienen secretos.
- Regresión: el log de 0dfbfae da "43 failed, 86 passed". El log de 99a9763 daba 51 fallas y 78 pasadas. Las fallas de ahora son exactamente las de test_wp_3_2 (6), test_wp_4_1 (18), test_wp_4_2 (8) y test_wp_4_3 (11), todas de WP Pendientes y presentes ya en el log de la it2. Las 8 de test_wp_5_2 ahora pasan. Ninguna prueba que antes pasaba falla ahora. WP-5.1 no tiene pytest propio. El log marca "Árbol limpio: no" por archivos sin seguimiento ajenos a `ui/`: `$defs`, `` ` ``, `` numpy.ndarray` `` y los logs y json de evidencia de 0dfbfae.
- Límite: no pudo ejecutarse `npm run build` porque el hook de lectura lo bloquea. Ver CA-5.1.1 y la nota 1.

## Hallazgos de iteraciones previas: cerrados / persistentes
Las observaciones del dictamen vigente (it2) siguen abiertas; el diff no las toca:
- H-1 [Observación] LEEME.md desactualizado frente a CC-007: persiste.
- H-2 [Observación] No consta el origen de la telemetría "después": persiste.
- H-3 [Observación] La consulta no tiene timeout ni protege contra respuestas fuera de orden (usePolling.js): persiste. useTarimas, que agregó WP-5.2, repite el mismo patrón, pero no afecta los criterios de WP-5.1.
