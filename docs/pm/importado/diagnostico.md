# Diagnóstico de la planeación importada — KOLEO

Fecha: 2026-11-11. Todo lo importado nace **[S]** hasta que se valide en G1.

## Documentos analizados

| Clave | Archivo | Qué es | Fecha / origen |
| --- | --- | --- | --- |
| DG | `KOLEO_Documentacion_General.md` (980 l.) | Especificación técnica del proyecto, derivada de la presentación del 21-oct. Separa "propuesto / reportado / pendiente". | Estado al 21-oct |
| TODO | `KOLEO_todo.md` (1723 l.) | Recopilación completa: Charter/WBS, BOM final, pinout, armado, factibilidad, pendientes, anexos con código. | Actualizado al 11-nov |
| MP | `KOLEO_Metodologia_y_plan.md` (164 l.) | Propuesta de Kanban semanal, contratos MQTT/estados/SQL, 24 tareas T01–T24 y calendario de 3 semanas. | 11-nov; **propuesta de un modelo, no decisiones del equipo** |

**Código en el repositorio:** ninguno. Los fragmentos de firmware ESP32, script de la Pi (A*, QR) y demo SQLite
viven solo como anexos dentro de TODO/DG. Por eso no hay `reconocimiento.md` ni WP de caracterización
(ver sección "Entrega a la planeación").

## Diagnóstico por requisito del método

| Requisito | Pregunta | Resultado | Detalle |
| --- | --- | --- | --- |
| IDs estables | ¿WP y requisitos tienen IDs reutilizables? | **Adaptar** | Hay `OBJ-01..05` (DG, etiquetas añadidas), `VAL-01..08` (DG, reutilizables como base de criterios de aceptación), `T01..T24` (MP, candidatos a WP) y listas numeradas de brechas (DG 1–10) y pendientes (TODO 1–18). Ninguno es un WP con alcance de archivos ni interfaz. No hay IDs de requisitos funcionales. |
| Criterios verificables | ¿Cada criterio indica qué evidencia lo demuestra? | **Adaptar (parcial)** | VAL-01..08 y la columna "Cómo se prueba" de MP son buenos: medición + evidencia. Pero los umbrales **se contradicen entre documentos** (ver conflictos C1, C2). Varias metas no tienen evidencia (p. ej. "no colisión" sin definir método). |
| Trazabilidad | ¿Cada requisito llega a un WP y viceversa? | **Falta** | MP relaciona T01–T24 con VAL y con brechas de DG, pero no hay matriz. Requisitos del Reto IoT (≥2 sensores, ≥2 actuadores, Web API, ≥5 indicadores, etapa 2 por alumno) no tienen tarea ni VAL: T21 cubre UI pero ningún T cubre "≥5 indicadores" ni "Web API" explícitamente. |
| Procedencia | ¿Se distingue lo decidido de lo asumido? | **Falta** | DG sí separa "propuesto / reportado / pendiente" (útil), pero no hay [D]/[S]/[N]. MP mezcla propuestas del modelo (dueños, MQTT, estados) con hechos. TODO registra decisiones del equipo con fecha (11-nov: quitar paro, alarma, fusible, LM2596, microSD, regletas; celda 20 kg; VL53L1X; un actuador), que son las candidatas más sólidas a [D]. |
| Ejemplos | ¿Hay casos concretos para lo crítico? | **Adaptar** | Existen datos de demo: TAR-101 (8.45 kg, válida), TAR-102 (11.80 kg, rechazo), TAR-103 (6.20 kg, válida); mapa 5×6 con 3 rutas; ejemplo de tarea bien escrita (obstáculo a 15 cm < 200 ms). Faltan casos límite: peso = 10.0 kg exacto, báscula desconectada, pérdida de Wi-Fi/UART, QR sin lectura. |
| Modelo y cadencia | ¿El modelo implícito sigue siendo adecuado? | **Reutilizable con ajustes** | MP propone Kanban con ciclos semanales, integración a mitad de semana, demo viernes y puertas de salida. Es razonable para ~3 semanas con hardware. Pendiente: reconciliar con el cronograma de 7 semanas del Charter (C3) y con la cadencia de validación del método (incrementos con demo). |
| Proporcionalidad | ¿La documentación es proporcional o sobra? | **Sobra en parte** | ~2,900 líneas para un proyecto académico de 5 personas. TODO duplica contenido de DG (pinout, arquitectura, protocolo, SQL, pruebas) y contiene material no de planeación (guion de presentación, preguntas del profesor, errores visuales, cotizaciones). Para la línea base solo hace falta: alcance, requisitos, restricciones, riesgos, WBS y criterios. |

