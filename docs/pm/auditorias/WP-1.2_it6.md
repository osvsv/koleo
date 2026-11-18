# Auditoría WP-1.2 — iteración 6
Dictamen: CONFORME CON OBSERVACIONES
Commit: 305a12c0746661d7f13921506990d6ab96b2c4d0
Evidencia: docs/pm/evidencia/WP-1.2_it6_aceptacion_305a12c.log
Archivos auditados: simulador/__init__.py, simulador/robot_falso.py, requirements.txt, .env.example, docs/pm/evidencia/WP-1.2/captura_mosquitto.txt
Tipo: reverificación

**Resumen:** desde el dictamen vigente (7ccd096), un solo commit tocó archivos auditados de WP-1.2: cf346a5, de WP-4.4, que en requirements.txt cambia `opencv-python-headless==5.0.0.93` por `rplidar==0.9.2`. El simulador no importa ninguno de los dos paquetes, `paho-mqtt==2.1.0` sigue igual y las pruebas de test_wp_1_2.py pasan en el log de HEAD. Sin hallazgos nuevos. Las dos observaciones previas (H-2, H-3) siguen abiertas.

## Verificación por criterio
| Criterio | Resultado | Evidencia |
| --- | --- | --- |
| CA-1.2.1 a CA-1.2.5, CA-1.2.7 | Cumple | Log de HEAD 305a12c: 49 failed, 111 passed; las 49 fallas son solo de test_wp_4_1, 4_2 y 4_3. Ninguna prueba de test_wp_1_2.py falla. |
| CA-1.2.6 | Cumple | Desde 7ccd096 ningún commit toca docs/pm/evidencia/WP-1.2. |

## Cambios reverificados
| Commit | WP de origen | Archivo | Efecto |
| --- | --- | --- | --- |
| cf346a5 | WP-4.4 | requirements.txt (-opencv-python-headless, +rplidar==0.9.2) | Dentro del alcance de WP-4.4 (CA-4.4.7, CC-014). El simulador solo importa la biblioteca estándar y paho.mqtt. Sin efecto en criterios de WP-1.2. |

## Hallazgos
Sin hallazgos nuevos.

- H-1 [Mayor] (it2): cerrado.
- H-2 [Observación]: abierta. Comentario de simulador/robot_falso.py:23-24 desactualizado, no cita CC-002.
- H-3 [Observación]: abierta. `connect` no captura errores y `wait_for_publish` no tiene timeout (simulador/robot_falso.py:106, 111).

## Alcance, integridad y regresión
- Alcance: único cambio en archivo auditado es cf346a5, dentro del alcance de WP-4.4.
- Integridad: "Árbol limpio: no" solo por docs/pm/uso.csv (hook de sesión) y la evidencia sin seguimiento.
- Regresión: 111 pasan (73 en it5), 49 fallan (51 en it5), todas de WP pendientes. Sin regresión.
- Nota (asunto de WP-4.4 y la línea base): la fila 8 de docs/pm/desviaciones.md, que registra `opencv-python-headless`, ya no corresponde al estado de requirements.txt.
