# WP-5.2 — informe de ejecución, iteración 1

Resultado: BLOQUEADO por una desviación de aprendizaje (código terminado, sin auditar; falta además la evidencia CA-5.2.5)

Archivos creados o modificados:
- `backend/koleo/ordenes.py` (nuevo): valida y crea órdenes, consulta órdenes y registra tarimas. La orden queda "pendiente"; el mensaje publicado lleva `ts`, `id_orden`, `tipo`, `ruta` e `id_tarima`; `id_orden` es `ORD-<12 hex>`.
- `backend/koleo/api.py`: cambio aditivo con `POST /api/ordenes` (202 o 400), `GET /api/ordenes/<id>` (200 o 404) y `POST /api/tarimas` (201 o 400). Los endpoints existentes, incluido `GET /api/ordenes`, no se tocaron.
- `ui/src/control/api.js` y `Control.jsx` (nuevos): botones INICIAR, CANCELAR y PARO, selectores de ruta y tarima, y lista de órdenes; cada orden pendiente se consulta cada 1 s hasta que pasa a aceptada o rechazada.
- `ui/src/logistica/Logistica.jsx` y `useTarimas.js` (nuevos): formulario de registro de tarima, tabla de tarimas con ubicación y estado, botón "Asignar" ruta (lleva a Control con ruta y tarima preseleccionadas) y traslados concluidos desde `/api/historial`.
- `ui/src/App.jsx`: modificación mínima (dos pestañas nuevas, el hook `useTarimas` y el render de las vistas).

Autoverificación (del ejecutor):
- CA-5.2.1 a CA-5.2.4: `pytest -q -k "wp_5_2 or wp_5_1 or wp_1_3"` dio 32 passed, con los 8 de `test_wp_5_2` (antes fallaban).
- CA-5.2.3: `ingesta.py` ya actualiza `ordenes` con el ack (`_ack`); no se tocó ni se duplicó.
- `npm run build` en `ui/` sin errores (35 módulos).
- CA-5.2.5: NO verificada; solo se comprobó que el tablero compila.

Desviaciones:
| Archivo o criterio | Categoría | Nota |
| --- | --- | --- |
| ui/src/App.jsx | alcance | Fuera del Alcance de archivos; modificación mínima necesaria para integrar la navegación |
| `main()` en api.py | aprendizaje | `crear_app` se llama sin publicador: con `python -m backend.koleo.api`, `POST /api/ordenes` devuelve 503. Hace falta un publicador MQTT real, que ningún criterio de la línea base pide |

Datos a conocer: la ingesta crea las órdenes con estado "enviada" y las de la API quedan "pendiente"; `peso_kg` se valida con 0 < peso ≤ 999.99 (por el DECIMAL(5,2) del esquema); una tarima duplicada responde 400.

Variables de entorno nuevas: ninguna.

Evidencia faltante: `docs/pm/evidencia/WP-5.2/control.png` (CA-5.2.5), con el tablero corriendo y mostrando los tres botones, el formulario de registro y una orden pasando de pendiente a aceptada.

## Archivos de WP conformes
Estos cambios tocan archivos auditados de WP conformes; quedarán en 'Requiere reverificación':
- WP-1.3: backend/koleo/api.py (está en el Alcance de archivos de WP-5.2: no es desviación)
- WP-5.1: ui/src/App.jsx (fuera del Alcance de WP-5.2: desviación de alcance registrada)
