# Calidad y costo por WP

> Archivo generado por metricas_wp.py el 2026-11-12T12:45 sobre el commit ff00514. No editar a mano. Los escapes se anotan en `metricas.md` (sección Escapes) y el uso lo registra el hook de fin de sesión en `uso.csv`.

Hallazgos it1 = Mayor/Menor/Observación/Línea base en la primera auditoría. Retrabajo = iteraciones de corrección + reverificaciones. USD eq. = equivalente con la tabla de precios del hook, sin el auditor en sombra (columna aparte).

| WP | Riesgo | Estado | Ejecutor | Auditor | Iter. | Hallazgos it1 (M/m/O/LB) | Escalado | Retrabajo | Escapes | Obs. abiertas | Tokens | USD eq. | USD sombra | Horas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WP-1.1 | medio | Conforme | sonnet | opus | 2 | 0/1/1/0 | no | 1 | 0 | 1 | 21872529 | 15.24 | 0.00 | 0.3 |
| WP-1.2 | bajo | Requiere reverificación | — | — | 2 | 1/0/2/0 | no | 1 | 0 | 2 | — | 0.00 | 0.00 | 0.8 |
| WP-1.3 | alto | Conforme | — | — | 2 | 0/1/0/0 | no | 1 | 0 | 0 | — | 0.00 | 0.00 | 0.3 |

## Resumen

- WP conformes: 2; USD eq. registrado en WP: 15.24
- Tasa de escape: 0/2 WP conformes con al menos un escape