## Conflictos entre documentos (deben resolverse antes de G1)

| # | Tema | Fuente A | Fuente B | Observación |
| --- | --- | --- | --- | --- |
| C1 | Tiempo de elevación 10 kg | TODO (Charter/presentación): **< 10 s** | DG y MP (VAL-01): **< 15 s** | Factibilidad (TODO §17) estima ~5–6 s, cumple ambos. DG dice que OBJ-* son etiquetas añadidas y no oficiales. |
| C2 | Error de llegada | TODO (Charter): **< 5 cm** | DG y MP (VAL-04): **< 10 cm** | TODO §17: lazo abierto no cumple 5 cm. MP sugiere reportar la medición real si no se alcanza. ¿Cuál es la meta comprometida con el profesor? |
| C3 | Calendario | TODO: 7 semanas; H1 sem. 3 (prueba banco 10 kg), H2/H3 sem. 6, cierre sem. 7 | MP: 3 semanas hasta **entrega 2-dic**, puertas 17 y 24-nov | Las fechas de semana del Charter (sem. 1 ≈ inicio de oct.) y la "entrega 2-dic" no cuadran sin confirmar. MP lo lista como pregunta abierta. |
| C4 | Canal de datos | TODO/DG: ESP32 → HTTP POST → Web API (Flask) → SQLite | MP: Pi publica MQTT (5 temas) | El Reto IoT admite MQTT **o** HTTP [N]. DG: "no hay evidencia de qué corre hoy". MP pregunta quién publica y dónde corre el broker. |
| C5 | Interfaz | DG: React + Vite + Tailwind | TODO: Flask + HTML/CSS/JS | Además TODO: el equipo decidió **no** incluir diapositivas de interfaz, pero el Reto exige ≥5 indicadores en tiempo real. |
| C6 | Sensores / hardware | DG: VL53L5CX, "puentes H", HC-SR04 y RPLIDAR, Google Coral | TODO (11-nov): VL53L1X, L298N + BTS7960; candidato a quitar HC-SR04 **o** RPLIDAR; Coral y "agricultura" son inconsistencias | TODO es más reciente: DG está desactualizado en BOM. MP deja RPLIDAR y Coral **fuera** del plan; pero HC-SR04 es la base de VAL-05 (T13). |
| C7 | Seguridad eléctrica | TODO: sin fusible, paro ni alarma (decisión del equipo) | MP: checklist "fusible puesto" antes de energizar | Contradicción directa; además TODO exige prueba de cortos "obligatoria sin fusible". |
| C8 | Pinout | DG: IN3 en GPIO 12 | TODO: IN3 en GPIO 23 (GPIO 12 es strapping); encoder canal B en 36/39 | TODO resuelto; DG obsoleto. |
| C9 | Estados | DG: `EN_PISO`, `UBICADA_DESTINO`, `BLOQUEADA_SOBREPESO` sin enumeración | MP propone enumeración de robot y de tarima | Propuesta [S] de MP, sin aprobación. |
| C10 | Seguimiento de sensores del Reto | TODO: 6 sensores y 3 actuadores "confirmar con el profesor" | — | Pendiente de confirmar (TODO pendiente 13). |
| C11 | Roles | TODO: define cinco roles, sin asignar personas | MP: asigna dueños por nombre (Álvaro, Miranda, Leo, Elías, Osvaldo) | Asignación de MP es propuesta ("ajústenla entre ustedes"). Notar que MP atribuye "tu rol" a Osvaldo (autor) y contradice "reparto por rol" de TODO. |

