# Auditoría WP-1.2 — iteración 2
Dictamen: NO CONFORME
Commit: d50666110a31c51edafc64a9d1e8642eabb75874
Evidencia: docs/pm/evidencia/WP-1.2_it2_aceptacion_d506661.log
Archivos auditados: simulador/__init__.py, simulador/robot_falso.py, requirements.txt, .env.example

**Resumen:** el código del simulador cumple CA-1.2.1 a CA-1.2.5 y CA-1.2.7, y no hay regresión. El único bloqueo es que falta la evidencia de CA-1.2.6 (la captura con mosquitto). Eso no se arregla con código: se cierra cuando una persona agrega la captura.

## Verificación por criterio
| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-1.2.1 | Cumple | El log no lista fallos de test_wp_1_2.py (log:1146-1207, "53 failed, 49 passed, 8 errors"). Lo confirmé con `python -m pytest tests/aceptacion/test_wp_1_2.py tests/aceptacion/test_wp_1_1.py -v`, que da 49 passed: los 3 tests de CA-1.2.1 pasan. En el código: el LIFT_OK de TAR-101 está en robot_falso.py:81. El DROP_OK es el último mensaje, en (150, 120) (robot_falso.py:85-87). El `id_evento` es único: usa uuid por corrida más la posición del mensaje (robot_falso.py:57 y 71). |
| CA-1.2.2 | Cumple | Pasa test_ca_1_2_2_sobrepeso_sin_lift_ni_drop. Si el peso supera el límite, se emite SOBREPESO y la función retorna antes de LIFT_OK y DROP_OK (robot_falso.py:77-80). |
| CA-1.2.3 | Cumple | Los dos tests de CA-1.2.3 pasan. La comparación es `peso_kg > LIMITE_KG` con LIMITE_KG = 10.0 (robot_falso.py:16 y 77), así que el límite es inclusivo. |
| CA-1.2.4 | Cumple | Pasa test_ca_1_2_4_ruta_desconocida (robot_falso.py:46-47). |
| CA-1.2.5 | Cumple | Pasa el test parametrizado para RUTA_1 y RUTA_3. El paso fijo es PASO_MS = 500 (robot_falso.py:17 y 66), así que el intervalo es exactamente 500 ms. |
| CA-1.2.6 | Sin evidencia: no se puede verificar | No existe docs/pm/evidencia/WP-1.2/captura_mosquitto.txt (`ls docs/pm/evidencia` no tiene subcarpeta WP-1.2). El código de publicación existe (robot_falso.py:91-124), pero leer el código no sustituye la evidencia que exige el diccionario. Ver H-1. |
| CA-1.2.7 | Cumple | Los 3 casos de test_ca_1_2_7_meta_y_tarima_de_cada_ruta pasan. RUTAS en robot_falso.py:25-29 coincide con CC-002, con la conversión x = columna×30 e y = fila×30 (robot_falso.py:40-41). |

## Predicciones frente a lo observado
No aplica (riesgo bajo).

## Hallazgos
### H-1 [Mayor] CA-1.2.6 no tiene la evidencia que define el diccionario
- Criterio o requisito afectado: CA-1.2.6 (y la parte "publica" de REQ-F-015).
- Evidencia: no existe el archivo `docs/pm/evidencia/WP-1.2/captura_mosquitto.txt`. El informe de ejecución (docs/pm/auditorias/WP-1.2_it2_ejecucion.md:3) lo reconoce como "pendiente de captura humana". La línea base no prevé dar por cumplido un criterio sin su evidencia: CLAUDE.md del proyecto dice "Nada se considera terminado sin dictamen CONFORME del auditor y evidencia". En la auditoría no hay evidencia objetiva de que los mensajes lleguen a un broker real.
- Qué tendría que ser cierto para cerrarlo: una persona ejecuta `python -m simulador.robot_falso --ruta RUTA_1 --peso 8.45 --broker <host>` con `mosquitto_sub -t 'koleo/#' -v` abierto y guarda la salida en docs/pm/evidencia/WP-1.2/captura_mosquitto.txt. La salida debe mostrar al menos: `koleo/robot1/conexion` con EN_LINEA; la telemetría; los eventos LIFT_OK y DROP_OK; FUERA_DE_LINEA al final. No hace falta cambiar código. Lo ideal es que la captura se haga sobre el mismo commit auditado o uno sin cambios en simulador/. Así, la iteración 3 solo tiene que verificar que el archivo existe y es coherente.

### H-2 [Observación] Comentario desactualizado tras CC-002
- Criterio o requisito afectado: ninguno (mantenibilidad).
- Evidencia: robot_falso.py:23-24 sigue diciendo que las metas de RUTA_2 y RUTA_3 "son supuestos del simulador". Desde CC-002 forman parte de la línea base (CA-1.2.7).
- Qué tendría que ser cierto para cerrarlo: que el comentario cite CC-002 / CA-1.2.7.

### H-3 [Observación] La publicación MQTT no tolera fallos de red
- Criterio o requisito afectado: ninguno directamente (CA-1.2.6 solo pide que los mensajes aparezcan).
- Evidencia: si el broker no está disponible, `cli.connect` (robot_falso.py:106) termina con un traceback en lugar de un mensaje claro. Además, `info.wait_for_publish()` (robot_falso.py:111) no tiene tiempo de espera, así que puede bloquearse si se pierde la conexión.
- Qué tendría que ser cierto para cerrarlo: capturar el error de conexión con un mensaje y código de salida, y usar `wait_for_publish(timeout=...)`.

## Alcance, integridad y regresión
- **Alcance.** El commit de trabajo 415d9cc toca simulador/__init__.py y simulador/robot_falso.py (dentro de `simulador/**`), requirements.txt (+`paho-mqtt==2.1.0`) y .env.example (3 líneas añadidas). Las dos últimas están registradas en docs/pm/desviaciones.md:5-6. simulador/__main__.py no está versionado, lo que coincide con el informe de ejecución.
- **Integridad de docs/pm/.** 415d9cc no toca docs/pm/. Los cambios en docs/pm/ están en commits `[pm]` separados: ba81c83 y d506661. La prueba test_wp_1_2.py solo cambió en 579ebab (CC-002, aprobado), que agrega los casos de CA-1.2.7 sin tocar ni relajar los anteriores.
- **Evidencia.** El log corresponde a HEAD d506661, con "Árbol limpio: sí". El JSON asociado tiene el mismo commit.
- **Regresión.** Ningún test de test_wp_1_1.py ni de test_wp_1_2.py aparece entre los fallos del log (49 passed: 12 de WP-1.2 y 37 de WP-1.1). Todos los fallos y errores restantes son ModuleNotFoundError de `backend` o `pi`, de WPs aún no ejecutados.
- **Credenciales.** robot_falso.py no tiene credenciales escritas: lee KOLEO_MQTT_PORT, KOLEO_MQTT_USER y KOLEO_MQTT_PASSWORD del entorno. Límite de la verificación: no se leyó .env.example por una regla de permisos; solo se verificó que tiene 3 líneas añadidas. Que no contenga valores se apoya en la afirmación del usuario, no en evidencia inspeccionada. No hay un .gitignore versionado que excluya .env (fuera del alcance de este WP).

## Hallazgos de iteraciones previas: cerrados / persistentes
No hay informes de auditoría previos: la iteración 1 terminó en bloqueo, resuelto con CC-002.
