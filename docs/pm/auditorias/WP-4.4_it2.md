# Auditoría WP-4.4 — iteración 2
Dictamen: CONFORME CON OBSERVACIONES
Commit: bc9f6a6cbc546018acd3ee51a53b2e1c8d0c48f2
Evidencia: docs/pm/evidencia/WP-4.4_it2_aceptacion_bc9f6a6.log
Archivos auditados: pi/lidar.py, pi/rplidar.py, requirements.txt, pi/qr.py, pi/camara.py

## Verificación por criterio
Usé el log indicado porque corresponde a HEAD (`Commit: bc9f6a6cbc546018acd3ee51a53b2e1c8d0c48f2`). Resultado de la suite: 160 pruebas, 111 pasan y 49 fallan. Ninguna de las que fallan es de `test_wp_4_4.py`, así que las 18 pruebas de WP-4.4 pasan.

| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
| --- | --- | --- |
| CA-4.4.1 | Cumple | Log: `test_ca_4_4_1_poste_de_6_cm_a_100_cm_y_20_grados` no aparece entre los FAILED (100±3 cm, 20±2°). En `pi/lidar.py:46-48` la distancia y el rumbo salen del promedio del grupo. |
| CA-4.4.2 | Cumple | Log: pasan las 3 pruebas de CA-4.4.2 (pared, vacío, puntos sueltos). Los grupos con menos de `min_puntos` y los de cuerda mayor que 12 cm se descartan en `pi/lidar.py:42-46`. |
| CA-4.4.3 | Cumple | Log: pasa `test_ca_4_4_3_tarima_no_es_poste[18/40]`. El descarte por cuerda está en `pi/lidar.py:44-46`. |
| CA-4.4.4 | Cumple | Log: pasan las 3 pruebas (poste frente a pared, en el eje y a 20°, y dos postes). Devuelve el más cercano con `min(..., key=distancia_cm)` en `pi/lidar.py:52`. |
| CA-4.4.5 | Cumple | Log: pasan las 4 pruebas. El filtro `distancia_min_cm <= d <= alcance_max_cm` se aplica antes de agrupar, en `pi/lidar.py:28-32`. |
| CA-4.4.6 | Cumple | Log: pasan las 3 pruebas. mm a cm en `pi/rplidar.py:60-64`. Ante timeout lanza `LidarSinDatos` (`pi/rplidar.py:53-57`). El puerto sale de `KOLEO_LIDAR_PUERTO` (`pi/rplidar.py:16-20`) y no hay puertos `/dev/tty` ni `COMn` fijos en `pi/`. |
| CA-4.4.7 | Cumple | `ls pi` muestra solo `__init__.py`, `enlace.py`, `lidar.py` y `rplidar.py`. `git show cf346a5 -- requirements.txt` quita `opencv-python-headless==5.0.0.93` y añade `rplidar==0.9.2`. Las 2 pruebas de inspección pasan. |
| CA-4.4.8 | No aplica | Pasó a WP-6.2 como CA-6.2.4 (CC-015). |

## Predicciones frente a lo observado
No aplica: el WP es de riesgo medio.

## Hallazgos
### H-1 [Observación] Con la resolución real del A1, el poste de 6 cm queda al límite de `min_puntos=2` y de la separación de 5 cm
- Criterio o requisito afectado: ninguno de WP-4.4, porque las pruebas usan escaneos sintéticos a 1°. Es un riesgo para CA-6.2.4 (WP-6.2) y para CA-4.3.4, que arranca a 120 cm.
- Evidencia: en la Pi el sensor da ≈137 puntos por vuelta, o sea ≈2.6° entre puntos. Un poste de 6 cm a 100 cm ocupa ≈3.4°, así que devuelve 1 o 2 puntos. A esa resolución, dos puntos vecinos quedan a ≈4.6 cm a 100 cm y a ≈5.0 cm a 110 cm. Con `SEPARACION_GRUPO_CM = 5.0` (`pi/lidar.py:8`, valor que fija la interfaz) y `min_puntos=2`, el poste de 6 cm deja de agruparse más allá de ≈108 cm y a 100 cm puede salir con un solo punto, de forma intermitente. La implementación sigue la línea base. Los parámetros salen de la interfaz, no del ejecutor.
- Qué tendría que ser cierto para cerrarlo: antes de WP-6.2, confirmar con escaneos reales que se detectan 5 de 5. Si no, usar un poste de 8 a 10 cm (dentro de SUP-036) o ajustar por `/pm-cambio` el umbral de agrupación o `min_puntos`.

