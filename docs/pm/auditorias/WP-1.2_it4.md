# Auditoría WP-1.2 — iteración 4
Dictamen: CONFORME CON OBSERVACIONES
Commit: 615282dce725dd788961d9de22c3cfa483816ba4
Evidencia: docs/pm/evidencia/WP-1.2_it4_aceptacion_615282d.log
Archivos auditados: simulador/__init__.py, simulador/robot_falso.py, requirements.txt, .env.example, docs/pm/evidencia/WP-1.2/captura_mosquitto.txt
Tipo: reverificación

**Resumen:** desde b7c751b solo cambió uno de los archivos auditados: .env.example, en el commit afd042b de WP-1.3. Los demás son idénticos. No hay ningún fallo de WP-1.2 en el log de HEAD, no hay regresión y no hay hallazgos nuevos. Hay una salvedad: no se pudo leer .env.example, así que el usuario tiene que confirmar que no contiene valores reales.

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-1.2.1 | Cumple | El log de 615282d dice "Árbol limpio: sí" (log:2-4) y termina en "48 failed, 68 passed" (log:908). Ninguna línea FAILED o ERROR es de test_wp_1_2.py (log:860-907); todas son de test_wp_3_2, 4_1, 4_2, 4_3, 4_4 y 5_2, por ModuleNotFoundError. `git diff --stat b7c751b..HEAD` sobre simulador/__init__.py, simulador/robot_falso.py y requirements.txt no muestra nada. |
| CA-1.2.2 | Cumple | Igual que CA-1.2.1: el test no falla y el código no cambió. |
| CA-1.2.3 | Cumple | Igual que CA-1.2.1. |
| CA-1.2.4 | Cumple | Igual que CA-1.2.1. |
| CA-1.2.5 | Cumple | Igual que CA-1.2.1. |
| CA-1.2.6 | Cumple | La captura es idéntica a la de b7c751b. `git diff --stat b7c751b -- docs/pm/evidencia/WP-1.2/captura_mosquitto.txt`, que compara el árbol de trabajo contra b7c751b, no muestra nada. Así que la restauración que hizo el usuario con git checkout es fiel, y la verificación de it3 sigue en pie. |
| CA-1.2.7 | Cumple | Igual que CA-1.2.1. |

Las 9 funciones de test de tests/aceptacion/test_wp_1_2.py no cambiaron desde b7c751b: `git log b7c751b..HEAD` sobre ese archivo no muestra commits, y `git diff b7c751b` tampoco muestra cambios. Las pruebas no se debilitaron.

## Cambios reverificados
| Commit | WP de origen | Archivo | Efecto |
| --- | --- | --- | --- |
| afd042b "[WP-1.3] it2: variables de entorno del backend en .env.example" | WP-1.3 | .env.example (+6/−1, 7 líneas tocadas) | Registrado en docs/pm/desviaciones.md:7 como "Variables KOLEO_MQTT_HOST, KOLEO_DB_PATH, KOLEO_API_HOST y KOLEO_API_PORT sin valores (lo creó el usuario)". El tamaño del cambio cuadra con cuatro variables nuevas más algún comentario o reemplazo de línea. No afecta a ningún criterio de WP-1.2: el simulador no lee .env.example, que es solo una plantilla. |

Ningún otro commit entre b7c751b y HEAD toca archivos auditados de WP-1.2 (`git log --name-only b7c751b..HEAD`): el resto son commits de backend/ (WP-1.3) y de docs/pm/.

**Límite de la verificación:** una regla de permisos impide leer .env.example; tampoco se puede ver su diff. No se intentó rodear. Por eso **no se puede afirmar que .env.example esté libre de valores reales**: la desviación declara "sin valores", pero no se verificó. El usuario debe confirmarlo, en particular que no haya contraseñas, usuarios ni hosts reales en las líneas de KOLEO_MQTT_*.

## Hallazgos
No hay hallazgos nuevos que nazcan del diff.

Observaciones abiertas del dictamen anterior (solo se listan, no se repiten):
- H-2 [Observación], abierta: comentario desactualizado en simulador/robot_falso.py:23-24, que no cita CC-002.
- H-3 [Observación], abierta: el `connect` no captura errores y `wait_for_publish` no tiene timeout (simulador/robot_falso.py:106, 111).

## Alcance, integridad y regresión
- **Alcance:** el único cambio en un archivo auditado (afd042b) pertenece a WP-1.3 y está registrado en desviaciones.md:7.
- **Integridad:** simulador/, requirements.txt, la captura y test_wp_1_2.py no cambiaron desde b7c751b.
- **Evidencia:** el log corresponde a HEAD 615282d con árbol limpio (log:2-4).
- **Regresión:** pasan 68 pruebas, frente a 49 en it3; el aumento corresponde a las pruebas de WP-1.3. Ningún test de test_wp_1_1.py, test_wp_1_2.py ni test_wp_1_3.py figura como fallido. Los 48 fallos son ModuleNotFoundError de WP aún no ejecutados (3.2, 4.x, 5.2).
- **Credenciales:** el código del simulador no cambió y ya estaba limpio. Sobre .env.example no hay dictamen posible por el límite de permisos descrito arriba; queda pendiente de que lo confirme el usuario.

## Hallazgos de iteraciones previas: cerrados / persistentes
- H-1 [Mayor] (it2): sigue **cerrado**. La captura no cambió.
- H-2 [Observación]: **persistente**, no bloquea.
- H-3 [Observación]: **persistente**, no bloquea.
