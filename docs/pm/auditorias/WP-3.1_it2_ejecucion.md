# Ejecución WP-3.1 — iteración 2
Resultado: LISTO (con una desviación de alcance no resuelta: LEEME.md)

Archivos modificados (firmware/esp32/): src/elevacion.h, src/elevacion.cpp, src/main.cpp, test/test_elevacion.cpp.

## Corrección por hallazgo
- H-1 y H-2: no aplican por CC-010 (la evidencia de banco pasó a WP-3.2 como CA-3.2.7 y CA-3.2.8, por MQTT). No se generaron peso_invalido.txt ni umbral.txt.
- H-3: `elevacionSolicitar` delega en `elevacionSolicitarEn(texto, ahoraMs)`. Con la elevación activa, un LIFT válido devuelve LIFT_OK sin tocar `g_inicioMs` ni volver a energizar. Tras el apagado por tiempo, un LIFT nuevo inicia otro ciclo.
- H-4: `evaluarLift` compara el double contra 10.0 antes de convertir a float.
- H-5 (parcial): el buffer `linea` de main.cpp queda acotado a 64 caracteres.
- Pruebas nuevas en test/test_elevacion.cpp: LIFT a t=1000 y otro a t=5000, sigue activo en 8999 y se apaga en 9000; "10.0000000001" da OVERWEIGHT.

## Autoverificación
- `g++ -Wall -I src test/test_elevacion.cpp src/elevacion.cpp`: sin advertencias, imprime "OK", pasan los asserts antiguos y los nuevos.
- PlatformIO no está instalado en este equipo: no se compiló para ESP32. main.cpp y la rama `#ifdef ARDUINO` no están compilados ni probados.
- pines.h y GPIO 14 sin cambios (CA-3.1.1). Pesos ausentes, no numéricos, 0, negativos o NaN siguen dando PESO_INVALIDO (CA-3.1.2). Sigue usando millis() sin delay(), máximo 8 s (CA-3.1.6).

## Desviaciones
| Archivo o criterio | Categoría | Nota |
| --- | --- | --- |
| docs/pm/evidencia/hw/WP-3.1/LEEME.md | alcance | El ejecutor intentó actualizarlo a CC-010 y el hook guard_paths bloqueó la escritura en docs/pm/. No lo eludió. LEEME.md sigue diciendo que peso_invalido.txt y umbral.txt están pendientes, lo cual contradice CC-010. Queda a decisión del usuario. |

Bloqueos con la línea base: ninguno. Variables de entorno nuevas: ninguna.