### H-2 [Observación] `escanear` puede devolver una vuelta parcial y deja vivo el hilo lector cuando hay timeout
- Criterio o requisito afectado: la interfaz pide "una vuelta completa". CA-4.4.6 se cumple con el driver falso.
- Evidencia: en `pi/rplidar.py:41-47` cada llamada crea un `iter_scans()` nuevo y se queda con la primera vuelta que entrega. Según el `iter_scans` de `rplidar` 0.9.2, esa primera vuelta junta las muestras previas a la primera marca de vuelta nueva, que suele ser un arco parcial. No lo pude verificar contra el código de la biblioteca porque no está instalada en `.venv` local. Además, cuando hay timeout el hilo daemon sigue bloqueado leyendo del puerto serie, y la llamada siguiente arranca otro lector sobre el mismo puerto. El propio ejecutor lo deja como pendiente en `docs/pm/auditorias/WP-4.4_it2_ejecucion.md:11`.
- Qué tendría que ser cierto para cerrarlo: verificar en WP-6.2 que el número de puntos por llamada sea estable (≈135-140). Si no lo es, descartar la primera vuelta o mantener un único iterador abierto.

### H-3 [Observación] Agrupación y rumbo en el corte de ±180°
- Criterio o requisito afectado: ninguno, porque los criterios no contemplan un poste detrás del robot.
- Evidencia: en `pi/lidar.py:28-38` se ordena por ángulo normalizado a [-180, 180) y no se une el último grupo con el primero. En `pi/lidar.py:48` el rumbo es una media aritmética. Un poste a ≈180° se parte en dos grupos o sale con un rumbo cercano a 0°.
- Qué tendría que ser cierto para cerrarlo: unir el grupo final con el inicial cuando los separan menos de 5 cm y promediar el ángulo como vector. Es opcional.

### H-4 [Observación] Falta `KOLEO_LIDAR_PUERTO` en `.env.example`
- Criterio o requisito afectado: ninguno. CA-4.4.6 solo pide leer la variable y no tener valores fijos.
- Evidencia: el docstring de `pi/rplidar.py:3` remite a `.env.example`. El ejecutor dice que no pudo editarlo por permisos (informe de ejecución, línea 9). Yo tampoco pude leerlo, por el mismo motivo.
- Qué tendría que ser cierto para cerrarlo: que el usuario añada `KOLEO_LIDAR_PUERTO=`, sin valor, a `.env.example`.

## Alcance, integridad y regresión
- **Alcance:** `git show --stat cf346a5` toca solo `pi/camara.py` (eliminado), `pi/lidar.py`, `pi/qr.py` (eliminado), `pi/rplidar.py` y `requirements.txt`. Todos están en el Alcance de archivos de WP-4.4. Ningún archivo de `docs/pm/` cambió en el commit del WP. `bc9f6a6` es el commit del método y solo añade `docs/pm/auditorias/WP-4.4_it2_ejecucion.md`.
- **Credenciales:** no hay credenciales ni puertos fijos en el código.
- **Regresión:** los 49 fallos son de WP-4.1, WP-4.2 y WP-4.3. Todos son `ModuleNotFoundError` o `ImportError` de `pi.puente_mqtt`, `pi.ordenes`, `pi.odometria`, `pi.mision` y `pi.navegacion`. Esos módulos no han existido nunca en el historial y los tres WP están "Pendiente" en `estado.md`. No son regresiones. Las pruebas de WP-1.x, 3.2 y 5.2 pasan.
- **Reverificación de WP-1.2:** `requirements.txt` es un archivo auditado de WP-1.2, que ya está conforme, así que WP-1.2 queda para reverificación. El cambio solo cambia opencv por rplidar.
- **Árbol:** el log indica "Árbol limpio: no" por archivos sin seguimiento (`Project`, los propios archivos de evidencia). Ninguno afecta las pruebas.

## Hallazgos de iteraciones previas: cerrados / persistentes
Los hallazgos de la iteración 1 eran sobre la versión con QR. CC-014 reescribió el WP y su historial dejó de aplicar, así que no hay hallazgos previos que evaluar.
