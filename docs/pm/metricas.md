# Métricas

## Validación

| Punto | Fecha | Preguntas | Minutos | Correcciones (errores de especificación) | Por formato |
| --- | --- | --- | --- | --- | --- |
| G1 | 2026-11-11 | 19 | 15 | 7 (V-01, V-02, V-06, V-10, V-11, V-18, V-19) | sí-no: 7 · A-B: 9 · ejemplo: 3 (respondió solo Osvaldo) |

## Escapes

| Fecha | WP de origen | Dónde se detectó | Tipo (ε_impl / ε_esp) | Severidad | Descripción breve |
| --- | --- | --- | --- | --- | --- |
| 2026-11-13 | WP-1.3 | WP-5.1 it1 (CC-005) | ε_esp | Mayor | `GET /api/robots` no exponía velocidad, ruta en curso ni alertas por robot que piden CA-5.1.2 y 5.1.3; los criterios de WP-1.3 no los incluían |
