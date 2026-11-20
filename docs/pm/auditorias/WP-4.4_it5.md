# Auditoría WP-4.4 — iteración 5
Dictamen: CONFORME CON OBSERVACIONES
Commit: b78956a7c6bba10fdc70c32824564ca6dd8fa08c
Evidencia: docs/pm/evidencia/WP-4.4_it5_aceptacion_b78956a.log
Archivos auditados: pi/lidar.py, pi/rplidar.py, requirements.txt, pi/qr.py, pi/camara.py
Tipo: reverificación

## Verificación por criterio

**Sobre la evidencia.** El log corresponde a HEAD (`Commit: b78956a…`, línea 2). Su resultado es `49 failed, 142 passed` (línea 962), y ningún FAILED es de `test_wp_4_4.py`: los 49 (líneas 913-961) son de `test_wp_4_1.py`, `test_wp_4_2.py` y `test_wp_4_3.py`.

El log y el .json dicen "Árbol limpio: no". Lo revisó con `git status`: lo único sucio es `docs/pm/estado.md` (generado) y dos archivos vacíos sin seguimiento, `Tarima` y `docs/pm/Tarima` (0 bytes). Ninguno afecta a las pruebas. Repitió la prueba con `python -m pytest tests/aceptacion/test_wp_4_4.py -v` (`.venv`): **49 passed in 0.15s**.

| Criterio | Resultado | Evidencia |
| --- | --- | --- |
| CA-4.4.1 | Cumple | La prueba pasa. `localizar_poste` (`pi/lidar.py:65-79`) y `_agrupar` (`:34-53`) no cambiaron respecto de a32dce2. |
| CA-4.4.2 | Cumple | Pasan las 3 pruebas. Código de poste intacto. |
| CA-4.4.3 | Cumple | Pasan las 2 (cara plana de 18 y 40 cm). |
| CA-4.4.4 | Cumple | Pasan las 3. |
| CA-4.4.5 | Cumple | Pasan las 4. |
| CA-4.4.6 | Cumple | Pasan las 3. `pi/rplidar.py` no cambió. |
| CA-4.4.7 | Cumple | Pasan las 2. `pi/qr.py` y `pi/camara.py` no existen; `requirements.txt` no cambió. |
| CA-4.4.8 | No aplica | Pasó a WP-6.2 como CA-6.2.4 (CC-015). |
| CA-4.4.9 | Cumple | Pasa `test_ca_4_4_9_…`: distancia 100 ± 3, rumbo 20 ± 2, ancho 18 ± 2 y lado FRENTE. Distancia y rumbo salen del punto medio entre esquinas (intersección de rectas ajustadas, `:193-196`); `ancho_cm` es la distancia entre esquinas (`:172`). |
| CA-4.4.10 | Cumple | Pasa `…_de_lado_a_100_cm_y_menos_30_grados`. Cara ≈ 40 cm da LADO por `cara >= ancho_lado_cm` (`:194`, SUP-041). |
| CA-4.4.11 | Cumple | Pasan los 9 casos de `None` (vacío, pared, poste, recta de 18, recta de 40, una sola ala con cara de 18 y de 40, "V" de dos tramos, torso curvo) y la escena con tarima y poste juntos. "Exactamente tres tramos" en `:162`. |
| CA-4.4.12 | Cumple | Pasan las 5 pruebas. Filtro de rango en `_agrupar` (`:42`); el más cercano sale de `min(...)` (`:218`). |
| CA-4.4.13 | Cumple | Pasan los 7 casos de `None` (alas a 20° y 70°, de 8 y 35 cm, abiertas alejándose, ala curva de 5 cm, asimetría 35°/55°) y la aceptación con 40°/50° y ruido ±0.5 cm (FRENTE y LADO). Tolerancias `:180-183`; simetría `:184`; sentido de apertura `:186-192`; ala curva `:161-166`. |
| CA-4.4.14 | Cumple | Pasan las 4. `zona_trasera` (`:44-46`) y la firma de `localizar_poste` (`:65-66`) idénticos a a32dce2. |

