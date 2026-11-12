# Estado del proyecto

> Archivo generado por gen_estado.py el 2026-11-12T12:43 sobre el commit 39e1607. No editar a mano.

## Gates

| Gate | Fecha | Aprobó | Notas |
| --- | --- | --- | --- |
| G0 | 2026-11-11 | Osvaldo | Perfil aprobado completo. DP-03 a DP-07 son [D] (decididas en Fase 0). DP-01, 02, 08 a 13 siguen [S] y entran al paquete de G1. |
| G1 | 2026-11-11 | Osvaldo | Línea base v1.1 aprobada con las respuestas de Osvaldo (V-01 a V-19). Pendiente: V-08 (fusible, SUP-004). Sin respuesta de los otros 4 integrantes. Suite de aceptación en tests/aceptacion (106 pruebas, fallan hasta ejecutar los WP). Ambigüedades menores de las pruebas: forma de las respuestas de GET /api/tarimas y /api/ordenes/<id>, avance de ejecutar_mision sin pulsos. |

## Paquetes de trabajo

| WP | Nombre | Riesgo | Tipo | Estado | Iteraciones | Último dictamen | Informe |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WP-1.1 | Contratos MQTT, comandos del ESP32, estados y SQL | medio | entregable | Conforme@7229b5e | 2 | CONFORME | docs/pm/auditorias/WP-1.1_it2.md |
| WP-1.2 | Robot simulado | bajo | entregable | Requiere reverificación | 2 | CONFORME CON OBSERVACIONES | docs/pm/auditorias/WP-1.2_it3.md |
| WP-1.3 | Backend de persistencia y Web API | alto | entregable | En corrección | 1 | NO CONFORME | docs/pm/auditorias/WP-1.3_it2.md |
| WP-2.1 | Chasis y tracción | medio | integracion | Pendiente | 0 | — | — |
| WP-2.2 | Mecanismo de elevación | alto | integracion | Pendiente | 0 | — | — |
| WP-2.3 | Energía y energizado seguro | alto | integracion | Pendiente | 0 | — | — |
| WP-2.4 | Sensores montados | medio | integracion | Pendiente | 0 | — | — |
| WP-3.1 | Báscula con fallo seguro y elevación | alto | entregable | Pendiente | 0 | — | — |
| WP-3.2 | Enlace de comandos Pi–ESP32 por MQTT | alto | entregable | Pendiente | 0 | — | — |
| WP-3.3 | Parada continua por obstáculo | alto | entregable | Pendiente | 0 | — | — |
| WP-4.1 | Puente MQTT | alto | entregable | Pendiente | 0 | — | — |
| WP-4.2 | Avance por distancia con encoders | medio | entregable | Pendiente | 0 | — | — |
| WP-4.3 | Planificador A* y misión | medio | entregable | Pendiente | 0 | — | — |
| WP-4.4 | Lectura QR | medio | entregable | Pendiente | 0 | — | — |
| WP-5.1 | Tablero: flotilla, monitoreo e indicadores | medio | entregable | Pendiente | 0 | — | — |
| WP-5.2 | Tablero: control y gestión logística | medio | entregable | Pendiente | 0 | — | — |
| WP-6.1 | Pruebas de elevación, rechazo, obstáculo y latencia | alto | integracion | Pendiente | 0 | — | — |
| WP-6.2 | Pruebas de rutas, llegada y traslado sostenido | alto | integracion | Pendiente | 0 | — | — |
| WP-6.3 | Ensayo general y reporte | medio | integracion | Pendiente | 0 | — | — |

## Resumen

Conforme: 1, En corrección: 1, Pendiente: 16, Requiere reverificación: 1
