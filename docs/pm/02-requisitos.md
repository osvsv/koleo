# Requisitos — KOLEO
Versión: 1.2 (G1, respuestas de Osvaldo aplicadas; CC-004)

Requisitos de sistema. Procedencia: [D] decidido por Osvaldo (Fase 0 o G1, ver `validacion/G1/respuestas.md`), [N] Reto IoT del curso, [S] supuesto del modelo. Fuentes de lo importado: `importado/KOLEO_Documentacion_General.md` (DG), `importado/KOLEO_todo.md` (TODO), `importado/KOLEO_Metodologia_y_plan.md` (MP).

| ID | Requisito | Procedencia | Prioridad | Verificación |
| --- | --- | --- | --- | --- |
| REQ-F-001 | El robot eleva y sostiene una tarima dentro de su capacidad de diseño de 10.0 kg (límite inclusivo, SUP-010), evaluada con el peso declarado de la tarima (CC-004: sin celda de carga). La carga de demostración es de 100 g (REQ-NF-009). | [D] | Crítica | Evidencia física (VAL-01, con 100 g) |
| REQ-F-002 | Si el peso declarado de la tarima supera 10.0 kg, el robot no eleva, publica el evento SOBREPESO, la tarima queda BLOQUEADA_SOBREPESO y se registra una fila en `registro_rechazos_seguridad`. | [D] | Crítica | Prueba de aceptación (software) y evidencia con peso declarado de 11.8 kg (VAL-02) |
| REQ-F-003 | Si el comando `LIFT` llega sin peso declarado válido (ausente, no numérico o ≤ 0), el robot no eleva y responde error; "sin peso" nunca equivale a 0 kg ni autoriza la elevación. | [D] | Crítica | Inspección de código y evidencia física |
| REQ-F-004 | Con el robot en movimiento, un obstáculo a 15 cm o menos detiene la tracción de forma continua e independiente de la Raspberry Pi y publica el evento OBSTACULO. Si el sensor deja de dar lectura mientras el robot avanza, también se detiene. | [D] | Crítica | Evidencia física (VAL-05) |
| REQ-F-005 | Si el ESP32 no recibe comandos durante 1 s o pierde la red con la tracción activa, detiene la tracción; si la Pi no recibe respuesta a un comando en 1 s, lo reporta como error. | [S] | Alta | Prueba de aceptación (software) y evidencia física |
| REQ-F-006 | El robot planea con A* y ejecuta las rutas de referencia RUTA_1, RUTA_2 y RUTA_3 del mapa 5×6 (celdas de 30 cm) sin colisión. El mapa y las rutas son referencia, no criterio de evaluación. | [D] | Media | Prueba de aceptación (planificador) y evidencia física (VAL-03) |
| REQ-F-007 | La tarima se identifica por QR; si no hay lectura válida, la misión no inicia (no se usa un ID por defecto). | [D] | Media | Prueba de aceptación y evidencia física |
| REQ-F-008 | Al depositar, se actualiza la tarima (estado UBICADA_DESTINO y coordenadas) y se crea una fila en `historial_movimientos` con ruta, origen, destino, peso y latencia. | [S] | Crítica | Prueba de aceptación (VAL-08) |
| REQ-F-009 | Los mensajes MQTT (`telemetria`, `evento`, `orden`, `orden/ack`, `conexion`) y los del ESP32 (`esp32/cmd`, `resp`, `sensores`, `evento`, `conexion`) están definidos en un contrato validable, llevan `ts` en milisegundos, las órdenes y comandos llevan id con confirmación y `conexion` es retenido con testamento. | [S] | Crítica | Prueba de aceptación |
| REQ-F-010 | Existe una sola enumeración de estados de robot y de tarima y un solo esquema SQL canónico, usados por firmware, Pi, backend y tablero. | [S] | Alta | Prueba de aceptación |
| REQ-F-011 | Una Web API lee y escribe la base de datos y expone tarimas, historial, rechazos, robots e indicadores. | [N] | Crítica | Prueba de aceptación |
| REQ-F-012 | El tablero muestra los módulos Flotilla y Monitoreo con al menos 5 indicadores actualizados en tiempo real (≤ 2 s tras el cambio). | [N] | Alta | Inspección con evidencia (captura/video) |
| REQ-F-013 | Desde el tablero se pueden INICIAR, CANCELAR y PARAR misiones; cada orden tiene id, se publica por MQTT y su confirmación se refleja. | [S] | Media | Prueba de aceptación (API) e inspección (tablero) |
| REQ-F-014 | El tablero permite registrar tarimas, consultar sus ubicaciones, asignar rutas y revisar traslados concluidos. | [S] | Media | Prueba de aceptación (API) e inspección (tablero) |
| REQ-F-015 | Un robot simulado publica telemetría y eventos conformes al contrato para las 3 rutas, de modo que backend y tablero se prueben sin el robot físico. | [S] | Alta | Prueba de aceptación |
| REQ-F-016 | Retirado por CC-004: sin báscula no hay detección de "sin carga"; un peso declarado ≤ 0 se rechaza por REQ-F-003 y el tablero ya rechaza pesos de 0 kg (REQ-F-014). | — | — | — |
| REQ-F-017 | Cada entrega lleva un id único (`id_evento`); todas las entregas se registran, aunque sean de la misma tarima, y un mismo `id_evento` repetido por reenvío se descarta. | [D] | Crítica | Prueba de aceptación |
| REQ-NF-001 | Error de llegada al destino < 10 cm. | [D] | Crítica | Evidencia física (VAL-04) |
| REQ-NF-002 | Elevación de la carga de demostración (100 g) en < 15 s; la capacidad de diseño sigue siendo 10 kg. | [D] | Crítica | Evidencia física (VAL-01) |
| REQ-NF-003 | Latencia desde que la Pi envía el comando `DROP` (SUP-011, CC-004) hasta que la fila queda en la BD < 2 s, con marcas `ts` de ambos lados. | [D] | Crítica | Evidencia física (VAL-07) y prueba de aceptación (cálculo) |
| REQ-NF-004 | Traslado sostenido de 3 min sin reinicio ni corte de energía. | [S] | Alta | Evidencia física (VAL-06) |
| REQ-NF-005 | Antes de energizar se completa la lista de seguridad (cortos, polaridad, tierra común, divisor en ECHO) y hay un fusible de 10 A en la línea de la batería (SUP-004, pendiente de decisión). | [S] | Crítica | Inspección con evidencia (fotos y lista firmada) |
| REQ-NF-006 | El ESP32 y la Raspberry Pi se conectan a la red (MQTT, sin cable de datos entre ellos); el sistema integra al menos 2 sensores y 2 actuadores en red y cada integrante conecta y programa un sensor y un actuador. | [N] | Alta | Inspección en el reporte |
| REQ-NF-007 | Cada prueba VAL deja evidencia guardada (video, foto, log o captura) enlazada en el WP y la bitácora del robot. | [S] | Alta | Inspección |
| REQ-NF-008 | El gasto total no supera $10,000 MXN. | [S] | Media | Inspección (reporte final) |
| REQ-NF-009 | La carga física de demostración es de 100 g; los 10 kg son capacidad de diseño de referencia y no se cargan físicamente. | [D] | Alta | Inspección (reporte) |
| REQ-NF-010 | La evaluación del profesor consiste en una demostración de cómo se mueve el robot y cómo carga el peso. | [D] | Alta | Inspección (demo grabada) |
| REQ-NF-011 | La respuesta de paro ante un obstáculo es menor a 200 ms (SUP-022). | [S] | Alta | Evidencia física (VAL-05) |

