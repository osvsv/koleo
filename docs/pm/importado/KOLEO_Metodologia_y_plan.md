# KOLEO — Metodología y plan de trabajo

Nov 11, 2026 · @osvaldo

## Respuesta corta

Sí conviene definir tareas específicas, pero solo funcionan con tres condiciones. Sin ellas, en un proyecto con hardware las tareas se marcan "hechas" y luego nada funciona junto.

1. **Cada tarea termina en algo que se puede probar.** No "programar encoders", sino "el ESP32 imprime la distancia recorrida y el error contra una cinta métrica es menor a 2 cm en 1 m".
2. **Primero se fijan los contratos entre partes.** Los mensajes MQTT, los estados y el esquema SQL se escriben una vez y todos los respetan. Así cada quien avanza sin esperar al otro.
3. **Se integra cada semana, no al final.** Una sesión fija con el robot real cada semana. Los problemas de hardware aparecen al juntar piezas, y con tres semanas no hay margen para descubrirlos el último día.

La metodología que recomiendo es un **Kanban con ciclos de una semana**: un tablero con las tareas, una planeación corta el lunes, una sesión de integración a media semana y una demo el viernes. Es más ligera que Scrum y se adapta mejor a esperas físicas (piezas, soldadura, impresión 3D).

La entrega es el **2 de diciembre**, así que el plan tiene tres semanas, y cada semana cierra con pruebas VAL-01 a VAL-08 aprobadas, no solo con código escrito.

## Metodología

Un tablero, cuatro reuniones cortas por semana y una regla para decir "terminado". Nada más.

### Roles: un dueño por subsistema

Cada parte del robot tiene **una** persona responsable. Puede pedir ayuda, pero responde por ella. Propuesta basada en las responsabilidades actuales (ajústenla entre ustedes):

| Subsistema | Dueño propuesto | Qué entrega |
| --- | --- | --- |
| Mecánica: chasis, elevación, tracción | Álvaro | Robot ensamblado que levanta 10 kg |
| Electrónica y alimentación: cableado, 12 V, reguladores | Miranda | Robot energizado de forma segura, con diagrama real |
| Firmware ESP32: sensores, motores, seguridad | Leo | ESP32 que obedece el protocolo y nunca levanta con sobrepeso |
| Raspberry Pi: misión, A\*, QR, encoders, puente MQTT | Elías | Misiones completas de inicio a destino |
| Datos e interfaz: contratos MQTT, backend, SQLite, UI | Osvaldo | Cada movimiento queda en la BD y se ve en la UI |

Tu rol encaja bien con no tener experiencia en hardware: eres **dueño de los contratos** (el "idioma" entre partes) y de todo lo que pasa después de MQTT. No necesitas tocar cables para avanzar.

### Cadencia semanal

| Cuándo | Qué | Duración |
| --- | --- | --- |
| Lunes | Planeación: cada quien elige sus tareas de la semana y dice qué necesita de otros | 30 min |
| Diario (por chat) | Tres líneas: qué hice, qué sigue, qué me bloquea | 2 min |
| Miércoles o jueves | **Sesión de integración** con el robot físico, todos presentes | 2–3 h |
| Viernes | Demo de lo que funciona + 3 preguntas: qué salió bien, qué no, qué cambiamos | 20 min |

### El tablero

Columnas: **Por hacer → En curso → Bloqueado → En prueba → Hecho**. Máximo dos tareas "En curso" por persona: terminar una antes de abrir otra evita tener diez cosas al 80 %. Sirve GitHub Projects (vive junto al código), Trello o Notion; lo importante es que sea uno solo.

### Tamaño de una tarea

Una tarea cabe en **una sesión de trabajo (2 a 6 horas)**. Si no cabe, se divide. Cada tarea lleva cuatro datos:

- **Resultado verificable:** qué se puede ver o medir al terminar.
- **Cómo se prueba:** el paso exacto (comando, medición, video) que cualquiera del equipo puede repetir.
- **Depende de:** qué tarea u objeto físico necesita antes (pieza, otra tarea, el robot armado).
- **Dueño:** una sola persona.

Ejemplo bien escrito: *"Parada por obstáculo continua. Resultado: con el robot avanzando, una caja a 15 cm detiene los motores en menos de 200 ms y publica el evento OBSTACULO. Prueba: video + log MQTT. Depende de: HC-SR04 instalado. Dueño: Leo."*

### Definición de terminado

Una tarea pasa a **Hecho** solo si cumple las cuatro:

1. El código o el diseño está en el repositorio, en la rama principal.
2. Se probó en el nivel que indica la tarea: en banco, en el subsistema o en el robot completo (ver la sección de hardware).
3. Hay evidencia guardada: video, foto, log o captura, enlazada en la tarea. Esto mismo sirve para el reporte final.
4. Si cambió un mensaje, estado o tabla, el contrato se actualizó y el equipo lo sabe.

## Contratos primero (semana 1)

