# Auditoría WP-1.2 — iteración 3
Dictamen: CONFORME CON OBSERVACIONES
Commit: b7c751bb01fe08ddc97f2bb590d506019f54cfb0
Evidencia: docs/pm/evidencia/WP-1.2_it3_aceptacion_b7c751b.log
Archivos auditados: simulador/__init__.py, simulador/robot_falso.py, requirements.txt, .env.example, docs/pm/evidencia/WP-1.2/captura_mosquitto.txt

**Resumen:** la captura con mosquitto ya existe y es coherente, así que H-1 (el único hallazgo Mayor de it2) queda cerrado. El código no cambió desde d506661, por lo que CA-1.2.1 a CA-1.2.5 y CA-1.2.7 siguen cumpliéndose según el log nuevo. No hay regresión. H-2 y H-3 siguen abiertos como observaciones, que no bloquean.

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-1.2.1 | Cumple | El log de b7c751b (árbol limpio) termina en "53 failed, 49 passed, 8 errors" (log:1207). Ningún test de test_wp_1_2.py aparece en las líneas FAILED o ERROR (log:1146-1206); todos los fallos son de WP-1.3, 3.2, 4.x y 5.2. Desde d506661 no hubo cambios en simulador/ ni en tests/ (`git diff --stat d506661..HEAD` solo lista archivos de docs/pm/). |
| CA-1.2.2 | Cumple | Igual que en it2. El test no falla en el log y el código no cambió. |
| CA-1.2.3 | Cumple | Igual que en it2. El test no falla en el log y el código no cambió. |
| CA-1.2.4 | Cumple | Igual que en it2. El test no falla en el log y el código no cambió. |
| CA-1.2.5 | Cumple | Igual que en it2. Además, en la captura los ts de telemetría avanzan exactamente 500 ms (captura:2-14). |
| CA-1.2.6 | Cumple | captura_mosquitto.txt (UTF-16, 16 líneas, en formato `mosquitto_sub -v`, es decir, tópico + payload). Contenido: línea 1 `koleo/robot1/conexion` EN_LINEA; líneas 2-14 telemetría; línea 4 evento LIFT_OK de TAR-101 con peso_kg 8.45; línea 15 evento DROP_OK de TAR-101 con 8.45 kg, x_cm 150.0, y_cm 120.0, ruta RUTA_1 y origen (0,0); línea 16 FUERA_DE_LINEA. |
| CA-1.2.7 | Cumple | Igual que en it2. La trayectoria de la captura, (0,0) → (0,120) → (150,120), coincide con RUTA_1 de CC-002 a 30 cm por celda. |

## Predicciones frente a lo observado
No aplica (riesgo bajo).

## Coherencia de la captura (detalle)
- Payloads: el peso es 8.45 kg en LIFT_OK, en DROP_OK y en la telemetría posterior a la elevación. DROP_OK cae en (150,120) y es el último evento, seguido solo por FUERA_DE_LINEA.
- id_evento: los dos eventos comparten el prefijo de corrida `EV-47de258776b9`, y los índices (LIFT_OK-2, DROP_OK-13) coinciden con su posición en la secuencia de 14 mensajes de la misión (captura:2-15). Eso indica que la captura sale de una sola ejecución del código auditado.
- Orden de los ts: el ts de conexion EN_LINEA (…490118) es posterior al de la primera telemetría (…490009). Se explica porque la misión se genera con tiempo simulado antes de conectar. No incumple CA-1.2.6, que solo exige que los mensajes aparezcan. Por la regla de hallazgos congelados no se registra como observación nueva.
- Límite de la verificación: la captura es evidencia humana. Que viene de un broker real se infiere del formato `-v` y de la coherencia interna; no se reprodujo (es un criterio [S]).

## Hallazgos
No hay hallazgos nuevos. Observaciones abiertas de it2, sin repetirlas como hallazgos nuevos:
- H-2 [Observación], abierta: comentario desactualizado en robot_falso.py:23-24, que no cita CC-002.
- H-3 [Observación], abierta: el `connect` no captura errores y `wait_for_publish` no tiene timeout (robot_falso.py:106, 111).

El informe de ejecución (docs/pm/auditorias/WP-1.2_it3_ejecucion.md:5) explica que no se corrigieron para no modificar simulador/ después de la captura. Es razonable. Se pueden atender en un WP posterior que toque el simulador, lo que dispararía una reverificación.

## Alcance, integridad y regresión
- **Alcance:** el commit b7c751b solo añade docs/pm/auditorias/WP-1.2_it3_ejecucion.md y docs/pm/evidencia/WP-1.2/captura_mosquitto.txt. Es un commit `[pm]` de evidencia, sin código.
- **Integridad:** entre d506661 y HEAD no cambiaron simulador/, requirements.txt, .env.example ni tests/aceptacion/. 03-wbs.md no cambió.
- **Evidencia:** el log corresponde a HEAD b7c751b, con "Árbol limpio: sí" (log:2-4).
- **Regresión:** ningún test de test_wp_1_1.py ni de test_wp_1_2.py falla. Los 49 que pasan son los mismos que en it2. Los fallos y errores restantes son ModuleNotFoundError de WPs aún no ejecutados.
- **Credenciales:** la captura no contiene host, usuario ni contraseña. El código no cambió respecto de it2, que no tenía credenciales escritas.

## Hallazgos de iteraciones previas: cerrados / persistentes
- H-1 [Mayor], faltaba la evidencia de CA-1.2.6: **cerrado**.
- H-2 [Observación]: **persistente**, no bloquea.
- H-3 [Observación]: **persistente**, no bloquea.