## Ejemplos de requisitos críticos

Se redactan para todos los requisitos funcionales (nivel Estándar). Nacen [S] salvo los marcados [D] por las respuestas de G1.

### REQ-F-001
- EJ-001 [D]: Dado un peso declarado de 0.1 kg (la carga de demostración de 100 g), cuando se envía el comando `LIFT` con `peso_kg` 0.1, entonces el ESP32 responde `LIFT_OK` y la plataforma sube.
- EJ-002 [D] (caso límite): Dado un peso declarado de exactamente 10.0 kg, cuando se envía `LIFT`, entonces se acepta (el límite es inclusivo).

### REQ-F-002
- EJ-003 [D]: Dado un peso declarado de 11.80 kg para TAR-102, cuando se envía `LIFT`, entonces responde `OVERWEIGHT`, el actuador no se energiza, la tarima queda BLOQUEADA_SOBREPESO y hay una fila en `registro_rechazos_seguridad` con peso 11.80.
- EJ-004 [D] (caso límite): Dado un peso declarado de 10.1 kg, cuando se envía `LIFT`, entonces se rechaza igual que en EJ-003.

### REQ-F-003
- EJ-005 [D]: Dado un comando `LIFT` sin `peso_kg`, cuando llega al ESP32, entonces responde `PESO_INVALIDO` y no se energiza el actuador.
- EJ-006 [D] (caso límite): Dado un `LIFT` con `peso_kg` 0, negativo o no numérico, entonces responde `PESO_INVALIDO` y no eleva; no se interpreta como 0 kg aceptable.

### REQ-F-004
- EJ-007 [S]: Dado el robot avanzando, cuando aparece una caja a 15 cm, entonces los motores se detienen y se publica el evento OBSTACULO.
- EJ-008 [D] (caso límite): Dado el robot avanzando y el HC-SR04 sin eco válido, cuando pasa el tiempo de espera, entonces el robot se detiene (fallo seguro).

