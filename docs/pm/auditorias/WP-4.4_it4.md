# Auditoría WP-4.4 — iteración 4
Dictamen: CONFORME CON OBSERVACIONES
Commit: a32dce23e4cb5c7a64c9dd62de52f250aec38ca1
Evidencia: docs/pm/evidencia/WP-4.4_it4_aceptacion_a32dce2.log
Archivos auditados: pi/lidar.py, pi/rplidar.py, requirements.txt, pi/qr.py, pi/camara.py

## Verificación por criterio
Usé el log que me indicaron. Corresponde a HEAD: tiene `Commit: a32dce23e4cb5c7a64c9dd62de52f250aec38ca1` en la línea 2 y "Árbol limpio: sí" en la línea 4, y el .json dice lo mismo (`arbol_limpio: true`, comando `.venv\Scripts\python.exe -m pytest tests/aceptacion -q`). Resultado de la suite: `49 failed, 129 passed` (línea 962). Ninguno de los FAILED (líneas 913-961) es de `test_wp_4_4.py`: los 49 son de `test_wp_4_1.py` a `test_wp_4_3.py`. En la iteración 3 pasaban 122 pruebas y ahora pasan 129. La diferencia son las 7 pruebas nuevas de CC-020: 1 + 2 para CA-4.4.13 y 1 + 2 + 1 para CA-4.4.14.

| Criterio | Resultado | Evidencia (log, comando y salida, o archivo:línea) |
|---|---|---|
| CA-4.4.1 | Cumple | La prueba no está entre los FAILED del log. Con `zona_trasera=None`, `_agrupar` (`pi/lidar.py:34-53`) hace lo mismo que en la iteración 3. Con el valor por defecto solo quita los puntos con ángulo absoluto ≥ 150° y d ≤ 40 cm, y un poste a 100 cm y 20° no cae ahí. |
| CA-4.4.2 | Cumple | Pasan las 3 pruebas. La regla de descarte está en `pi/lidar.py:83` y no cambió. |
| CA-4.4.3 | Cumple | Pasan. Ver `pi/lidar.py:83`. |
| CA-4.4.4 | Cumple | Pasan. El poste más cercano sale de `pi/lidar.py:89`. |
| CA-4.4.5 | Cumple | Pasan las 4 pruebas. El filtro de rango está en `pi/lidar.py:42` y no cambió. |
| CA-4.4.6 | Cumple | Pasan las 3 pruebas. `pi/rplidar.py` no cambió (`git show --stat a697903` solo toca `pi/lidar.py`). |
| CA-4.4.7 | Cumple | Pasan las 2 pruebas de inspección. Los archivos no cambiaron. |
| CA-4.4.8 | No aplica | Pasó a WP-6.2 como CA-6.2.4 (CC-015). |
| CA-4.4.9 | Cumple | Pasa. Una cara plana sin ruido tiene desviación ≈ 0, menor que 1.5 (`pi/lidar.py:103`). |
| CA-4.4.10 | Cumple | Pasa. |
| CA-4.4.11 | Cumple | Pasan las 4 pruebas. En la escena con tarima y poste, el poste sigue saliendo con la `zona_trasera` por defecto. |
| CA-4.4.12 | Cumple | Pasan las 5 pruebas. |
| CA-4.4.13 | Cumple | Pasan `test_ca_4_4_13_objeto_curvo_..._no_es_tarima` y `test_ca_4_4_13_cara_plana_con_ruido_...[18-FRENTE/40-LADO]`. `_desviacion_max` (`pi/lidar.py:60-67`) calcula bien la distancia de cada punto a la recta entre los extremos y devuelve 0 si L = 0. El descarte con `> desviacion_max_cm` está en `pi/lidar.py:103`. La prueba sí discrimina: el arco de 40 cm a 100 cm tiene una cuerda de ≈ 40 cm, más de 4 puntos y una separación de ≈ 1.7 cm entre puntos, así que sin el filtro de desviación saldría como tarima "LADO". Con una flecha de 5 cm queda muy por encima de 1.5. Con ruido de ±0.5 cm, la desviación no pasa de ≈ 1 cm. |
| CA-4.4.14 | Cumple | Pasan `..._punto_del_actuador_a_25_cm_y_175_grados_no_es_poste`, `..._poste_al_frente_o_a_100_cm_se_sigue_encontrando[25-0/100-20]` (con el actuador en la escena) y `..._con_zona_trasera_none_el_punto_trasero_si_se_reporta`. El filtro de `pi/lidar.py:44-46` se aplica antes de agrupar, como pide la interfaz, y sus límites son inclusivos (≥ 150°, ≤ 40 cm), como dice SUP-042. `_normalizar` deja 180° en −180°, que `abs()` convierte en 180°. Nota: el criterio habla de "un punto", pero la prueba (commit de línea base 88098ff, no del ejecutor) usa dos puntos a 174° y 176°. Con `min_puntos=2`, un punto suelto nunca daría un poste, ni siquiera con `None`. Me parece una interpretación razonable y no la registro como hallazgo. |

