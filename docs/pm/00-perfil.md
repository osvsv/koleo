# Perfil del proyecto — KOLEO
Versión: 1.0 (borrador para G0)

## Contexto (seis dimensiones)

1. **Naturaleza.** Prototipo académico de robot móvil con hardware y software (IoT): sube, transporta y deposita tarimas de hasta 10 kg y registra el movimiento en una base de datos. Curso Implementación de IoT, gpo 501, Tec de Monterrey GDL. Repositorio sin código aún; los fragmentos de firmware, A* y SQL de los anexos son material de referencia [S].
2. **Tamaño y complejidad.** 5 personas, 3 semanas (11-nov a 2-dic). Cinco subsistemas (mecánica, electrónica, firmware ESP32, Raspberry Pi, datos/UI) con muchas interfaces. Presupuesto $8,000 MXN (±25 %, tope $10,000), sin margen para repuestos.
3. **Certidumbre de requisitos.** Alta en metas (10 kg, <15 s, <10 cm, <2 s, 3 rutas, 3 min) y en el Reto IoT. Baja en la técnica: el robot es "un armado muy básico y aún nada ha funcionado bien"; navegación, mecánica de elevación y energía no están probadas.
4. **Criticidad.** Baja en impacto externo (prototipo de laboratorio) pero con riesgo físico real: batería LiPo 3S sin fusible ni paro, 12 V con picos de corriente, actuador de 75 kg. Un ESP32 o Pi quemados cuestan días.
5. **Partes interesadas.** Los 5 integrantes del equipo validan entre sí en una sesión semanal con el robot; el profesor evalúa la entrega del 2-dic (disponibilidad limitada, no participa en G0/G1).
6. **Restricciones.** Fecha fija 2-dic; presupuesto cerrado y BOM final al 11-nov; piso liso y escala 30×30 cm por celda; dependencia de piezas físicas y soldadura; sin hardware no se puede probar el ensamble.

## Nivel de rigor y justificación

**Estándar.** Semanas de duración, entregable evaluado, varias integraciones y cinco personas. Ligero no cubre la coordinación entre subsistemas; Riguroso no se justifica porque no hay datos personales, dinero ni normativa. Disparador para subir a Riguroso: ninguno previsto. Disparador para tratar un WP como riesgo alto: toca energía de 12 V/LiPo, la elevación con carga, el rechazo por sobrepeso o integra MQTT/Wi-Fi.

## Modelo de planeación y cadencia

- Modelo: **incremental con arranque en espiral por riesgo**. Primero lo más incierto y bloqueante (ensamble mecánico y energizado, báscula, UART), y en paralelo lo que no depende del hardware (contratos, robot simulado, persistencia).
- Cadencia: **tres incrementos semanales cerrados en viernes con demo** (20-nov, 27-nov y cierre 30-nov/1-dic) y entrega el 2-dic. Sesión de integración con el robot físico a mitad de semana.
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
| Demo Inc. 1 (vie 20-nov) | Equipo, en sesión con el robot | 20 | Presencial, con robot simulado y real |
| Demo Inc. 2 (vie 27-nov) | Equipo | 20 | Presencial con robot real |
| Cierre (30-nov a 1-dic) | Equipo; el profesor evalúa la entrega del 2-dic | 30 | Presencial y reporte final |

## Incrementos

IDs definitivos de `03-wbs.md` (la tabla del borrador aprobado en G0 usaba IDs provisionales; el cambio es solo de numeración y agrupación: el QR pasó a WP-4.4, los indicadores se fundieron en WP-5.1 y las pruebas VAL se separaron en WP-6.1 a 6.3).

| Incremento | WP que lo cierran | Demo |
| --- | --- | --- |
| Inc. 1 — contratos, ensamble y esqueleto (cierre vie 20-nov) | WP-1.1 contratos; WP-1.2 robot simulado; WP-1.3 backend (MQTT → SQLite → API); WP-2.1 chasis y tracción; WP-2.2 elevación; WP-2.3 energía y energizado seguro; WP-3.1 báscula con fallo seguro | Robot simulado completa 2 traslados y 1 rechazo en la BD (VAL-08); robot armado energizado levanta sin carga |
| Inc. 2 — robot real y seguridad (cierre vie 27-nov) | WP-2.4 sensores montados; WP-3.2 UART Pi–ESP32; WP-3.3 parada continua por obstáculo; WP-4.1 puente MQTT real; WP-4.2 avance por encoders; WP-5.1 tablero: flotilla, monitoreo e indicadores; WP-6.1 VAL-01, 02, 05 y 07 | Elevación de 10 kg, rechazo de 11.8 kg, paro por obstáculo y latencia, con evidencia |
| Inc. 3 — navegación, interfaz y validación (cierre 30-nov/1-dic) | WP-4.3 A* y misión; WP-4.4 QR; WP-5.2 tablero: control y logística; WP-6.2 VAL-03, 04 y 06; WP-6.3 ensayo y reporte | Tres rutas, error de llegada, 3 minutos y demo completa grabada |

