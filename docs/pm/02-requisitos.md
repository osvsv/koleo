# Requisitos — KOLEO
Versión: 1.0 (borrador previo a G1)

Requisitos de sistema. Todos nacen [S] salvo los marcados [D] (decididos por Osvaldo el 2026-11-11, DP-04) o [N] (Reto IoT del curso). Fuentes: `importado/KOLEO_Documentacion_General.md` (DG), `importado/KOLEO_todo.md` (TODO), `importado/KOLEO_Metodologia_y_plan.md` (MP).

| ID | Requisito | Procedencia | Prioridad | Verificación |
| --- | --- | --- | --- | --- |
| REQ-F-001 | El robot eleva y sostiene una tarima de hasta 10.0 kg (límite inclusivo, SUP-010), medida por la báscula. | [S] | Crítica | Evidencia física (VAL-01) |
| REQ-F-002 | Si el peso medido supera 10.0 kg, el robot no eleva, publica el evento SOBREPESO, la tarima queda BLOQUEADA_SOBREPESO y se registra una fila en `registro_rechazos_seguridad`. | [S] | Crítica | Prueba de aceptación (software) y evidencia física (VAL-02) |
| REQ-F-003 | Si la báscula no entrega una lectura válida, el robot no eleva y responde error; "sin lectura" nunca equivale a 0 kg. | [S] | Crítica | Inspección de código y evidencia física |
| REQ-F-004 | Con el robot en movimiento, un obstáculo a 15 cm o menos (SUP-003) detiene la tracción en menos de 200 ms, de forma continua e independiente de la Raspberry Pi, y publica el evento OBSTACULO. | [S] | Crítica | Evidencia física (VAL-05) |
| REQ-F-005 | Si el enlace Pi–ESP32 no responde en 1 s o deja de recibir comandos con la tracción activa, la tracción se detiene y se reporta error. | [S] | Alta | Prueba de aceptación (software) y evidencia física |
| REQ-F-006 | El robot planea con A* y ejecuta RUTA_1, RUTA_2 y RUTA_3 del mapa 5×6 (celdas de 30 cm) sin colisión. | [S] | Alta | Prueba de aceptación (planificador) y evidencia física (VAL-03) |
| REQ-F-007 | La tarima se identifica por QR con formato `TAR-NNN`; sin lectura válida la misión no inicia (no se usa un ID por defecto). | [S] | Media | Prueba de aceptación y evidencia física |
| REQ-F-008 | Al depositar, se actualiza la tarima (estado UBICADA_DESTINO y coordenadas) y se crea una fila en `historial_movimientos` con ruta, origen, destino, peso y latencia; repetir el mismo evento no duplica filas. | [S] | Crítica | Prueba de aceptación (VAL-08) |
| REQ-F-009 | Los mensajes MQTT (`telemetria`, `evento`, `orden`, `orden/ack`, `conexion`) están definidos en un contrato validable, llevan `ts` en milisegundos, las órdenes llevan id con confirmación y `conexion` es retenido con testamento. | [S] | Crítica | Prueba de aceptación |
| REQ-F-010 | Existe una sola enumeración de estados de robot y de tarima y un solo esquema SQL canónico, usados por firmware, Pi, backend y tablero. | [S] | Alta | Prueba de aceptación |
| REQ-F-011 | Una Web API lee y escribe la base de datos y expone tarimas, historial, rechazos, robots e indicadores. | [N] | Crítica | Prueba de aceptación |
| REQ-F-012 | El tablero muestra los módulos Flotilla y Monitoreo con al menos 5 indicadores actualizados en tiempo real (≤ 2 s tras el cambio). | [N] | Alta | Inspección con evidencia (captura/video) |
| REQ-F-013 | Desde el tablero se pueden INICIAR, CANCELAR y PARAR misiones; cada orden tiene id, se publica por MQTT y su confirmación se refleja. | [S] | Media | Prueba de aceptación (API) e inspección (tablero) |
| REQ-F-014 | El tablero permite registrar tarimas, consultar sus ubicaciones, asignar rutas y revisar traslados concluidos. | [S] | Media | Prueba de aceptación (API) e inspección (tablero) |
| REQ-F-015 | Un robot simulado publica telemetría y eventos conformes al contrato para las 3 rutas, de modo que backend y tablero se prueben sin el robot físico. | [S] | Alta | Prueba de aceptación |
| REQ-NF-001 | Error de llegada al destino < 10 cm. | [D] | Crítica | Evidencia física (VAL-04) |
| REQ-NF-002 | Elevación de 10 kg en < 15 s. | [D] | Crítica | Evidencia física (VAL-01) |
| REQ-NF-003 | Latencia desde que la celda detecta la tarima suelta hasta que la fila queda en la BD < 2 s, con marcas `ts` de ambos lados (SUP-011). | [S] | Crítica | Evidencia física (VAL-07) y prueba de aceptación (cálculo) |
| REQ-NF-004 | Traslado sostenido de 3 min sin reinicio ni corte de energía. | [S] | Alta | Evidencia física (VAL-06) |
| REQ-NF-005 | Antes de energizar se completa la lista de seguridad (cortos, polaridad, tierra común, divisor en ECHO) y hay un fusible de 10 A en la línea de la batería (SUP-004). | [S] | Crítica | Inspección con evidencia (fotos y lista firmada) |
| REQ-NF-006 | El sistema integra al menos 2 sensores y 2 actuadores en red (MQTT) y cada integrante conecta y programa un sensor y un actuador (SUP-001). | [N] | Alta | Inspección en el reporte |
| REQ-NF-007 | Cada prueba VAL deja evidencia guardada (video, foto, log o captura) enlazada en el WP y la bitácora del robot. | [S] | Alta | Inspección |
| REQ-NF-008 | El gasto total no supera $10,000 MXN. | [S] | Media | Inspección (reporte final) |

