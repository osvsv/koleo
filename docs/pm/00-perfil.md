# Perfil del proyecto — KOLEO
Versión: 1.1 (G1, respuestas de Osvaldo aplicadas)

## Contexto (seis dimensiones)

1. **Naturaleza.** Prototipo académico de robot móvil con hardware y software (IoT): sube, transporta y deposita tarimas de hasta 10 kg y registra el movimiento en una base de datos. Curso Implementación de IoT, gpo 501, Tec de Monterrey GDL. Repositorio sin código aún; los fragmentos de firmware, A* y SQL de los anexos son material de referencia [S].
2. **Tamaño y complejidad.** 5 personas, 3 semanas (11-nov a 2-dic, entrega tentativa), con 4 a 6 h por semana por persona (≈ 60 a 90 h de equipo en total). Cinco subsistemas (mecánica, electrónica, firmware ESP32, Raspberry Pi, datos/UI) con muchas interfaces. Presupuesto $8,000 MXN (±25 %, tope $10,000), sin margen para repuestos.
3. **Certidumbre de requisitos.** Alta en metas (100 g de demostración, <15 s, <10 cm, <2 s, 3 rutas de referencia, 3 min) y en el Reto IoT. Baja en la técnica: el robot es "un armado muy básico y aún nada ha funcionado bien"; navegación, mecánica de elevación y energía no están probadas.
4. **Criticidad.** Baja en impacto externo (prototipo de laboratorio) pero con riesgo físico real: batería LiPo 3S sin fusible ni paro, 12 V con picos de corriente, actuador de 75 kg. Un ESP32 o Pi quemados cuestan días.
5. **Partes interesadas.** Los 5 integrantes del equipo validan entre sí en una sesión semanal con el robot; el profesor evalúa solo la entrega final (tentativa 2-dic), sin revisiones parciales.
6. **Restricciones.** Fecha fija 2-dic; presupuesto cerrado y BOM final al 11-nov; piso liso y escala 30×30 cm por celda; dependencia de piezas físicas y soldadura; sin hardware no se puede probar el ensamble.

## Nivel de rigor y justificación

**Estándar.** Semanas de duración, entregable evaluado, varias integraciones y cinco personas. Ligero no cubre la coordinación entre subsistemas; Riguroso no se justifica porque no hay datos personales, dinero ni normativa. Disparador para subir a Riguroso: ninguno previsto. Disparador para tratar un WP como riesgo alto: toca energía de 12 V/LiPo, la elevación con carga, el rechazo por sobrepeso o integra MQTT/Wi-Fi.

## Modelo de planeación y cadencia

- Modelo: **incremental con arranque en espiral por riesgo**. Primero lo más incierto y bloqueante (ensamble mecánico y energizado, elevación con peso declarado, enlace de comandos por red), y en paralelo lo que no depende del hardware (contratos, robot simulado, persistencia).
- Cadencia: **tres incrementos con demo interna del equipo, sin fecha comprometida** (el profesor no hace revisiones parciales, DP-12); la entrega final es tentativamente el 2-dic. Sesión de integración con el robot físico a mitad de semana, a convenir.
- Justificación: en Stacey la parte de software está en "complicado" (se puede planear) y la de hardware en "complejo" (se descubre al integrar), por lo que se necesita integrar cada semana. Quien valida está disponible semanalmente con el robot. El costo de cambio es alto en lo físico y bajo en software: los contratos (MQTT, estados, SQL) se fijan primero. Hay fecha fija, así que el recorte de alcance por puerta es preferible al atraso acumulado.

## Segmentación

**No se segmenta.** Hardware y software difieren en incertidumbre, pero son pocas semanas, el acoplamiento es alto (cada prueba VAL cruza varias partes) y la sobrecarga de dos líneas de base superaría el beneficio. La separación se hace por tipo de WP, no por segmento.

## Piezas activas del método

Las de Estándar: procedencia y registro de supuestos; tabla de decisiones del perfil; paquete de validación en G1 (interno, externo, revisión externa); ejemplos de aceptación para todos los requisitos funcionales; suite de aceptación del redactor para lo automatizable; demos en el primer incremento y al cierre (aquí en cada incremento por la sesión semanal); auditoría ciega en dos fases para riesgo medio y alto; regresión acumulativa; hooks, `pm_check` y estado derivado; reverificación sin ejecutor; métricas de calidad y costo. Sin auditor en sombra.

**Adaptación a hardware.** Los WP de ensamble, electrónica y pruebas físicas los hacen personas; su "ejecución" no la hace un agente. Su evidencia (foto, video, log, medición, bitácora) se guarda en `docs/pm/evidencia/hw/<WP>/` y el auditor la inspecciona. Los WP de software (contratos, simulador, backend, UI, A*, puente MQTT, firmware con simulación) se ejecutan con `/pm-ejecutar` y llevan pruebas de aceptación cuando son automatizables.

## Artefactos