## Decisiones del perfil

| ID | Decisión | Procedencia | Fuente |
| --- | --- | --- | --- |
| DP-01 | Nivel de rigor: Estándar | [S] | Propuesta de /pm-planificar; se confirma en G1 |
| DP-02 | Modelo incremental con arranque en espiral por riesgo, tres incrementos semanales con demo | [S] | Propuesta de /pm-planificar (basada en `KOLEO_Metodologia_y_plan.md`); se confirma en G1 |
| DP-03 | Entrega el 2-dic-2026, tres semanas desde hoy | [D] | Osvaldo, Fase 0 de /pm-planificar, 2026-11-11 |
| DP-04 | Metas comprometidas: elevar 10 kg en <15 s y error de llegada <10 cm | [D] | Osvaldo, Fase 0 de /pm-planificar, 2026-11-11 |
| DP-05 | Canal de datos: MQTT con broker, publicando la Raspberry Pi | [D] | Osvaldo, Fase 0 de /pm-planificar, 2026-11-11 |
| DP-06 | Tablero con React + Vite + Tailwind | [D] | Osvaldo, Fase 0 de /pm-planificar, 2026-11-11 |
| DP-07 | Validan los 5 del equipo, en sesión semanal con el robot | [D] | Osvaldo, Fase 0 de /pm-planificar, 2026-11-11 |
| DP-08 | No se segmenta el proyecto | [S] | Propuesta de /pm-planificar; se confirma en G1 |
| DP-09 | WP físicos los hacen personas, con evidencia en `evidencia/hw/` que audita el agente | [S] | Propuesta de /pm-planificar; se confirma en G1 |
| DP-10 | Seguridad eléctrica: reincorporar un fusible de 10 A en la línea de batería y mantener sin paro de emergencia físico (se usa desconectar el conector T y el STOP por software) | [S] | Propuesta de /pm-planificar; Osvaldo delegó la decisión el 2026-11-11 y desconoce la decisión del 11-nov del equipo (`KOLEO_todo.md` §6). Revertirla contradice al equipo: confirmar en G1 |
| DP-11 | Sensor de paro: HC-SR04 como base de VAL-05 (lo lee el ESP32 directo). RPLIDAR y Google Coral quedan fuera del alcance | [S] | Propuesta de /pm-planificar; Osvaldo marcó "aún no decidido" el 2026-11-11 |
| DP-12 | Entregar los incrementos con cierres el 20-nov, 27-nov y 30-nov/1-dic | [S] | Propuesta de /pm-planificar; el plan importado usaba "17 y 24-nov" con fechas de la semana que no coinciden con el calendario |
| DP-13 | Se acepta reportar la medición real si una meta no se alcanza (en vez de demostrar algo que falla) | [S] | `KOLEO_Metodologia_y_plan.md` (propuesta); confirmar en G1 |

## Riesgos y supuestos que el perfil deja abiertos hacia G1

- **Reto IoT: "microcontroladores en red".** Con DP-05 el ESP32 no se conecta por Wi-Fi: lo hace la Pi. Confirmar con el profesor que la Pi cuenta (SUP a registrar). Impacto alto, afecta WP-3.x, 4.1, 1.3.
- **Calendario.** `KOLEO_Metodologia_y_plan.md` supone lunes 18-nov; el 18-nov de 2026 es miércoles. Fechas del plan importado no se heredan sin revisión.
- **Estado físico del robot.** "Muy básico y nada ha funcionado bien": el Inc. 1 puede no cerrar mecánica. Regla de puerta: si no se cumple, se recorta alcance (p. ej. RPLIDAR, QR) y no se acumula atraso.
- **Fusible.** Es una pieza nueva fuera del BOM; costo mínimo pero contradice una decisión del equipo.
- **Python y entorno.** No hay archivos de requisitos aún; el WP-1.1 o 1.3 debe fijar versiones (pytest, Flask/FastAPI, paho-mqtt).

## Presupuesto de tamaño (Estándar, proporcional al caso)

Línea base total ≲ 12 WP de software y ≲ 10 WP físicos, sin sección sin consumidor en la matriz. Más allá, recortar.