## Ejemplos de requisitos críticos

Se redactan para todos los requisitos funcionales (nivel Estándar). Todos nacen [S]; los valida G1.

### REQ-F-001
- EJ-001 [S]: Dado una tarima de 8.45 kg (TAR-101) bajo el robot, cuando se envía `LIFT:TAR-101`, entonces el ESP32 responde `ACK:LIFT_OK` y la plataforma sube.
- EJ-002 [S] (caso límite): Dado una masa calibrada de 10.0 kg, cuando se envía `LIFT`, entonces se eleva (el límite es inclusivo).

### REQ-F-002
- EJ-003 [S]: Dado TAR-102 con 11.80 kg, cuando se envía `LIFT:TAR-102`, entonces responde `ERR:OVERWEIGHT`, el actuador no se energiza, la tarima queda BLOQUEADA_SOBREPESO y hay una fila en `registro_rechazos_seguridad` con peso 11.80.
- EJ-004 [S] (caso límite): Dado un peso de 10.1 kg, cuando se envía `LIFT`, entonces se rechaza igual que en EJ-003.

### REQ-F-003
- EJ-005 [S]: Dado el HX711 desconectado, cuando se envía `LIFT:TAR-101`, entonces responde `ERR:SCALE_FAIL` y no se energiza el actuador.
- EJ-006 [S] (caso límite): Dado una lectura válida de exactamente 0.0 kg (sin tarima), cuando se envía `LIFT`, entonces no se levanta y se reporta que no hay carga (no es lo mismo que fallo de báscula).

### REQ-F-004
- EJ-007 [S]: Dado el robot avanzando, cuando aparece una caja a 15 cm, entonces los motores se detienen en menos de 200 ms y se publica el evento OBSTACULO.
- EJ-008 [S] (caso límite): Dado el robot avanzando y el HC-SR04 sin eco válido, cuando pasa el tiempo de espera, entonces el robot se detiene (fallo seguro).

### REQ-F-005
- EJ-009 [S]: Dado el ESP32 apagado, cuando la Pi envía un comando, entonces a 1 s lanza error de tiempo de espera y no continúa la misión.
- EJ-010 [S] (caso límite): Dado un `MOVE` activo y ningún comando durante más de 1 s, entonces el ESP32 detiene la tracción.

### REQ-F-006
- EJ-011 [S]: Dado el mapa 5×6, cuando se planea RUTA_1 de (0,0) a (4,5), entonces el camino tiene 10 celdas, ninguna es obstáculo y termina en (4,5).
- EJ-012 [S] (caso límite): Dado una meta en una celda obstáculo (0,3), cuando se planea, entonces no hay camino y la misión no inicia.

### REQ-F-007
- EJ-013 [S]: Dado un QR con "TAR-101" frente a la cámara, cuando se lee dentro de 2.5 s, entonces se devuelve `TAR-101`.
- EJ-014 [S] (caso límite): Dado ningún QR o contenido "XYZ", cuando pasan 2.5 s, entonces la misión no inicia y no se usa el ID por defecto de la ruta.

### REQ-F-008
- EJ-015 [S]: Dado un evento DROP_OK de TAR-101 con peso 8.45 y destino (150, 120), cuando el backend lo procesa, entonces `tarimas` queda UBICADA_DESTINO en (150, 120) e `historial_movimientos` tiene una fila nueva.
- EJ-016 [S] (caso límite): Dado el mismo evento recibido dos veces, entonces sigue habiendo una sola fila de historial.

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
