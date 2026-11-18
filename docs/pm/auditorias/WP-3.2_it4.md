# Auditoría WP-3.2 — iteración 4
Dictamen: CONFORME CON OBSERVACIONES
Commit: 067ff2094cebda3ae9b862867b4cd86e8a666aec
Evidencia: docs/pm/evidencia/WP-3.2_it4_aceptacion_067ff20.log
Archivos auditados: pi/enlace.py, firmware/.gitignore, firmware/esp32/platformio.ini, firmware/esp32/src/main.cpp, firmware/esp32/src/red_mqtt.cpp, firmware/esp32/src/red_mqtt.h, firmware/esp32/src/secrets.example.h

**Resumen:** el único hallazgo bloqueante de it3, H-1 [Línea base], está cerrado. CC-018 (opción A) ajustó el texto de SUP-035 y del entregable de WP-3.2, que ya no contradicen `contratos/esp32.md:28` ni CA-3.2.2. El código, las pruebas y los contratos no cambiaron desde 7831656, así que los cuatro criterios vigentes siguen cumpliéndose. No hay hallazgos Mayores, Menores ni de Línea base. Siguen abiertas O-1 y O-2, que no bloquean y se cierran en WP-6.1.

## Verificación por criterio
| Criterio | Resultado | Evidencia |
| --- | --- | --- |
| CA-3.2.1 | Cumple | Log it4 línea 962: `49 failed, 111 passed`. Ninguna prueba de test_wp_3_2 entre los FAILED (líneas 913-961, todas de test_wp_4_1, 4_2 y 4_3). `git diff --stat 7831656 HEAD -- pi firmware contratos tests` vacío; sigue en pie lo verificado en it3 (pi/enlace.py:41-44 y 53-54). |
| CA-3.2.2 | Cumple | Las pruebas de 3.2 no fallan. Código sin cambios: pi/enlace.py:45-51 lanza TimeoutError a 1 s, envía STOP sin recursión y no reintenta; ahora coincide con SUP-035 y con el entregable (03-wbs.md:173). |
| CA-3.2.3 | Cumple | Las pruebas de 3.2 no fallan. Código sin cambios (pi/enlace.py:20-21 y 57). |
| CA-3.2.6 | Cumple (por inspección, ver O-1) | firmware/ no cambió. En it3: firmware/.gitignore:1 `esp32/src/secrets.h`, sin secrets.h en el historial y sin credenciales literales. |

## Predicciones frente a lo observado
Valen las de it3 (docs/pm/auditorias/WP-3.2_it3_predicciones.md): el código no cambió. La única divergencia de it3, el reenvío de SUP-035, desaparece: la línea base pide ahora lo que el código hace. `enviar` no reintenta y conserva el `id_cmd` dado; el firmware mantiene su caché de idempotencia, que CC-018 conserva de forma explícita.

## Hallazgos
### O-1 [Observación] CA-3.2.6 verificado por inspección (abierta desde it3)
Se cierra en WP-6.1 con el `secrets.h` real, cuando `git check-ignore -v` muestre `firmware/.gitignore:1`.

### O-2 [Observación] Firmware sin compilar (abierta desde it3)
PlatformIO no está instalado. Se cierra en WP-6.1 (CA-6.1.5 a 6.1.8).

## Alcance, integridad y regresión
- Código: `git diff --stat 7831656 HEAD -- pi firmware contratos tests` vacío.
- Línea base: `git diff 7831656 HEAD` solo toca `docs/pm/` en commits [pm] (auditoría y predicciones de it3, CC-018 y estado). CC-018 cambió solo 03-wbs.md (versión 1.18 y el entregable de WP-3.2, línea 173), supuestos.md:40 (SUP-035) y cambios.md:22. Criterios, alcance de archivos e interfaz de WP-3.2 sin cambios.
- Evidencia: el .json indica commit 067ff2094cebda3ae9b862867b4cd86e8a666aec, `arbol_limpio: true`; código 1 solo por fallos de WP pendientes.
- Regresión: 111 aprobadas y 49 falladas, igual que en it3; todas de test_wp_4_1, 4_2 y 4_3. Sin regresión.
- Credenciales: ninguna en el código.

## Hallazgos de iteraciones previas
- **H-1 [Línea base] Reenvío con el mismo `id_cmd` frente a "No hay reintento": CERRADO.** docs/pm/supuestos.md:40 (SUP-035) y docs/pm/03-wbs.md:173 dicen ahora que la Pi no reintenta y que una `resp` perdida termina en `TimeoutError` a 1 s, `STOP` y aborto de la misión, con el firmware conservando su caché de idempotencia (aclarado por Osvaldo, CC-018). contratos/esp32.md:28 sigue diciendo "No hay reintento del comando": los tres documentos coinciden, y con CA-3.2.2 y CA-4.3.6. CC-013 conserva su texto como historial y CC-018 declara que su frase sobre el reenvío queda sustituida. Las demás menciones de "reenv"/"reintent" (charter:23, 03-wbs.md:76, REQ-F-017/EJ-034) tratan otros casos y no contradicen.
- O-1 y O-2: persisten, no bloquean; su cierre queda asignado a WP-6.1.