| Artefacto | Decisión | Justificación |
| --- | --- | --- |
| Charter (`01-charter.md`) | Incluido | Siempre; reutiliza Charter original (10-oct) y metas confirmadas. |
| Requisitos de sistema (`02-requisitos.md`) | Incluido, ligero | Lista de requisitos de sistema y del Reto IoT con IDs REQ-F/NF; sin SRS completa de ISO 29148. |
| WBS y diccionario (`03-wbs.md`) | Incluido | WP derivados de T01–T24 y VAL-01..08. |
| Trazabilidad | Incluida dentro de WBS y requisitos | Evita un archivo sin consumidor. |
| Registro de riesgos (`05-riesgos.md`) | Incluido | Estándar; hay riesgos físicos y de calendario ya identificados. |
| `supuestos.md`, `gates.md`, `cambios.md`, `desviaciones.md`, `bloqueos.md`, `metricas.md` | Incluidos | Formato fijo del método. |
| `contratos/` (MQTT, estados, SQL) | Se produce como WP-1.1, **no** es documento de planeación | Es entregable del proyecto, consumido por backend, simulador, Pi y UI. |
| SRS extensa, documento de arquitectura aparte, plan de comunicaciones | Omitidos | Sin consumidor; TODO/DG ya cubren arquitectura. |
| Material de presentación, guion, preguntas del profesor, cotizaciones | Omitidos de la línea base | Siguen disponibles en `docs/pm/importado/`. |

## Matriz de consumo

| Documento o sección | Lo consume |
| --- | --- |
| `00-perfil.md`, decisiones del perfil | Gate G0, `pm_check`, `/pm-planificar` |
| `01-charter.md` (metas, alcance, cierre) | Gate G1, `/pm-validar`, auditor (alcance) |
| `02-requisitos.md` y ejemplos | Redactor de aceptación, auditor, G1 |
| `03-wbs.md` (alcance, interfaz, criterios) | `ejecutor-wbs`, `auditor-conformidad`, `gen_estado.py`, `pm_check` |
| `05-riesgos.md` | Auditor (riesgo del WP), sesión de lunes del equipo |
| `supuestos.md` | G1 (paquete de validación), `/pm-cambio` |
| `contratos/` (producido por WP-1.1) | Ejecutores de WP de software, redactor de aceptación |
| `evidencia/hw/**` | Auditor de WP físicos, demos, reporte final |

## Validación

| Punto | Quién valida | Presupuesto (min) | Canal |
| --- | --- | --- | --- |
| G0 (este perfil) | Osvaldo (con revisión externa opcional en claude.ai) | 15 | Claude Code + `revision-externa.md` |
| G1 (línea base) | Los 5 del equipo (Osvaldo coordina) | 40 total (≈ 10 por persona en el paquete externo) | Paquete externo en archivo compartible + Claude Code |
| Demo Inc. 1 (punto interno, sin fecha comprometida) | Equipo, en sesión con el robot | 20 | Presencial, con robot simulado y real |
| Demo Inc. 2 (punto interno) | Equipo | 20 | Presencial con robot real |
| Cierre (antes de la entrega final) | Equipo; el profesor evalúa la entrega final tentativa del 2-dic | 30 | Presencial y reporte final |

## Incrementos

IDs definitivos de `03-wbs.md` (la tabla del borrador aprobado en G0 usaba IDs provisionales; el cambio es solo de numeración y agrupación: el QR pasó a WP-4.4, los indicadores se fundieron en WP-5.1 y las pruebas VAL se separaron en WP-6.1 a 6.3).

| Incremento | WP que lo cierran | Demo |
| --- | --- | --- |
| Inc. 1 — contratos, ensamble y esqueleto (sin fecha comprometida) | WP-1.1 contratos; WP-1.2 robot simulado; WP-1.3 backend (MQTT → SQLite → API); WP-2.1 chasis y tracción; WP-2.2 elevación; WP-2.3 energía y energizado seguro; WP-3.1 elevación con peso declarado y rechazo por sobrepeso | Robot simulado completa 2 traslados y 1 rechazo en la BD (VAL-08); robot armado energizado levanta sin carga |
| Inc. 2 — robot real y seguridad (sin fecha comprometida) | WP-2.4 sensores montados; WP-3.2 enlace de comandos por MQTT; WP-3.3 parada continua por obstáculo; WP-4.1 puente MQTT real; WP-4.2 avance por encoders; WP-5.1 tablero: flotilla, monitoreo e indicadores; WP-6.1 VAL-01, 02, 05 y 07 | Elevación de la carga de demostración (100 g), rechazo con peso simulado de 11.8 kg, paro por obstáculo y latencia, con evidencia |
| Inc. 3 — navegación, interfaz y validación (antes de la entrega final) | WP-4.3 A* y misión; WP-4.4 QR; WP-5.2 tablero: control y logística; WP-6.2 VAL-03, 04 y 06; WP-6.3 ensayo y reporte | Tres rutas, error de llegada, 3 minutos y demo completa grabada |

## Decisiones del perfil