**Firmas frente a la interfaz:**
- `localizar_poste(escaneo, ancho_max_cm=12, min_puntos=2, alcance_max_cm=200, distancia_min_cm=15, zona_trasera=(150, 40))` (`pi/lidar.py:75-76`) coincide.
- `localizar_tarima(..., ancho_min_cm=12, ancho_max_cm=50, ancho_lado_cm=29, min_puntos=4, alcance_max_cm=200, distancia_min_cm=15, desviacion_max_cm=1.5)` (`pi/lidar.py:92-93`) coincide.
- Los parámetros nuevos van al final, así que los llamadores posicionales anteriores siguen funcionando.

**`localizar_poste` sin el punto trasero:** el diff `ce9f4a6..HEAD -- pi/lidar.py` solo añade el bloque condicional `if zona_trasera is not None` en `_agrupar` y pasa el argumento. Con `None`, el camino es idéntico al de la iteración 3. La regla de descarte, `_centro` y la selección del más cercano no cambiaron.

**Requisitos y supuestos:**
- REQ-F-006: la detección se amplía según CC-020.
- REQ-F-007: sin cambio, porque solo se detecta y no se envían órdenes.
- SUP-037: se conserva el ancho máximo de 12 cm.
- SUP-041: el umbral de 29 cm sigue en `pi/lidar.py:106`.
- SUP-042: los valores 150°, 40 cm y 1.5 cm están en el código, tal cual.

## Predicciones frente a lo observado
No aplica: el WP es de riesgo medio.

## Hallazgos
No hay hallazgos nuevos. Esta es la iteración 4 y rige la regla de hallazgos congelados: solo cuentan los Mayores nuevos, y no encontré ninguno.

## Alcance, integridad y regresión
- **Alcance:** el commit de trabajo `a697903` toca solo `pi/lidar.py` (+32/−7), que está en el Alcance de archivos.
  - `a32dce2` es el commit del método y solo añade `docs/pm/auditorias/WP-4.4_it4_ejecucion.md`.
  - Los cambios de `tests/aceptacion/test_wp_4_4.py`, `docs/pm/03-wbs.md` y `docs/pm/supuestos.md` llegan en los commits de línea base de CC-020 (`88098ff`, `744d0a4`), no en el commit del WP.
  - `scripts/lidar_*.py` y `scripts/ver_lidar.sh` vienen de `5ef51cb` ("[pm] herramientas: visor del LIDAR"), fuera del commit del WP.
- **Integridad:** nada en `docs/pm/` cambió en `a697903`.
- **Credenciales:** no hay ninguna en `pi/lidar.py` ni en los scripts nuevos. `ver_lidar.sh` usa un alias `ssh koleo-pi` sin secretos.
- **Regresión:** los 49 fallos son los mismos que en la iteración 3 (WP-4.1, 4.2 y 4.3, todos pendientes) y no hay fallos nuevos.
- **Otros WP:** hoy ningún código fuera de `pi/lidar.py` y `scripts/` llama a `localizar_poste` (WP-4.3 no está implementado). El cambio del valor por defecto solo afecta a puntos traseros a ≤ 40 cm, como manda CC-020.

## Hallazgos de iteraciones previas: cerrados / persistentes
Las cuatro observaciones de la iteración 2 siguen abiertas, sin cambios, y ninguna bloquea. CC-020 no trató ninguna:
- H-1 [Observación] Resolución real del A1 frente a los umbrales de agrupación y `min_puntos`. **Persiste.** El umbral de 1.5 cm de desviación también queda por calibrar en WP-6.2 (SUP-042).
- H-2 [Observación] `escanear` puede devolver una vuelta parcial y deja vivo el hilo lector cuando hay timeout. **Persiste** (`pi/rplidar.py` sin cambios).
- H-3 [Observación] Agrupación y rumbo en el corte de ±180°. **Persiste.** La `zona_trasera` cae justo en ese corte: el actuador a 175–177° se descarta antes de agrupar, así que no le afecta, pero un objeto trasero a más de 40 cm sigue expuesto al problema.
- H-4 [Observación] Falta `KOLEO_LIDAR_PUERTO` en `.env.example`. **Persiste.**
