# Paquete de validación G1 (interno) — KOLEO

Quién valida: los 5 del equipo (Osvaldo coordina). Presupuesto: 40 min en total, unos 10 por persona.
Formatos: SN = sí / no / corregir · AB = opciones · EJ = ejemplo.
Una decisión por pregunta. Ninguna opción es la respuesta esperada; las recomendaciones del modelo están en `revision-externa.md`.

| ID | Formato | Pregunta (resumen) | Decide | Afecta a | Impacto |
| --- | --- | --- | --- | --- | --- |
| V-01 | SN | ¿Los dueños por subsistema propuestos son correctos? | Quién es dueño de cada subsistema | SUP-016 (19 WP) | Alto |
| V-02 | SN | ¿Cada integrante puede dar al menos 10 h por semana hasta el 2-dic? | Disponibilidad semanal mínima | SUP-016 (19 WP) | Alto |
| V-03 | SN | ¿Todas las piezas del listado final del 11-nov ya están en poder del equipo? | Si el hardware está completo | SUP-008, REQ-NF-008 (9 WP) | Alto |
| V-04 | SN | ¿El backend, la Pi y el simulador se programan en Python? | Lenguaje del software de alto nivel | SUP-007 (8 WP) | Alto |
| V-05 | AB | ¿Dónde corre el broker MQTT? | Ubicación del broker | SUP-006 (6 WP) | Alto |
| V-06 | AB | ¿La Raspberry Pi cuenta como el dispositivo "en red" del Reto IoT? | Aceptación de la arquitectura MQTT desde la Pi | SUP-001, REQ-NF-006 (5) | Alto |
| V-07 | AB | ¿Qué sensor(es) detienen el robot ante un obstáculo? | Sensor(es) de paro | SUP-005, REQ-F-004 (5) | Alto |
| V-08 | AB | ¿Se instala un fusible de 10 A en la batería? | Fusible sí/no | SUP-004, REQ-NF-005 (2) | Alto (seguridad) |
| V-09 | AB | ¿A qué distancia frontal se detiene el robot? | Umbral de paro | SUP-003, REQ-F-004 (3) | Medio |
| V-10 | SN | ¿El mapa 5×6 con celdas de 30 cm y las tres rutas son las que se evalúan? | Mapa y rutas de evaluación | SUP-009 (5) | Alto |
| V-11 | EJ | Con una masa de exactamente 10.0 kg, ¿el robot la levanta? | Tratamiento del límite exacto | SUP-010, REQ-F-001/002 (5) | Medio |
| V-12 | EJ | Con la báscula bien conectada y sin tarima (0.0 kg), ¿el robot no se eleva y avisa? | Comportamiento con peso válido de 0 kg | REQ-F-003 (3) | Medio |
| V-13 | EJ | Si el sensor de obstáculos deja de dar lectura mientras avanza, ¿el robot se detiene? | Fallo seguro del sensor de paro | REQ-F-004 (3) | Alto (seguridad) |
| V-14 | AB | ¿Qué estado tiene una tarima después de depositarse? | Nombre del estado tras el depósito | SUP-013, REQ-F-008/010 (4) | Medio |
| V-15 | AB | ¿Desde qué instante se cuenta la latencia de menos de 2 s? | Inicio de la medición de latencia | SUP-011, REQ-NF-003 (3) | Alto |
| V-16 | AB | Si el QR no se lee, ¿qué hace el robot? | Comportamiento sin lectura de QR | SUP-014, REQ-F-007 (3) | Medio |
| V-17 | AB | ¿Cuáles son las metas oficiales que se entregan al profesor? | Metas oficiales frente al profesor | SUP-002, REQ-NF-001/002 (4) | Alto |
| V-18 | EJ | Si el robot informa dos veces la misma entrega, ¿el historial muestra una sola? | Duplicados en el historial | REQ-F-008 (3) | Medio |
| V-19 | SN | ¿Los cierres del 20-nov, 27-nov y 30-nov/1-dic son los correctos? | Fechas de cierre de incremento | SUP-018 (3) | Medio |

## Fuera del paquete por presupuesto

SUP-006 en lo relativo a Flask + SQLite, SUP-012 (telemetría a 2 Hz), SUP-013 en lo relativo a la lista de estados del robot, SUP-015 (tablero por consulta cada 1 s), SUP-017 (515 pulsos por vuelta: se medirá), DP-09 (WP físicos por personas con evidencia), DP-13 (reportar la medición real si no se alcanza una meta). Se tratan como [S] hasta que alguien los objete.
