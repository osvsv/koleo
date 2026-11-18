# Auditoría WP-4.4 — iteración 3
Dictamen: CONFORME CON OBSERVACIONES
Commit: ce9f4a613d047394d753bc9177654254461e6c5d
Evidencia: docs/pm/evidencia/WP-4.4_it3_aceptacion_ce9f4a6.log
Archivos auditados: pi/lidar.py, pi/rplidar.py, requirements.txt, pi/qr.py, pi/camara.py

## Verificación por criterio
Usé el log indicado. Corresponde a HEAD (`Commit: ce9f4a613d047394d753bc9177654254461e6c5d`, "Árbol limpio: sí"). Resultado de la suite: `49 failed, 122 passed` (línea 962). En la lista de FAILED (líneas 913-961) no hay ninguna prueba de `test_wp_4_4.py`. Pasan las 29 pruebas de WP-4.4: las 18 de la iteración 2 y las 11 que añadió CC-019 (cc61c71). En la iteración 2 pasaban 111 pruebas; ahora pasan 122, que son esas mismas 111 más las 11 nuevas. El hook no me dejó ejecutar pytest por separado, así que me baso en el log, que es del commit auditado.

| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
|---|---|---|
| CA-4.4.1 | Cumple | La prueba no está entre los FAILED del log. En `pi/lidar.py:59-69`, `localizar_poste` se reorganizó con funciones auxiliares (`_agrupar`, `_cuerda`, `_centro`) y hace lo mismo que antes: filtra por rango, agrupa con separación < 5 cm, descarta con `len < min_puntos or cuerda > ancho_max_cm` y promedia. |
| CA-4.4.2 | Cumple | Las 3 pruebas pasan (pared, vacío, puntos sueltos). Ver `pi/lidar.py:63`. |
| CA-4.4.3 | Cumple | Pasan los casos de tarima de 18 y 40 cm, que no se reportan como poste. Ver `pi/lidar.py:63`. |
| CA-4.4.4 | Cumple | Pasan las 3 pruebas. Devuelve el más cercano con `min(..., key=distancia_cm)` en `pi/lidar.py:69`. |
| CA-4.4.5 | Cumple | Pasan las 4 pruebas. El filtro de rango está en `_agrupar`, `pi/lidar.py:39`. |
| CA-4.4.6 | Cumple | Pasan las 3 pruebas. `pi/rplidar.py` no cambió en esta iteración (`git show --stat 8c1d4bc` solo toca `pi/lidar.py`). |
| CA-4.4.7 | Cumple | Pasan las 2 pruebas de inspección. `pi/qr.py`, `pi/camara.py` y `requirements.txt` no cambiaron desde la iteración 2. |
| CA-4.4.8 | No aplica | Pasó a WP-6.2 como CA-6.2.4 (CC-015). |
| CA-4.4.9 | Cumple | `test_ca_4_4_9_tarima_de_frente_a_100_cm_y_20_grados` pasa: `isinstance Tarima`, 100±3 cm, 20±2°, `lado == "FRENTE"`. `Tarima` tiene los 4 campos de la interfaz (`pi/lidar.py:17-22`). La regla es `"FRENTE" if cuerda < ancho_lado_cm` (`pi/lidar.py:81`), con el valor por defecto de 29 que fijan la interfaz y SUP-041. |
| CA-4.4.10 | Cumple | `test_ca_4_4_10_..._menos_30_grados` pasa: `lado == "LADO"`, 100±3 cm, −30±2°. Con una cuerda ≥ 29 el lado es LADO (`pi/lidar.py:81`). |
| CA-4.4.11 | Cumple | Pasan `test_ca_4_4_11_sin_tarima_devuelve_none[vacio/pared/poste]` y `..._tarima_y_poste_en_la_misma_escena_...`. Los grupos con cuerda `<= ancho_min_cm` o `> ancho_max_cm`, o con menos de `min_puntos`, se descartan en `pi/lidar.py:78`, como pide la interfaz. Con la tarima y el poste en la misma escena, cada función devuelve el suyo. |
| CA-4.4.12 | Cumple | Pasan las 5 pruebas: con dos tarimas devuelve la más cercana (`pi/lidar.py:85`), ignora un cuerpo a 10 cm y una tarima a 250 cm, y en ninguno de esos casos la tarima real queda tapada. Las firmas y los valores por defecto coinciden con la interfaz (`pi/lidar.py:72-73`: 12, 50, 29, 4, 200, 15). |

REQ-F-006 (EJ-035, EJ-036) y SUP-041 quedan reflejados literalmente en `pi/lidar.py:78-81`. SUP-037 (ancho máximo del poste 12 cm) se conserva en `localizar_poste`. REQ-F-007 no cambia: `localizar_tarima` solo detecta, no envía órdenes ni identifica.

## Predicciones frente a lo observado
No aplica: el WP es de riesgo medio.

## Hallazgos
No hay hallazgos nuevos. La iteración 3 se rige por la regla de hallazgos congelados: solo cuentan los Mayores nuevos, y no encontré ninguno.

## Alcance, integridad y regresión
- **Alcance:** `git show --stat 8c1d4bc` (commit de trabajo) toca solo `pi/lidar.py` (+42/−9), que está en el Alcance de archivos de WP-4.4. Ningún archivo de `docs/pm/` ni de `tests/aceptacion/` cambió en ese commit. `ce9f4a6` es el commit del método y solo añade `docs/pm/auditorias/WP-4.4_it3_ejecucion.md`.
- **Credenciales:** no hay credenciales ni valores fijos nuevos.
- **Regresión:** los 49 fallos son exactamente los de la iteración 2, de `test_wp_4_1.py`, `test_wp_4_2.py` y `test_wp_4_3.py` (WP pendientes), no regresiones.
- **Otros WP:** WP-4.3 consume `localizar_poste`, y su firma y comportamiento no cambian.

## Hallazgos de iteraciones previas: cerrados / persistentes
Las cuatro observaciones de la iteración 2 siguen abiertas. Ninguna bloquea:
- H-1 [Observación] Con la resolución real del A1 (≈2.6° entre puntos), los umbrales de agrupación de 5 cm y `min_puntos` quedan al límite. **Persiste.** Afecta también a `localizar_tarima`: con `min_puntos=4`, una cara de 18 cm subtiende ≈10° a 100 cm y ≈7° a 150 cm, es decir unos 3-4 y 2-3 puntos reales, y la cuerda medida entre extremos subestima el ancho. Hay que verificarlo en WP-6.2 junto con SUP-041.
- H-2 [Observación] `escanear` puede devolver una vuelta parcial y deja vivo el hilo lector cuando hay timeout. **Persiste** (`pi/rplidar.py` sin cambios).
- H-3 [Observación] Agrupación y rumbo en el corte de ±180°. **Persiste.** `_agrupar` y `_centro` ahora los comparten ambos detectores.
- H-4 [Observación] Falta `KOLEO_LIDAR_PUERTO` en `.env.example`. **Persiste** (requiere acción del usuario).