## Decisiones que parecen firmes (candidatas a confirmar en G1)

Fuente en paréntesis. Todas siguen [S] hasta validación.

1. Objetivo del prototipo: robot ~300×300 mm que sube, transporta y deposita tarimas de **hasta 10 kg** (TODO §1, DG §3).
2. Entrega al curso Implementación de IoT, gpo 501, Tec Campus Guadalajara; equipo de 5 (TODO §2).
3. Presupuesto **$8,000 MXN ±25 %, tope $10,000** (Charter, TODO §4); sin piezas nuevas (TODO §4).
4. BOM final al 11-nov y piezas quitadas: paro, alarma LiPo, fusible, LM2596, microSD, regletas (TODO §6).
5. Un solo actuador lineal de 75 kg/50 mm con guías verticales; celda de 20 kg; VL53L1X; GA25-370 (TODO §7).
6. Arquitectura Pi 5 (QR, A*, UART) + ESP32 (control físico, sensores) (TODO §5, DG §4).
7. Mapa 5×6, celdas de 30 cm, tres rutas RUTA_1..3 con TAR-101..103 (DG §8).
8. Rechazo por sobrepeso con registro (`BLOQUEADA_SOBREPESO`) y esquema de 3 tablas (DG §10).
9. Latencia depósito → BD **< 2 s** y traslado sostenido de **3 min** (todos).
10. Requisitos del Reto IoT: ≥2 sensores, ≥2 actuadores, red MQTT/HTTP, BD + Web API, ≥5 indicadores en tiempo real (TODO §3) → **[N]** si se cita el enunciado del curso.
11. Lo que queda fuera por ahora: RPLIDAR en el mapa y Google Coral (MP; coincide con TODO "candidato a quitar").

## Supuestos del documento MP que no son decisiones del usuario

- Kanban semanal con 4 reuniones; "máx. 2 tareas en curso por persona".
- Definición de terminado de 4 puntos.
- Temas MQTT, estados unificados, esquema SQL canónico (con `ubicacion_nodo`).
- Asignación de dueños por subsistema.
- Robot falso en Python y pruebas en tres niveles (banco / subsistema / robot completo).
- Fechas de las puertas (17 y 24-nov) y entrega 2-dic: la entrega aparece como pregunta abierta en el propio MP.

## Riesgos ya identificados por los documentos

Armado mecánico aún sin chasis al 11-nov (bloquea VAL-01, 03–07); navegación en lazo abierto vs tolerancia de 5/10 cm;
báscula devuelve 0.0 si falla (elevación insegura); sin Web API ni dashboard; latencia medida solo en la escritura;
presupuesto sin margen para repuestos; sin fusible/paro; consumo USB de la Pi (1.6 A); picos de corriente reinician placas;
tiempo restante muy corto para integración.

## Entrega a la planeación

**Reutilizable:** VAL-01..08 como base de criterios; T01–T24 como borrador de WBS (reasignar IDs a WP-x.y y añadir alcance
de archivos/interfaz); datos y mapa de demo como ejemplos; BOM y decisiones de TODO como restricciones; brechas y pendientes como registro de riesgos.

**Falta:** IDs de requisitos y matriz de trazabilidad; procedencia; criterios de los requisitos del Reto (Web API, ≥5 indicadores);
casos límite; reconciliación de C1–C11.

**Alcance de adopción propuesto:** *solo trabajo nuevo*. No hay código versionado, por lo que no se prevén WP de
caracterización (`WP-0.x`). Los fragmentos de los anexos (firmware, A*, SQL demo) se tratan como **material de referencia [S]**,
no como código base; si el equipo quiere partir de ellos, un WP de extracción los llevaría al repositorio con sus pruebas.

**Preguntas que `/pm-planificar` debe cerrar primero:** C1, C2, C3 (fecha real de entrega y revisiones parciales), C4/C5 (stack de
datos e interfaz), C6/C7 (sensor de paro y política de seguridad eléctrica), estado físico real del robot, horas disponibles por persona,
herramienta de tareas y repositorio.