La primera tarea del proyecto es escribir los contratos, porque cierran cinco de las diez brechas de la documentación (1, 2, 6, 7 y 9). Van en una carpeta `contratos/` del repositorio, y nadie cambia un mensaje sin actualizarla.

### Temas MQTT (propuesta para validar con lo que ya corre)

| Tema | Quién publica | Contenido |
| --- | --- | --- |
| `koleo/robot1/telemetria` | Raspberry Pi, 2 veces por segundo | posición x/y en cm, velocidad, estado del robot, peso, distancia al obstáculo |
| `koleo/robot1/evento` | Raspberry Pi | LIFT\_OK, SOBREPESO, OBSTACULO, DROP\_OK, ERROR, con id de tarima y hora |
| `koleo/robot1/orden` | Backend o UI | INICIAR (ruta, tarima), CANCELAR, PARO, con un id de orden |
| `koleo/robot1/orden/ack` | Raspberry Pi | confirma o rechaza cada id de orden |
| `koleo/robot1/conexion` | Raspberry Pi (retenido, con testamento) | EN\_LINEA o FUERA\_DE\_LINEA |

Cada mensaje lleva `ts` (hora en milisegundos), con eso se mide la latencia de VAL-07 de extremo a extremo. El enlace UART entre Pi y ESP32 conserva sus comandos (`LIFT`, `MOVE`, `STOP`, `DROP`), pero se documenta la respuesta y el tiempo de espera de cada uno.

### Estados unificados

- **Robot:** INACTIVO, EN\_MISION, ELEVANDO, EN\_RUTA, DEPOSITANDO, DETENIDO\_OBSTACULO, ERROR.
- **Tarima:** EN\_PISO, EN\_TRANSITO, UBICADA\_DESTINO, BLOQUEADA\_SOBREPESO.

Estos reemplazan los nombres sueltos actuales (`EN_PISO` en el ESP32 frente a `UBICADA_DESTINO` en SQLite).

### Esquema SQL canónico

Una sola versión de `tarimas`, `historial_movimientos` y `registro_rechazos_seguridad`. Se toman los nombres del diagrama E-R (`ruta_ejecutada`, `peso_medido_kg`, `latencia_red_ms`) y se agrega `ubicacion_nodo` a `tarimas`, que hoy falta en el código.

## Cómo trabajar con hardware sin perder semanas

El software se puede reintentar gratis; el hardware no. Estas cinco reglas evitan los tropiezos más comunes en equipos sin experiencia.

1. **Un robot falso desde el día uno.** Un script de Python que publica la misma telemetría y eventos MQTT que el robot real, siguiendo las rutas del mapa. Con él, el backend, la BD y la UI avanzan aunque el robot esté desarmado, y después solo se cambia el origen de los datos. Lo puedes hacer tú.
2. **Probar en tres niveles, siempre en este orden.** *Banco*: un componente solo, sobre la mesa (el HX711 con pesas conocidas). *Subsistema*: varias piezas juntas (ESP32 + motores + encoders, con las ruedas al aire). *Robot completo*: en el piso, en el mapa. Saltar al robot completo hace imposible saber qué falló.
3. **Un cambio a la vez en el robot.** Si se cambian cables y firmware el mismo día y algo falla, no se sabe cuál fue. En la sesión de integración se prueba una cosa nueva, se anota el resultado y se pasa a la siguiente.
4. **Lista antes de energizar.** Antes de conectar la batería: tierra común revisada, divisor 5 V → 3.3 V en ECHO, polaridad de 12 V, fusible puesto. Un ESP32 quemado cuesta días de envío.
5. **Bitácora del robot.** Un documento compartido con fecha, qué se cambió, qué se probó y qué pasó. Es la evidencia para VAL-01 a VAL-08 y para el reporte final.

Lo más riesgoso va primero: el ensamble mecánico y la elevación bloquean seis de las ocho pruebas (VAL-01 y VAL-03 a VAL-07). Si una meta no se alcanza a tiempo, por ejemplo el error menor a 10 cm, se demuestra con lo logrado y se reporta la medición real; eso vale más que una demo que falla.

## Calendario de tres semanas

&#91;embedded content: plan de 3 semanas · 2 puertas y la entrega\]

No se pasa a la siguiente semana sin cruzar su puerta: si la Puerta 1 no se cumple el 17 de noviembre, el lunes 18 se replanea recortando alcance, no se acumula atraso.

## Primer desglose de tareas

Son 24 tareas, cada una con un resultado medible, y salen de las brechas (sección 16) y del plan de integración (sección 17) de la documentación. Los dueños son una propuesta; cópienlas al tablero y ajústenlas el lunes.

### Semana 1 (11 al 17 de noviembre): contratos, ensamble y esqueleto