| ID | Decisión | Procedencia | Fuente |
| --- | --- | --- | --- |
| DP-01 | Nivel de rigor: Estándar | [S] | Propuesta de /pm-planificar; se confirma en G1 |
| DP-02 | Modelo incremental con arranque en espiral por riesgo, tres incrementos semanales con demo | [S] | Propuesta de /pm-planificar (basada en `KOLEO_Metodologia_y_plan.md`); se confirma en G1 |
| DP-03 | Entrega final tentativa el 2-dic-2026; el profesor no hace revisiones parciales ni fijó fechas intermedias | [D] | Osvaldo, Fase 0 de /pm-planificar y G1 V-19, 2026-11-11 |
| DP-04 | Metas oficiales: elevar la carga de demostración (100 g) en <15 s y error de llegada <10 cm | [D] | Osvaldo, Fase 0 de /pm-planificar y G1 V-17, 2026-11-11 |
| DP-05 | Canal de datos: MQTT con el broker en la Raspberry Pi; el ESP32 y la Pi publican por MQTT | [D] | Osvaldo, Fase 0 de /pm-planificar y G1 V-05, 2026-11-11 |
| DP-06 | Tablero con React + Vite + Tailwind | [D] | Osvaldo, Fase 0 de /pm-planificar, 2026-11-11 |
| DP-07 | Validan los 5 del equipo, en sesión semanal con el robot | [D] | Osvaldo, Fase 0 de /pm-planificar, 2026-11-11 |
| DP-08 | No se segmenta el proyecto | [S] | Propuesta de /pm-planificar; se confirma en G1 |
| DP-09 | WP físicos los hacen personas, con evidencia en `evidencia/hw/` que audita el agente | [S] | Propuesta de /pm-planificar; se confirma en G1 |
| DP-10 | Seguridad eléctrica: reincorporar un fusible de 10 A en la línea de batería y mantener sin paro de emergencia físico (se usa desconectar el conector T y el STOP por software) | [S] | Propuesta de /pm-planificar; Osvaldo delegó la decisión el 2026-11-11 y desconoce la decisión del 11-nov del equipo (`KOLEO_todo.md` §6). Revertirla contradice al equipo: confirmar en G1 |
| DP-11 | Sensor de paro: solo HC-SR04 (lo lee el ESP32 directo). RPLIDAR y Google Coral quedan fuera del alcance | [D] | Osvaldo, G1 V-07, 2026-11-11 |
| DP-12 | Los cierres de incremento son puntos internos sin fecha comprometida; solo la entrega final (tentativa 2-dic) tiene fecha | [D] | Osvaldo, G1 V-19, 2026-11-11 |
| DP-13 | Se acepta reportar la medición real si una meta no se alcanza (en vez de demostrar algo que falla) | [S] | `KOLEO_Metodologia_y_plan.md` (propuesta); confirmar en G1 |
| DP-14 | Sin cable de datos entre ESP32 y Pi: ambos se conectan a la red; el ESP32 publica sensores y eventos y recibe comandos por MQTT, y la Pi los consolida en los temas del contrato | [D] | Osvaldo, G1 V-06, 2026-11-11 |
| DP-15 | La carga física de demostración es de 100 g | [D] | Osvaldo, G1 V-11 y V-17, 2026-11-11 |
| DP-16 | El límite de sobrepeso sigue en 10 kg y el rechazo se verifica con el peso declarado de la tarima (sin celda de carga) | [D] | Osvaldo, G1 (aclaración tras V-11), 2026-11-11; Osvaldo, CC-004, 2026-11-13 |
| DP-17 | Se mantienen los 19 WP y se recorta por puerta lo que no alcance el tiempo | [D] | Osvaldo, G1 (aclaración tras V-02), 2026-11-11 |
| DP-18 | El trabajo se asigna por tareas, sin dueños por subsistema | [D] | Osvaldo, G1 V-01, 2026-11-11 |
| DP-19 | Capacidad del equipo: 4 a 6 h por semana por persona | [D] | Osvaldo, G1 V-02, 2026-11-11 |

## Riesgos y supuestos que el perfil deja abiertos hacia G1

- **Reto IoT: "microcontroladores en red".** Resuelto en G1 (V-06): el ESP32 se conecta él mismo a la red por MQTT.
- **Calendario.** `KOLEO_Metodologia_y_plan.md` supone lunes 18-nov; el 18-nov de 2026 es miércoles. Fechas del plan importado no se heredan sin revisión.
- **Estado físico del robot.** "Muy básico y nada ha funcionado bien": el Inc. 1 puede no cerrar mecánica. Regla de puerta: si no se cumple, se recorta alcance (p. ej. RPLIDAR, QR) y no se acumula atraso.
- **Fusible.** Es una pieza nueva fuera del BOM; costo mínimo pero contradice una decisión del equipo.
- **Python y entorno.** No hay archivos de requisitos aún; el WP-1.1 o 1.3 debe fijar versiones (pytest, Flask/FastAPI, paho-mqtt).

## Presupuesto de tamaño (Estándar, proporcional al caso)

Línea base total ≲ 12 WP de software y ≲ 10 WP físicos, sin sección sin consumidor en la matriz. Más allá, recortar.