**Firmas frente a la interfaz (WBS v1.22):** `localizar_tarima(...)` (`pi/lidar.py:199-201`) coincide en nombres, orden y valores por defecto. `localizar_poste` y `Tarima` no cambiaron.

**CC-022:** `_vertices` (`:112-125`) aplica Douglas-Peucker con tolerancia `desviacion_max_cm` (`:82-101`) y después quita uno a uno los vértices cuya eliminación deja todos los puntos del tramo fusionado a ≤ `desviacion_max_cm` (`_desviacion_tramo`, `:104-109`), empezando por el de menor desviación.

## Cambios reverificados
- **`51c4742` [WP-4.4] it5 (CC-021, CC-022).** Toca solo `pi/lidar.py` (+130/−22): quita `_desviacion_max`, reescribe `localizar_tarima` y añade `_douglas_peucker`, `_desviacion_tramo`, `_vertices`, `_recta`, `_interseccion`, `_angulo_entre` y `_evaluar_tarima`. `localizar_poste`, `_agrupar`, `_cuerda`, `_centro`, `Poste` y `Tarima` no cambian.
- **`8d93d53` [pm] CC-021 (línea base).** Reescribe CA-4.4.9 a 4.4.13 y las pruebas de tarima; no se quitó ni relajó ninguna aserción de los criterios no reabiertos.
- **`576bfe6` [pm] CC-022 (línea base).** Solo aclara la interfaz (WBS 1.22).
- **`94b3a11`, `e592e44`, `4257b2f`, `b78956a`.** Solo `docs/pm/`.

## Hallazgos
No hay hallazgos nuevos. Notas que no constituyen hallazgo:
- `min_puntos_tramo` cuenta los puntos de cada tramo incluyendo los vértices compartidos (`:164-165`); la interfaz no lo precisa y la lectura del ejecutor es razonable.
- `localizar_tarima` sigue sin aplicar `zona_trasera` (`:212`); ya era así en a32dce2.

## Alcance, integridad y regresión
- **Alcance:** `51c4742` toca solo `pi/lidar.py`, que está en el alcance.
- **Integridad:** nada en `docs/pm/` cambió dentro de `51c4742`; el bloqueo de la it5 quedó resuelto por CC-022.
- **Credenciales:** ninguna en `pi/lidar.py`.
- **Regresión:** it4 49 failed / 129 passed; ahora 49 failed / 142 passed (las 13 de más son las nuevas de tarima). Los 49 fallos son de WP-4.1, 4.2 y 4.3, pendientes; no hay fallos nuevos.
- **Otros WP:** WP-4.3 usa `localizar_poste`, que no cambió.
- **Higiene:** los archivos vacíos `Tarima` y `docs/pm/Tarima` parecen restos de una redirección de shell; conviene borrarlos.

## Hallazgos de iteraciones previas
- **H-1 [Observación] Resolución real del A1 frente a los umbrales de agrupación y `min_puntos`. Persiste**, y con CC-021 pesa más: con la separación de ≈ 2.6° de SUP-042, un ala a 45° y ~100 cm deja puntos separados ~6 cm, por encima de `SEPARACION_GRUPO_CM` (5 cm); las alas podrían quedar fuera del grupo de la cara. Las pruebas sintéticas, a 1°, no lo ejercen. Se valida en WP-6.2 (SUP-036, SUP-043).
- **H-2 [Observación]** `escanear` puede devolver una vuelta parcial y deja vivo el hilo lector tras un timeout. Persiste.
- **H-3 [Observación]** Agrupación y rumbo en el corte de ±180°. Persiste.
- **H-4 [Observación]** Falta `KOLEO_LIDAR_PUERTO` en `.env.example`. Persiste.