| ID | Tarea y resultado esperado | Dueño | Depende de | Cómo se prueba |
| --- | --- | --- | --- | --- |
| T01 | Contratos MQTT, estados y esquema SQL escritos y aceptados por el equipo | Osvaldo | — | Revisión en la reunión del lunes |
| T02 | Inventario de lo que ya corre: broker, quién publica qué tema hoy | Elías, Osvaldo | — | Captura de `mosquitto_sub -t 'koleo/#'` |
| T03 | Robot falso en Python publica telemetría y eventos de RUTA\_1 | Osvaldo | T01 | Los mensajes aparecen con el formato del contrato |
| T04 | Backend guarda eventos MQTT en SQLite con el esquema canónico | Osvaldo | T01 | VAL-08 con el robot falso: 2 traslados y 1 rechazo |
| T05 | Chasis y tracción ensamblados | Álvaro | Piezas | Soporta 10 kg en estático; ruedas giran libres |
| T06 | Mecanismo de elevación montado con el actuador | Álvaro | T05 | Sube y baja sin carga con fuente de banco |
| T07 | Diagrama real de alimentación y lista antes de energizar | Miranda | — | Robot energizado sin carga; voltajes medidos anotados |
| T08 | HX711 calibrado; si falla la lectura, bloquea la elevación | Leo | — | Error menor a 0.2 kg con pesas conocidas; desconectado no levanta |
| T09 | UART Pi–ESP32 en banco con respuesta y tiempo de espera por comando | Elías, Leo | T01 | Los 4 comandos responden; sin respuesta en 1 s se marca error |

### Semana 2 (18 al 24 de noviembre): robot real en el esqueleto y seguridad

| ID | Tarea y resultado esperado | Dueño | Depende de | Cómo se prueba |
| --- | --- | --- | --- | --- |
| T10 | Sensores montados: celda de carga, HC-SR04, ToF, encoders | Miranda | T05, T07 | Cada sensor reporta lecturas en el robot armado |
| T11 | Elevación de 10 kg | Álvaro, Leo | T06, T08 | **VAL-01**: menos de 15 s, cronometrado en video |
| T12 | Rechazo por sobrepeso de punta a punta | Leo, Osvaldo | T04, T08 | **VAL-02**: 11.8 kg no sube; evento y fila en la BD |
| T13 | Parada continua por obstáculo | Leo | T10 | **VAL-05**: caja a 15 cm detiene motores; evento publicado |
| T14 | Avance por distancia con encoders | Elías | T10 | Una celda (30 cm) con error menor a 3 cm, 5 repeticiones |
| T15 | La Pi publica telemetría real y sustituye al robot falso | Elías, Osvaldo | T03, T09 | La UI muestra el robot real moviendo una celda |
| T16 | Medición de latencia del depósito a la BD | Osvaldo | T12, T15 | **VAL-07**: menos de 2 s, con `ts` de ambos lados |
| T17 | UI: Flotilla y Monitoreo conectadas por MQTT | Osvaldo | T03 | Funciona con el robot falso y con el real |

### Semana 3 (25 de noviembre al 1 de diciembre): navegación, interfaz y validación

| ID | Tarea y resultado esperado | Dueño | Depende de | Cómo se prueba |
| --- | --- | --- | --- | --- |
| T18 | Tres rutas completas en el piso del mapa | Elías | T14, T15 | **VAL-03**: RUTA\_1, 2 y 3 sin colisión, en video |
| T19 | Error de llegada al destino | Elías, Álvaro | T18 | **VAL-04**: menor a 10 cm, medido con cinta |
| T20 | Traslado sostenido | Todos | T11, T18 | **VAL-06**: 3 min sin reinicio ni corte de energía |
| T21 | UI: Control (iniciar, cancelar, paro) y Gestión logística | Osvaldo | T15, T17 | Una orden desde la UI mueve el robot y queda registrada |
| T22 | Lectura QR con Picamera2 en el robot | Elías | T15 | Lee TAR-101 en menos de 2.5 s, 5 de 5 intentos |
| T23 | Ensayo general de la demo y video de respaldo | Todos | T18–T21 | Demo completa grabada el 30 de noviembre |
| T24 | Reporte con evidencia de VAL-01 a VAL-08 | Todos, coordina Osvaldo | T23 | Cada prueba con su resultado medido y evidencia |

**Fuera del plan, salvo que sobre tiempo:** integrar el RPLIDAR al mapa y Google Coral. Ninguna prueba VAL los requiere, y con tres semanas conviene recortarlos ya. También nota que te tocan 8 tareas de software: si te saturas, T03 y T16 son las más fáciles de pasar a alguien.

## Preguntas para ajustar el plan

- [ ] ¿Cómo está hoy el robot físico: armado, a medias o solo en CAD? Esto mueve T05, T06 y T10.
- [ ] ¿Quién publica MQTT ahora, el ESP32 directo o la Raspberry Pi? ¿Dónde corre el broker?
- [ ] ¿La entrega final sigue siendo el 2 de diciembre? ¿Hay revisiones parciales antes?
- [ ] ¿Cuántas horas por semana puede dar cada quien, y qué día pueden reunirse todos con el robot?
- [ ] ¿Usan ya alguna herramienta de tareas, o arrancamos con GitHub Projects? ¿Cuál es el repositorio?