### REQ-F-005
- EJ-009 [S]: Dado el ESP32 apagado, cuando la Pi envía un comando, entonces a 1 s hay un error de tiempo de espera y no continúa la misión.
- EJ-010 [S] (caso límite): Dado un `MOVE` activo y la red caída o sin comandos durante más de 1 s, entonces el ESP32 detiene la tracción.

### REQ-F-006
- EJ-011 [S]: Dado el mapa 5×6, cuando se planea RUTA_1 de (0,0) a (4,5), entonces el camino tiene 10 celdas, ninguna es obstáculo y termina en (4,5).
- EJ-012 [S] (caso límite): Dado una meta en una celda obstáculo (0,3), cuando se planea, entonces no hay camino y la misión no inicia.

### REQ-F-007
- EJ-013 [S]: Dado un QR con "TAR-101" frente a la cámara, cuando se lee dentro de 2.5 s, entonces se devuelve `TAR-101`.
- EJ-014 [D] (caso límite): Dado ningún QR legible, cuando pasan 2.5 s, entonces la misión no inicia y no se usa el ID por defecto de la ruta.

### REQ-F-008
- EJ-015 [S]: Dado un evento DROP_OK de TAR-101 con peso 8.45 y destino (150, 120), cuando el backend lo procesa, entonces `tarimas` queda UBICADA_DESTINO en (150, 120) e `historial_movimientos` tiene una fila nueva.
- EJ-016 [S] (caso límite): Dado un DROP_OK cuyo destino coincide con la posición actual de la tarima, entonces igualmente se crea la fila de historial.

### REQ-F-009
- EJ-017 [S]: Dado un mensaje de telemetría con `ts`, `robot_id`, posición, velocidad, estado, peso y distancia, cuando se valida contra el esquema, entonces es válido.
- EJ-018 [S] (caso límite): Dado el mismo mensaje sin `ts`, entonces es inválido; y si el robot cae, el broker publica `FUERA_DE_LINEA` retenido.

### REQ-F-010
- EJ-019 [S]: Dado `estados.json`, entonces el estado de robot contiene exactamente INACTIVO, EN_MISION, ELEVANDO, EN_RUTA, DEPOSITANDO, DETENIDO_OBSTACULO y ERROR.
- EJ-020 [S] (caso límite): Dado `esquema.sql`, cuando se ejecuta en SQLite vacío, entonces `tarimas` incluye `ubicacion_nodo` y las otras tablas usan `ruta_ejecutada`, `peso_medido_kg` y `latencia_red_ms`.

### REQ-F-011
- EJ-021 [S]: Dado una tarima en la BD, cuando se consulta `GET /api/tarimas`, entonces el JSON incluye su id, estado y coordenadas.
- EJ-022 [S] (caso límite): Dado la BD vacía, cuando se consulta `GET /api/historial`, entonces devuelve una lista vacía y código 200.

### REQ-F-012
- EJ-023 [S]: Dado el robot simulado publicando, cuando se abre el tablero, entonces se ven al menos 5 indicadores que cambian en ≤ 2 s.
- EJ-024 [S] (caso límite): Dado el backend caído, cuando el tablero consulta, entonces muestra "sin conexión" y no presenta datos viejos como actuales.

### REQ-F-013
- EJ-025 [S]: Dado el robot INACTIVO, cuando se envía INICIAR con ruta RUTA_1 y TAR-101 desde el tablero, entonces se publica una orden con id y la UI muestra "aceptada" al llegar el ack.
- EJ-026 [S] (caso límite): Dado el robot EN_MISION, cuando se envía PARO, entonces se publica de inmediato; y un INICIAR en ese estado recibe ack "rechazada".

### REQ-F-014
- EJ-027 [S]: Dado el formulario, cuando se registra TAR-104 con 5.0 kg, entonces aparece en la lista con estado EN_PISO.
- EJ-028 [S] (caso límite): Dado un peso de 0 kg o un id "ABC", entonces el registro se rechaza con 400.

### REQ-F-015
- EJ-029 [S]: Dado el simulador con RUTA_1 y 8.45 kg, entonces genera telemetría, LIFT_OK y DROP_OK final en (150, 120), todos válidos contra el contrato.
- EJ-030 [S] (caso límite): Dado RUTA_2 con 11.80 kg, entonces genera SOBREPESO y ningún LIFT_OK ni DROP_OK.

### REQ-F-016
- EJ-031 y EJ-032: retirados por CC-004 (ver REQ-F-016).

### REQ-F-017
- EJ-033 [D]: Dado dos entregas de TAR-101 con `id_evento` distintos, cuando el backend las procesa, entonces `historial_movimientos` tiene dos filas.
- EJ-034 [D] (caso límite): Dado el mismo DROP_OK con el mismo `id_evento` recibido dos veces por un reenvío, entonces hay una sola fila; y un DROP_OK sin `id_evento` se descarta como inválido.
