# Respuestas de validación G1 — KOLEO

Respondió Osvaldo el 2026-11-11 (en nombre del equipo). Los otros cuatro integrantes no respondieron el paquete; sus respuestas, si llegan, entran por `/pm-cambio`.

**Numeración.** Osvaldo usó la del paquete externo, que va ordenada por tema. Esta tabla la traduce a los IDs internos (`paquete.md`): 10→V-13, 11→V-10, 12→V-11, 13→V-12, 17→V-18, 18→V-17, 19→V-19 (escribió "V20"); 1 a 9, 14, 15 y 16 coinciden. Cada traducción se verificó por el contenido de la respuesta.

| Pregunta | Respuesta | Quién respondió | Fecha | Efecto |
| --- | --- | --- | --- | --- |
| V-01 (ext. 1) dueños por subsistema | "Aún no delegues roles, solo tareas. Probablemente todos terminemos trabajando en todo." | Osvaldo | 2026-11-11 | SUP-016 Corregido: se trabaja por tareas, sin dueños. Charter actualizado (DP-18). |
| V-02 (ext. 2) horas por semana | "Probablemente menos, considera un rango de 4-6 horas." | Osvaldo | 2026-11-11 | SUP-016 Corregido: capacidad 4 a 6 h por persona (≈ 60 a 90 h de equipo). RK-08 sube; se mantiene el alcance y se recorta por puerta (DP-17). |
| V-03 (ext. 3) hardware completo | "Sí" | Osvaldo | 2026-11-11 | SUP-008 Confirmado (solo la parte del hardware). La ejecución por personas pasa a SUP-019 (DP-09, sigue [S]). |
| V-04 (ext. 4) Python | "Sí" | Osvaldo | 2026-11-11 | SUP-007 Confirmado (solo el lenguaje). pytest pasa a SUP-020, sigue [S]. |
| V-05 (ext. 5) broker | "A" (en la Raspberry Pi) | Osvaldo | 2026-11-11 | SUP-024 Confirmado. Dónde corre el backend queda en SUP-006 [S]. |
| V-06 (ext. 6) Pi en red / Reto IoT | "El ESP32 y la Rasp no deberían estar conectadas por cable, se conectan ambas a la red." Aclaración: acepta la propuesta (ESP32 y Pi publican y reciben por MQTT; la Pi consolida hacia los temas del contrato) y pregunta por qué el USB. | Osvaldo | 2026-11-11 | SUP-001 Corregido y Confirmado: sin UART (DP-14). Se rehacen WP-1.1, 3.2, 3.3, 4.1. El USB queda solo como alimentación (SUP-025, [S]). |
| V-07 (ext. 7) sensor de paro | "A" (solo HC-SR04) | Osvaldo | 2026-11-11 | SUP-005 Confirmado; DP-11 pasa a [D]. |
| V-08 (ext. 8) fusible | "Aún no lo hemos decidido bien, déjalo pendiente y sugiérelo si crees que es indispensable." | Osvaldo | 2026-11-11 | SUP-004 sigue Pendiente; DP-10 sigue [S]. El modelo lo recomienda (ver más abajo). |
| V-09 (ext. 9) umbral de paro | "15 cm" | Osvaldo | 2026-11-11 | SUP-003 Confirmado (solo el umbral). El tiempo de respuesta < 200 ms pasa a SUP-022, [S]. |
| V-10 (ext. 11) mapa y tres rutas | "No es lo que van a evaluar pero mantenla como referencia; lo único que mostraremos es cómo se mueve y cómo carga el peso." | Osvaldo | 2026-11-11 | SUP-009 Corregido: mapa y rutas son referencia, no evaluación. REQ-F-006 baja a Media. REQ-NF-010 nuevo: la evaluación es esa demostración. |
| V-11 (ext. 12) 10.0 kg exactos | "Idealmente sí, aunque estamos pensando en bajar la carga a 100 gramos ya que no queremos dañar los motores." | Osvaldo | 2026-11-11 | SUP-010 Corregido junto con la aclaración posterior. REQ-NF-009 nuevo (DP-15). |
| V-12 (ext. 13) báscula en 0 kg | "Sí" | Osvaldo | 2026-11-11 | REQ-F-016 nuevo [D]: sin carga, no sube y avisa. El umbral de 0.03 kg es [S] (SUP-026). |
| V-13 (ext. 10) sensor sin lectura | "Sí" | Osvaldo | 2026-11-11 | REQ-F-004 [D]; CA-3.3.3 [D]. |
| V-14 (ext. 14) estado tras el depósito | "A" | Osvaldo | 2026-11-11 | SUP-023 Confirmado: UBICADA_DESTINO tras depositar, EN_PISO para tarimas registradas. |
| V-15 (ext. 15) inicio de la latencia | "A" (celda detecta que se soltó) | Osvaldo | 2026-11-11 | SUP-011 Confirmado. |
| V-16 (ext. 16) sin QR | "A" (no inicia) | Osvaldo | 2026-11-11 | SUP-014 Confirmado; REQ-F-007 [D]. |
| V-17 (ext. 18) metas oficiales | "A, aunque bajando significativamente el peso; por el momento déjalo en 100 g" | Osvaldo | 2026-11-11 | SUP-002 Confirmado. REQ-NF-001 y REQ-NF-002 [D], esta última con la carga de 100 g (DP-04, DP-15). |
| V-18 (ext. 17) duplicados | "No, debería notificar todas las entregas; si llegase a ser un duplicado por error deberíamos corregirlo." Aclaración: "Id único por entrega". | Osvaldo | 2026-11-11 | REQ-F-017 nuevo [D]: todas las entregas se registran; mismo `id_evento` repetido se descarta. REQ-F-008 deja de deduplicar por tarima. |
| V-19 (ext. 19, "V20") fechas | "No hay revisiones por parte del profesor, y de haberlas no hay una fecha, solo considera la entrega final, tentativamente el 2 de diciembre." | Osvaldo | 2026-11-11 | SUP-018 Corregido; DP-03 pasa a "tentativa"; DP-12 reemplazada: los cierres son internos y sin fecha. |
| Aclaración: límite de sobrepeso con 100 g | "Sigue en 10 kg" | Osvaldo | 2026-11-11 | DP-16 [D]. El rechazo se verifica con peso simulado (SUP-027, [S]); 11.8 kg no se carga físicamente. |
| Aclaración: alcance con 4 a 6 h | "Mantener y recortar por puerta" | Osvaldo | 2026-11-11 | DP-17 [D]: se conservan los 19 WP y se recorta en el camino. |

## Recomendación del modelo sobre V-08 (fusible) [S]

Lo considero indispensable antes de conectar la LiPo a los motores y al actuador. Una LiPo 3S 25C puede entregar decenas de amperes en un corto, y sin fusible ni paro físico el único límite es el cableado. Un fusible de 10 A en línea cuesta unos pocos pesos y se instala en minutos. El resto (sin paro físico) puede quedarse como lo decidió el equipo. La decisión sigue pendiente y no bloquea la línea base: REQ-NF-005 conserva el fusible como [S].

Revisión externa: no — sin cambios (no se hizo la revisión en claude.ai antes de responder).
