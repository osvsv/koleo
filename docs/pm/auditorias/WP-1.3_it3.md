# Auditoría WP-1.3 — iteración 3
Dictamen: CONFORME CON OBSERVACIONES
Commit: ff005142031c43ea3835b11c524e637ff7b16360
Evidencia: docs/pm/evidencia/WP-1.3_it3_aceptacion_ff00514.log
Archivos auditados: backend/__init__.py, backend/koleo/__init__.py, backend/koleo/api.py, backend/koleo/ingesta.py, backend/koleo/suscriptor.py, .env.example

**Resumen:** H-1, el único hallazgo de la it2, queda cerrado. Ahora el rechazo SOBREPESO toma las coordenadas solo de la fila `robots`, aunque el evento traiga `x_cm`/`y_cm`. No hay regresión. No aparecen hallazgos Mayores nuevos. Siguen abiertas las observaciones O-1, O-2 y O-3 de la it2, que no bloquean. La captura de CA-1.3.9 sigue siendo válida y no hace falta repetirla.

**Límite de la auditoría:** igual que en la it2, no se pudo leer `.env.example` porque lo bloquea una regla de permisos, y no se rodeó. Se verificó que ese archivo no cambió desde la it2: `git diff a189891..HEAD --stat` solo muestra `backend/koleo/ingesta.py` y `docs/pm/auditorias/WP-1.3_it3_ejecucion.md`. **No se puede afirmar que `.env.example` esté libre de valores reales de credenciales.** El usuario debe confirmar que solo contiene nombres de variables.

## Verificación por criterio
Se aplica la regla de hallazgos congelados: los criterios CA-1.3.1 a CA-1.3.11 no se reabren. Solo se confirma que siguen en pie con la evidencia nueva.

| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-1.3.1 a CA-1.3.8, CA-1.3.10, CA-1.3.11 | Cumplen (sin cambios desde la it2) | El log de ff00514 (árbol limpio, según el JSON) termina en "48 failed, 68 passed in 1.24s" (línea 908). Ninguna de las líneas FAILED (860-907) es de test_wp_1_3.py. f0e6c36 solo cambia ingesta.py:157, dentro de la rama `elif tipo == "SOBREPESO"`, así que no toca DROP_OK, LIFT_OK, la validación, la API ni la telemetría |
| CA-1.3.9 | Cumple (evidencia humana de e126fe0, sigue siendo válida) | Ver "Validez de la captura de CA-1.3.9" |
| CA-1.3.12 | Cumple | ingesta.py:151-157: `x, y` salen de `SELECT x_cm, y_cm FROM robots WHERE robot_id=?` y se insertan sin mirar el payload. `_robot` (ingesta.py:144) asegura que la fila exista, así que sin telemetría previa `x_cm`/`y_cm` quedan en NULL. test_ca_1_3_12 (los dos casos) pasa según el log |

## Validez de la captura de CA-1.3.9
- `git diff --stat e126fe0 HEAD` muestra que, fuera de docs/pm y .env.example, solo cambió `backend/koleo/ingesta.py`, en una sola línea (f0e6c36).
- El cambio pasa de `p.get("x_cm", x), p.get("y_cm", y)` a `x, y`. Si el evento no trae `x_cm`/`y_cm`, las dos expresiones dan el mismo valor.
- El simulador emite el SOBREPESO con `evento("SOBREPESO", peso_kg=peso_kg)` (simulador/robot_falso.py:78). El helper `evento` (líneas 68-73) solo pone ts, robot_id, tipo, id_evento e id_tarima, más los extras, y no añade coordenadas. Con la captura, el código anterior y el nuevo dan exactamente las mismas filas: el rechazo de TAR-102 en (0, 0), tomado de la telemetría ELEVANDO.
- Conclusión: el cambio no puede alterar lo capturado y no hace falta repetir la corrida.

## Predicciones frente a lo observado
Las predicciones de la it2 (docs/pm/auditorias/WP-1.3_it2_predicciones.md) no se repiten. La única divergencia abierta era la precedencia de coordenadas en el rechazo, origen de H-1. Ahora el comportamiento coincide con la predicción: coordenadas de la última telemetría, o NULL si no hubo.

## Hallazgos
No hay hallazgos nuevos. Las observaciones abiertas de la it2 se listan sin repetirlas:
- O-1 [Observación]: tiempo_ciclo_s no comprueba que el LIFT_OK sea de la misma tarima. Abierta.
- O-2 [Observación]: el suscriptor registra un WARNING por cada mensaje de los temas esp32/*. Abierta.
- O-3 [Observación]: `executescript` en `asegurar_tablas` confirma las transacciones pendientes de quien llama. Abierta.

Nota sin rango de hallazgo (las reglas de congelación no permiten agregar observaciones nuevas): ninguna prueba de aceptación cubre el caso de H-1, un SOBREPESO con `x_cm`/`y_cm` distintos de los de la telemetría. El cierre está verificado leyendo el código, no ejecutándolo. El ejecutor lo señala en WP-1.3_it3_ejecucion.md:6. Si se quiere esa prueba, se añade con /pm-cambio.

## Alcance, integridad y regresión
- **Alcance:** f0e6c36 solo modifica `backend/koleo/ingesta.py` (+1/−1), dentro de `backend/**`.
- **Integridad de docs/pm:** el commit de trabajo f0e6c36 no toca docs/pm/. ff00514 es un commit `[pm]` que solo añade WP-1.3_it3_ejecucion.md.
- **Regresión:** la it2 (39e1607) y la it3 (ff00514) dan el mismo resultado, 68 passed y 48 failed. No hay ninguna línea FAILED de test_wp_1_1.py, test_wp_1_2.py ni test_wp_1_3.py. Los 48 fallos son de WP pendientes, ya presentes antes: test_wp_3_2 y test_wp_4_1 a test_wp_4_4 fallan porque no existe el módulo `pi`, y test_wp_5_2 da 405 en los POST.
- **Credenciales:** una búsqueda en backend/ (password, secret, token, clave) solo encuentra lecturas de variables de entorno (suscriptor.py:4, 27, 31, 69). No hay credenciales escritas en el código. El límite sobre `.env.example` está explicado al principio.

## Hallazgos de iteraciones previas: cerrados / persistentes
- **H-1 [Menor], cerrado.** backend/koleo/ingesta.py:157 ahora inserta `(id_tarima, p["peso_kg"], "SOBREPESO", x, y, _iso(ts))`. `x, y` salen solo de la fila `robots` (ingesta.py:151-152) y son NULL si no hubo telemetría.
- **O-1, O-2 y O-3 (Observación), persistentes.** No bloquean.
