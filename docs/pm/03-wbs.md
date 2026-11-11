# WBS — KOLEO
Versión: 1.0 (borrador previo a G1)

Convenciones: los WP de software los ejecuta `/pm-ejecutar`. Los WP **físicos** (tipo `integracion`) los hacen personas; su evidencia va a `docs/pm/evidencia/hw/<WP>/` y el auditor la inspecciona (DP-09). Los WP de firmware combinan código (lo escribe el ejecutor) y pruebas de banco (las aportan personas). Los criterios llevan procedencia [S] salvo los marcados [D] por DP-04.

## Árbol

1. Contratos y datos
   1.1 WP-1.1 Contratos MQTT, UART, estados y SQL
   1.2 WP-1.2 Robot simulado
   1.3 WP-1.3 Backend de persistencia y Web API
2. Hardware
   2.1 WP-2.1 Chasis y tracción
   2.2 WP-2.2 Mecanismo de elevación
   2.3 WP-2.3 Energía y energizado seguro
   2.4 WP-2.4 Sensores montados
3. Firmware ESP32
   3.1 WP-3.1 Báscula con fallo seguro y elevación
   3.2 WP-3.2 Enlace UART Pi–ESP32
   3.3 WP-3.3 Parada continua por obstáculo
4. Raspberry Pi
   4.1 WP-4.1 Puente MQTT
   4.2 WP-4.2 Avance por distancia con encoders
   4.3 WP-4.3 Planificador A* y misión
   4.4 WP-4.4 Lectura QR
5. Tablero
   5.1 WP-5.1 Tablero: flotilla, monitoreo e indicadores
   5.2 WP-5.2 Tablero: control y gestión logística
6. Validación
   6.1 WP-6.1 Pruebas de elevación, rechazo, obstáculo y latencia
   6.2 WP-6.2 Pruebas de rutas, llegada y traslado sostenido
   6.3 WP-6.3 Ensayo general y reporte

## Diccionario

### WP-1.1 — Contratos MQTT, UART, estados y SQL
- Riesgo: medio
- Tipo: entregable
- Entregable: carpeta `contratos/` con el contrato de mensajes MQTT (JSON Schema), el contrato UART, la enumeración de estados y el esquema SQL canónico
- Alcance de archivos: contratos/**
- Interfaz: `contratos/mensajes.schema.json` (JSON Schema 2020-12 con `$defs`: `telemetria`, `evento`, `orden`, `orden_ack`, `conexion`); `contratos/estados.json` (`{"robot": [...], "tarima": [...]}`); `contratos/esquema.sql` (SQLite, ejecutable con `sqlite3.Connection.executescript`); `contratos/mqtt.md` y `contratos/uart.md` (documentos)
- Trazabilidad: REQ-F-009, REQ-F-010
- Dependencias: ninguna
- Criterios de aceptación:
  - CA-1.1.1 [S]: `telemetria` exige `ts` (entero, ms), `robot_id`, `x_cm`, `y_cm`, `velocidad_cm_s`, `estado`, `peso_kg` y `distancia_obstaculo_cm`; `evento` exige `ts`, `robot_id`, `tipo` ∈ {LIFT_OK, SOBREPESO, OBSTACULO, DROP_OK, ERROR} e `id_tarima` — Evidencia: tests/aceptacion/test_wp_1_1.py
  - CA-1.1.2 [S]: `orden` exige `ts`, `id_orden` y `tipo` ∈ {INICIAR, CANCELAR, PARO}; INICIAR exige además `ruta` e `id_tarima`; `orden_ack` exige `id_orden` y `resultado` ∈ {aceptada, rechazada}; `conexion` admite EN_LINEA y FUERA_DE_LINEA — Evidencia: tests/aceptacion/test_wp_1_1.py
  - CA-1.1.3 [S]: un mensaje sin `ts` o con `tipo` desconocido es inválido contra el esquema — Evidencia: tests/aceptacion/test_wp_1_1.py
  - CA-1.1.4 [S]: `estados.json` contiene exactamente los estados de robot (INACTIVO, EN_MISION, ELEVANDO, EN_RUTA, DEPOSITANDO, DETENIDO_OBSTACULO, ERROR) y de tarima (EN_PISO, EN_TRANSITO, UBICADA_DESTINO, BLOQUEADA_SOBREPESO) — Evidencia: tests/aceptacion/test_wp_1_1.py
  - CA-1.1.5 [S]: `esquema.sql` crea en un SQLite vacío `tarimas` (con `ubicacion_nodo`), `historial_movimientos` (con `ruta_ejecutada`, `peso_medido_kg`, `latencia_red_ms`) y `registro_rechazos_seguridad`, con claves foráneas a `tarimas` — Evidencia: tests/aceptacion/test_wp_1_1.py
  - CA-1.1.6 [S]: `mqtt.md` define los temas `koleo/robot1/telemetria`, `evento`, `orden`, `orden/ack` y `conexion` con publicador, QoS, retención de `conexion` y su testamento — Evidencia: inspección de contratos/mqtt.md
  - CA-1.1.7 [S]: `uart.md` documenta, para `LIFT`, `MOVE`, `STOP` y `DROP`, la respuesta (incluye `ACK:LIFT_OK`, `ERR:OVERWEIGHT`, `ERR:SCALE_FAIL`, `ERR:OBSTACULO_CERCANO`) y el tiempo de espera de 1 s — Evidencia: inspección de contratos/uart.md

### WP-1.2 — Robot simulado
- Riesgo: bajo
- Tipo: entregable
- Entregable: simulador de Python que genera (y opcionalmente publica) la telemetría y los eventos de una misión conforme al contrato
- Alcance de archivos: simulador/**
- Interfaz: `simulador.robot_falso.generar_mision(ruta: str, peso_kg: float) -> list[tuple[str, dict]]` (pares `(tema, payload)` en orden); CLI `python -m simulador.robot_falso --ruta RUTA_1 --peso 8.45 [--broker HOST]`
- Trazabilidad: REQ-F-015, REQ-F-009
- Dependencias: WP-1.1
- Criterios de aceptación:
  - CA-1.2.1 [S]: `generar_mision("RUTA_1", 8.45)` devuelve solo mensajes válidos contra `contratos/mensajes.schema.json`, con un evento LIFT_OK de TAR-101 y un DROP_OK final en (150, 120) — Evidencia: tests/aceptacion/test_wp_1_2.py
  - CA-1.2.2 [S]: `generar_mision("RUTA_2", 11.80)` incluye un evento SOBREPESO y no incluye LIFT_OK ni DROP_OK — Evidencia: tests/aceptacion/test_wp_1_2.py
  - CA-1.2.3 [S]: con `peso_kg = 10.0` la misión se completa (límite inclusivo) y con 10.1 se rechaza — Evidencia: tests/aceptacion/test_wp_1_2.py
  - CA-1.2.4 [S]: una ruta desconocida lanza `ValueError` — Evidencia: tests/aceptacion/test_wp_1_2.py
  - CA-1.2.5 [S]: mensajes de telemetría consecutivos distan ≤ 500 ms en `ts` — Evidencia: tests/aceptacion/test_wp_1_2.py
  - CA-1.2.6 [S]: con `--broker`, los mensajes aparecen en `mosquitto_sub -t 'koleo/#'` — Evidencia: docs/pm/evidencia/WP-1.2/captura_mosquitto.txt

### WP-1.3 — Backend de persistencia y Web API
- Riesgo: alto
- Tipo: entregable
- Entregable: servicio Python que recibe mensajes MQTT, los guarda en SQLite con el esquema canónico y los expone por una API REST
- Alcance de archivos: backend/**
- Interfaz: `backend.koleo.ingesta.procesar_mensaje(conn: sqlite3.Connection, topic: str, payload: dict, recibido_ms: int) -> None`; `backend.koleo.api.crear_app(db_path: str, publicador=None) -> flask.Flask` con `GET /api/tarimas`, `/api/historial`, `/api/rechazos`, `/api/robots`, `/api/indicadores`; `backend/koleo/suscriptor.py` (cliente MQTT que llama a `procesar_mensaje`)
- Trazabilidad: REQ-F-008, REQ-F-011, REQ-NF-003
- Dependencias: WP-1.1, WP-1.2
- Criterios de aceptación:
  - CA-1.3.1 [S]: un evento DROP_OK de TAR-101 (8.45 kg, destino 150, 120) deja la tarima UBICADA_DESTINO en esas coordenadas y crea una fila en `historial_movimientos` — Evidencia: tests/aceptacion/test_wp_1_3.py
  - CA-1.3.2 [S]: `latencia_red_ms` de esa fila es `recibido_ms − ts` del evento y es ≥ 0 — Evidencia: tests/aceptacion/test_wp_1_3.py
  - CA-1.3.3 [S]: un evento SOBREPESO de TAR-102 (11.80 kg) crea una fila en `registro_rechazos_seguridad` con ese peso, deja la tarima BLOQUEADA_SOBREPESO y no crea fila de historial — Evidencia: tests/aceptacion/test_wp_1_3.py
  - CA-1.3.4 [S]: con la salida de `generar_mision` para TAR-101 (RUTA_1), TAR-102 (RUTA_2, 11.80 kg) y TAR-103 (RUTA_3), queda 2 filas de historial y 1 de rechazo (VAL-08) — Evidencia: tests/aceptacion/test_wp_1_3.py
  - CA-1.3.5 [S]: un mensaje inválido (sin `ts` o `tipo` desconocido) se descarta, no cambia la BD y se registra en el log — Evidencia: tests/aceptacion/test_wp_1_3.py
  - CA-1.3.6 [S]: procesar dos veces el mismo DROP_OK no duplica la fila de historial — Evidencia: tests/aceptacion/test_wp_1_3.py
  - CA-1.3.7 [S]: `GET /api/tarimas` devuelve id, estado y coordenadas; `GET /api/historial` sobre una BD vacía devuelve `[]` con código 200 — Evidencia: tests/aceptacion/test_wp_1_3.py
  - CA-1.3.8 [S]: `GET /api/indicadores` devuelve al menos las claves `ocupacion`, `posicion_robot`, `tiempo_ciclo_s`, `peso_kg`, `precision_cm`, `alertas` — Evidencia: tests/aceptacion/test_wp_1_3.py
  - CA-1.3.9 [S]: el suscriptor corre contra un broker Mosquitto real con el simulador y la BD queda poblada — Evidencia: docs/pm/evidencia/WP-1.3/corrida_con_broker.txt

### WP-2.1 — Chasis y tracción
- Riesgo: medio
- Tipo: integracion
- Entregable: base de 300 × 300 mm con motores GA25-370, ruedas de 65 mm y ruedas locas ensambladas
- Alcance de archivos: docs/pm/evidencia/hw/WP-2.1/**
- Interfaz: ninguna (físico)
- Trazabilidad: REQ-F-001, REQ-F-006
- Dependencias: ninguna
- Criterios de aceptación:
  - CA-2.1.1 [S]: el chasis soporta 10 kg estáticos sin deformarse — Evidencia: docs/pm/evidencia/hw/WP-2.1/carga_estatica.jpg
  - CA-2.1.2 [S]: las dos ruedas motrices giran libres y las ruedas locas (2 o 4) no dejan el robot cojo sobre el piso — Evidencia: docs/pm/evidencia/hw/WP-2.1/giro_libre.mp4
  - CA-2.1.3 [S]: dimensiones ≤ 300 × 300 mm — Evidencia: docs/pm/evidencia/hw/WP-2.1/medidas.jpg
  - CA-2.1.4 [S]: la bitácora del robot registra el ensamble con fecha, cambios y resultado — Evidencia: docs/pm/evidencia/hw/WP-2.1/bitacora.md

### WP-2.2 — Mecanismo de elevación
- Riesgo: alto
- Tipo: integracion
- Entregable: actuador lineal de 75 kg con guías verticales, adaptador y celda de carga montados bajo la plataforma
- Alcance de archivos: docs/pm/evidencia/hw/WP-2.2/**
- Interfaz: ninguna (físico)
- Trazabilidad: REQ-F-001
- Dependencias: WP-2.1
- Criterios de aceptación:
  - CA-2.2.1 [S]: con fuente de banco de 12 V sube y baja sin carga el recorrido completo, sin trabarse ni ladear la plataforma — Evidencia: docs/pm/evidencia/hw/WP-2.2/ciclo_sin_carga.mp4
  - CA-2.2.2 [S]: la cadena actuador → adaptador → celda → plataforma cabe en la altura total del robot (~19 cm) — Evidencia: docs/pm/evidencia/hw/WP-2.2/altura.jpg
  - CA-2.2.3 [S]: el tiempo de un recorrido completo sin carga queda anotado — Evidencia: docs/pm/evidencia/hw/WP-2.2/bitacora.md

### WP-2.3 — Energía y energizado seguro
- Riesgo: alto
- Tipo: integracion
- Entregable: distribución de 12 V, 5.1 V y 3.3 V con fusible de 10 A y robot energizado sin carga
- Alcance de archivos: docs/pm/evidencia/hw/WP-2.3/**
- Interfaz: ninguna (físico)
- Trazabilidad: REQ-NF-005
- Dependencias: ninguna
- Criterios de aceptación:
  - CA-2.3.1 [S]: existe un diagrama de alimentación real y la lista antes de energizar (cortos con multímetro, polaridad de 12 V, tierra común, divisor 1 kΩ/2 kΩ en ECHO) firmada por quien la hizo — Evidencia: docs/pm/evidencia/hw/WP-2.3/lista_energizado.md
  - CA-2.3.2 [S]: hay un fusible de 10 A en la línea positiva de la batería y el conector T se puede desconectar rápido — Evidencia: docs/pm/evidencia/hw/WP-2.3/fusible.jpg
  - CA-2.3.3 [S]: voltajes medidos con el robot energizado sin carga anotados (12 V, 5.1 V del buck, 3.3 V) — Evidencia: docs/pm/evidencia/hw/WP-2.3/voltajes.md
  - CA-2.3.4 [S]: la Pi arranca del SSD con `vcgencmd get_throttled` = `0x0` — Evidencia: docs/pm/evidencia/hw/WP-2.3/throttled.txt
  - CA-2.3.5 [S]: tras 3 min con todo encendido sin carga, la LiPo en reposo mide ≥ 10.8 V — Evidencia: docs/pm/evidencia/hw/WP-2.3/bateria.md

### WP-2.4 — Sensores montados
- Riesgo: medio
- Tipo: integracion
- Entregable: HC-SR04, VL53L1X, celda de carga con HX711 y encoders montados y leyendo en el robot armado
- Alcance de archivos: docs/pm/evidencia/hw/WP-2.4/**
- Interfaz: ninguna (físico)
- Trazabilidad: REQ-F-004, REQ-F-006, REQ-NF-006
- Dependencias: WP-2.1, WP-2.2, WP-2.3
- Criterios de aceptación:
  - CA-2.4.1 [S]: cada sensor reporta lecturas coherentes con el robot armado (log serial por sensor) — Evidencia: docs/pm/evidencia/hw/WP-2.4/lecturas.txt
  - CA-2.4.2 [S]: el ECHO del HC-SR04 llega al ESP32 con ≤ 3.3 V medidos — Evidencia: docs/pm/evidencia/hw/WP-2.4/echo_voltaje.jpg
  - CA-2.4.3 [S]: los contadores de encoder suben al girar la rueda hacia adelante y bajan hacia atrás, en ambas ruedas — Evidencia: docs/pm/evidencia/hw/WP-2.4/encoders.txt
  - CA-2.4.4 [S]: quedan registrados qué integrante conectó y programó cada sensor y actuador (Etapa 2 del Reto) — Evidencia: docs/pm/evidencia/hw/WP-2.4/reparto_etapa2.md

### WP-3.1 — Báscula con fallo seguro y elevación
- Riesgo: alto
- Tipo: entregable
- Entregable: esqueleto del firmware ESP32 con el pinout final, lectura de báscula que distingue "sin lectura" de 0 kg, y `LIFT` con rechazo por sobrepeso
- Alcance de archivos: firmware/esp32/**, docs/pm/evidencia/hw/WP-3.1/**
- Interfaz: `bool medirPesoKg(float &kg)` (falso si no hay lectura válida); comando UART `LIFT:<id>` → `ACK:LIFT_OK` | `ERR:OVERWEIGHT` | `ERR:SCALE_FAIL`
- Trazabilidad: REQ-F-002, REQ-F-003, REQ-F-001
- Dependencias: ninguna
- Criterios de aceptación:
  - CA-3.1.1 [S]: `firmware/esp32/src/pines.h` coincide con el pinout final de `importado/KOLEO_todo.md` §9 (IN3 en GPIO 23, canal B de encoders en 36/39, VL53L1X, GPIO 14 en bajo al inicio) — Evidencia: inspección de firmware/esp32/src/pines.h
  - CA-3.1.2 [S]: `medirPesoKg` devuelve falso cuando el HX711 no está listo o expira, y nunca devuelve 0.0 por ese motivo — Evidencia: inspección de firmware/esp32/src/bascula.cpp
  - CA-3.1.3 [S]: con el HX711 desconectado, `LIFT` responde `ERR:SCALE_FAIL` y no se energiza el actuador — Evidencia: docs/pm/evidencia/hw/WP-3.1/scale_fail.txt
  - CA-3.1.4 [S]: calibrada con pesas de 1, 5 y 10 kg, el error de lectura es < 0.2 kg — Evidencia: docs/pm/evidencia/hw/WP-3.1/calibracion.md
  - CA-3.1.5 [S]: con 11.8 kg responde `ERR:OVERWEIGHT` y con 10.0 kg acepta — Evidencia: docs/pm/evidencia/hw/WP-3.1/umbral.txt
  - CA-3.1.6 [S]: la elevación usa `millis()` y no `delay()` bloqueante, y el actuador tiene un tiempo máximo de 8 s — Evidencia: inspección de firmware/esp32/src/elevacion.cpp

### WP-3.2 — Enlace UART Pi–ESP32
- Riesgo: medio
- Tipo: entregable
- Entregable: cliente Python del enlace y manejo de comandos `LIFT`, `MOVE`, `STOP`, `DROP` en el firmware, con tiempo de espera y paro por pérdida de comandos
- Alcance de archivos: pi/uart.py, firmware/esp32/src/main.cpp, firmware/esp32/src/enlace_uart.*, docs/pm/evidencia/hw/WP-3.2/**
- Interfaz: `pi.uart.EnlaceESP32(puerto, timeout_s: float = 1.0)` con `enviar(cmd: str) -> str` (devuelve la línea de respuesta o lanza `TimeoutError`), `lift(id)`, `move(izq, der)`, `stop()`, `drop(id, x_cm, y_cm)`; `puerto` es un objeto tipo `serial.Serial` (se inyecta uno falso en pruebas)
- Trazabilidad: REQ-F-005
- Dependencias: WP-1.1, WP-3.1
- Criterios de aceptación:
  - CA-3.2.1 [S]: `enviar("LIFT:TAR-101")` contra un puerto falso que responde `ACK:LIFT_OK` devuelve `"ACK:LIFT_OK"`; con `ERR:OVERWEIGHT` devuelve esa línea — Evidencia: tests/aceptacion/test_wp_3_2.py
  - CA-3.2.2 [S]: sin respuesta en 1 s `enviar` lanza `TimeoutError` y el enlace intenta enviar `STOP` — Evidencia: tests/aceptacion/test_wp_3_2.py
  - CA-3.2.3 [S]: `drop("TAR-101", 150, 120)` escribe `DROP:TAR-101:150:120\n` y `move(80, -80)` escribe `MOVE:80:-80\n` — Evidencia: tests/aceptacion/test_wp_3_2.py
  - CA-3.2.4 [S]: el firmware responde a los cuatro comandos con la respuesta del contrato y maneja `DROP` (hoy ausente del `loop()`) — Evidencia: docs/pm/evidencia/hw/WP-3.2/comandos_banco.txt
  - CA-3.2.5 [S]: con `MOVE` activo y sin comandos durante más de 1 s, el ESP32 detiene la tracción — Evidencia: docs/pm/evidencia/hw/WP-3.2/watchdog.mp4

### WP-3.3 — Parada continua por obstáculo
- Riesgo: alto
- Tipo: entregable
- Entregable: lectura periódica del HC-SR04 en el firmware, independiente de los comandos, que detiene la tracción y avisa
- Alcance de archivos: firmware/esp32/src/obstaculo.*, firmware/esp32/src/main.cpp, docs/pm/evidencia/hw/WP-3.3/**
- Interfaz: constante `DISTANCIA_PARO_CM = 15`; aviso UART `ERR:OBSTACULO_CERCANO`
- Trazabilidad: REQ-F-004
- Dependencias: WP-2.4, WP-3.2
- Criterios de aceptación:
  - CA-3.3.1 [S]: la lectura del HC-SR04 se ejecuta periódicamente (≤ 50 ms) aunque no lleguen comandos — Evidencia: inspección de firmware/esp32/src/obstaculo.cpp
  - CA-3.3.2 [S]: con el robot avanzando, una caja a 15 cm detiene los motores en menos de 200 ms y se envía `ERR:OBSTACULO_CERCANO` — Evidencia: docs/pm/evidencia/hw/WP-3.3/paro_15cm.mp4 y docs/pm/evidencia/hw/WP-3.3/paro_log.txt
  - CA-3.3.3 [S]: sin eco válido del HC-SR04 con la tracción activa, el robot se detiene (fallo seguro) — Evidencia: docs/pm/evidencia/hw/WP-3.3/sin_eco.txt

### WP-4.1 — Puente MQTT
- Riesgo: alto
- Tipo: entregable
- Entregable: proceso en la Pi que traduce eventos UART a mensajes MQTT, publica telemetría y atiende órdenes con acuse
- Alcance de archivos: pi/puente_mqtt.py, pi/ordenes.py, docs/pm/evidencia/hw/WP-4.1/**
- Interfaz: `pi.puente_mqtt.traducir_uart(linea: str, contexto: dict, ts_ms: int) -> list[tuple[str, dict]]`; `pi.ordenes.procesar_orden(payload: dict, estado_robot: str, vistas: set) -> dict` (devuelve el `orden_ack`)
- Trazabilidad: REQ-F-009, REQ-F-013, REQ-F-008
- Dependencias: WP-1.1, WP-1.3, WP-3.2
- Criterios de aceptación:
  - CA-4.1.1 [S]: `traducir_uart("ACK:LIFT_OK", ...)`, `"ERR:OVERWEIGHT"` y `"ERR:OBSTACULO_CERCANO"` producen eventos válidos contra el esquema (LIFT_OK, SOBREPESO, OBSTACULO) — Evidencia: tests/aceptacion/test_wp_4_1.py
  - CA-4.1.2 [S]: una orden INICIAR válida con el robot INACTIVO produce un ack `aceptada`; el mismo `id_orden` repetido produce el mismo ack sin ejecutarse otra vez — Evidencia: tests/aceptacion/test_wp_4_1.py
  - CA-4.1.3 [S]: una orden INICIAR con el robot EN_MISION produce ack `rechazada`; una orden PARO se acepta en cualquier estado — Evidencia: tests/aceptacion/test_wp_4_1.py
  - CA-4.1.4 [S]: la telemetría se publica al menos 2 veces por segundo con `ts` creciente — Evidencia: docs/pm/evidencia/hw/WP-4.1/telemetria.txt
  - CA-4.1.5 [S]: al conectar se publica `EN_LINEA` retenido y, al matar el proceso, el broker publica `FUERA_DE_LINEA` — Evidencia: docs/pm/evidencia/hw/WP-4.1/conexion.txt
  - CA-4.1.6 [S]: con el robot real, el tablero o el backend muestran el robot moviendo una celda — Evidencia: docs/pm/evidencia/hw/WP-4.1/robot_real.mp4

### WP-4.2 — Avance por distancia con encoders
- Riesgo: medio
- Tipo: entregable
- Entregable: conversión de pulsos a distancia y avance por celda en lazo cerrado
- Alcance de archivos: pi/odometria.py, firmware/esp32/src/odometria.*, firmware/esp32/src/main.cpp, docs/pm/evidencia/hw/WP-4.2/**
- Interfaz: `pi.odometria.pulsos_a_cm(pulsos: int, pulsos_por_vuelta: float = 515, diametro_rueda_mm: float = 65) -> float`; `pi.odometria.cm_a_pulsos(cm: float, ...) -> int`
- Trazabilidad: REQ-F-006, REQ-NF-001
- Dependencias: WP-3.3
- Criterios de aceptación:
  - CA-4.2.1 [S]: `pulsos_a_cm(515)` ≈ 20.42 cm (π × 6.5, ±0.01) y `pulsos_a_cm(0)` = 0 — Evidencia: tests/aceptacion/test_wp_4_2.py
  - CA-4.2.2 [S]: `cm_a_pulsos(pulsos_a_cm(n))` ≈ n para n ∈ {100, 515, 1000}, y `cm_a_pulsos(30)` ≈ 757 — Evidencia: tests/aceptacion/test_wp_4_2.py
  - CA-4.2.3 [S]: pulsos negativos dan distancia negativa (marcha atrás) — Evidencia: tests/aceptacion/test_wp_4_2.py
  - CA-4.2.4 [S]: una celda (30 cm) avanza con error < 3 cm en 5 repeticiones, con y sin carga — Evidencia: docs/pm/evidencia/hw/WP-4.2/celda_30cm.md
  - CA-4.2.5 [S]: si hay PWM y los encoders no cambian durante 1 s, el firmware detiene la tracción y reporta error — Evidencia: docs/pm/evidencia/hw/WP-4.2/atasco.txt

### WP-4.3 — Planificador A* y misión
- Riesgo: medio
- Tipo: entregable
- Entregable: mapa 5×6, planificador A* y orquestación de la misión sobre el enlace UART
- Alcance de archivos: pi/mapa.py, pi/planificador.py, pi/mision.py
- Interfaz: `pi.mapa.MAPA`, `pi.mapa.RUTAS`; `pi.planificador.PlanificadorAStar(mapa).planificar(inicio, meta) -> list[tuple[int, int]] | None`; `pi.mision.celda_a_cm(fila, col) -> tuple[float, float]`; `pi.mision.ejecutar_mision(ruta: str, id_tarima: str, enlace, odometria) -> dict`
- Trazabilidad: REQ-F-006, REQ-F-007, REQ-F-002
- Dependencias: WP-3.2, WP-4.2, WP-4.4
- Criterios de aceptación:
  - CA-4.3.1 [S]: `planificar` resuelve RUTA_1, RUTA_2 y RUTA_3 con caminos de 10, 6 y 8 celdas (incluyendo inicio y meta) sin pasar por celdas con 1 — Evidencia: tests/aceptacion/test_wp_4_3.py
  - CA-4.3.2 [S]: una meta en obstáculo (0,3) devuelve `None`; con inicio igual a meta devuelve solo esa celda — Evidencia: tests/aceptacion/test_wp_4_3.py
  - CA-4.3.3 [S]: `celda_a_cm(4, 5)` = (150, 120) — Evidencia: tests/aceptacion/test_wp_4_3.py
  - CA-4.3.4 [S]: con un enlace falso, `ejecutar_mision("RUTA_1", "TAR-101", ...)` envía `LIFT`, luego movimientos y `DROP` con las coordenadas del destino — Evidencia: tests/aceptacion/test_wp_4_3.py
  - CA-4.3.5 [S]: si `LIFT` responde `ERR:OVERWEIGHT` o `ERR:SCALE_FAIL`, no se envía `MOVE` ni `DROP` y el resultado indica rechazo — Evidencia: tests/aceptacion/test_wp_4_3.py
  - CA-4.3.6 [S]: si el enlace lanza `TimeoutError`, la misión se aborta con `STOP` y el resultado indica error — Evidencia: tests/aceptacion/test_wp_4_3.py

### WP-4.4 — Lectura QR
- Riesgo: medio
- Tipo: entregable
- Entregable: lectura de QR con Picamera2 y validación del formato `TAR-NNN`
- Alcance de archivos: pi/qr.py, pi/camara.py, docs/pm/evidencia/hw/WP-4.4/**
- Interfaz: `pi.qr.identificar_tarima(camara, timeout_s: float = 2.5) -> str` (lanza `TarimaNoIdentificada`); `camara` es un objeto con `capturar() -> numpy.ndarray` (se inyecta una falsa en pruebas); `pi/camara.py` implementa `capturar` con Picamera2
- Trazabilidad: REQ-F-007
- Dependencias: ninguna
- Criterios de aceptación:
  - CA-4.4.1 [S]: una imagen con QR "TAR-101" devuelve `"TAR-101"` — Evidencia: tests/aceptacion/test_wp_4_4.py
  - CA-4.4.2 [S]: sin QR durante 2.5 s lanza `TarimaNoIdentificada` — Evidencia: tests/aceptacion/test_wp_4_4.py
  - CA-4.4.3 [S]: un QR con contenido que no cumple `TAR-\d{3}` (por ejemplo "XYZ") lanza `TarimaNoIdentificada` — Evidencia: tests/aceptacion/test_wp_4_4.py
  - CA-4.4.4 [S]: `pi/camara.py` usa Picamera2 y no `cv2.VideoCapture` — Evidencia: inspección de pi/camara.py
  - CA-4.4.5 [S]: en la Pi con el Camera Module 3, TAR-101 se lee en menos de 2.5 s en 5 de 5 intentos — Evidencia: docs/pm/evidencia/hw/WP-4.4/lectura_5_de_5.md

### WP-5.1 — Tablero: flotilla, monitoreo e indicadores
- Riesgo: medio
- Tipo: entregable
- Entregable: aplicación React + Vite + Tailwind con los módulos Flotilla y Monitoreo y al menos 5 indicadores en tiempo real
- Alcance de archivos: ui/**, docs/pm/evidencia/WP-5.1/**
- Interfaz: `npm run build` y `npm run dev`; consume `GET /api/robots` y `GET /api/indicadores` por consulta cada 1 s (SUP-015)
- Trazabilidad: REQ-F-012
- Dependencias: WP-1.2, WP-1.3
- Criterios de aceptación:
  - CA-5.1.1 [S]: `npm run build` termina sin errores — Evidencia: docs/pm/evidencia/WP-5.1/build.txt
  - CA-5.1.2 [S]: Flotilla muestra, por robot, identificador, conexión (EN_LINEA / FUERA_DE_LINEA), estado y alertas — Evidencia: docs/pm/evidencia/WP-5.1/flotilla.png (con el simulador)
  - CA-5.1.3 [S]: Monitoreo muestra peso frente a capacidad, velocidad, ruta e historial reciente — Evidencia: docs/pm/evidencia/WP-5.1/monitoreo.png
  - CA-5.1.4 [S]: se muestran al menos 5 indicadores (ocupación, posición del robot, tiempo de ciclo, peso, precisión, alertas) y cambian en ≤ 2 s tras publicar el simulador — Evidencia: docs/pm/evidencia/WP-5.1/indicadores.mp4
  - CA-5.1.5 [S]: con el backend detenido el tablero muestra "sin conexión" y no presenta datos viejos como actuales — Evidencia: docs/pm/evidencia/WP-5.1/sin_conexion.png

### WP-5.2 — Tablero: control y gestión logística
- Riesgo: medio
- Tipo: entregable
- Entregable: endpoints de órdenes y de registro de tarimas, y los módulos Control y Gestión logística del tablero
- Alcance de archivos: ui/src/control/**, ui/src/logistica/**, backend/koleo/ordenes.py, backend/koleo/api.py, docs/pm/evidencia/WP-5.2/**
- Interfaz: `POST /api/ordenes` (`{tipo, ruta?, id_tarima?}` → 202 `{id_orden}`, publica con el `publicador` inyectado en `crear_app`); `GET /api/ordenes/<id>`; `POST /api/tarimas` (`{id_tarima, peso_kg, descripcion}`)
- Trazabilidad: REQ-F-013, REQ-F-014
- Dependencias: WP-1.3, WP-5.1
- Criterios de aceptación:
  - CA-5.2.1 [S]: `POST /api/ordenes` con INICIAR válido responde 202, publica en `koleo/robot1/orden` un mensaje válido contra el esquema y deja la orden "pendiente" — Evidencia: tests/aceptacion/test_wp_5_2.py
  - CA-5.2.2 [S]: INICIAR sin `id_tarima` o sin `ruta` responde 400 y no publica — Evidencia: tests/aceptacion/test_wp_5_2.py
  - CA-5.2.3 [S]: un `orden_ack` recibido actualiza el estado de la orden a "aceptada" o "rechazada" — Evidencia: tests/aceptacion/test_wp_5_2.py
  - CA-5.2.4 [S]: `POST /api/tarimas` con TAR-104 y 5.0 kg crea la tarima EN_PISO; con peso 0 o id "ABC" responde 400 — Evidencia: tests/aceptacion/test_wp_5_2.py
  - CA-5.2.5 [S]: el tablero tiene botones INICIAR, CANCELAR y PARO y un formulario de registro, y refleja el ack — Evidencia: docs/pm/evidencia/WP-5.2/control.png

### WP-6.1 — Pruebas de elevación, rechazo, obstáculo y latencia
- Riesgo: alto
- Tipo: integracion
- Entregable: resultados medidos de VAL-01, VAL-02, VAL-05 y VAL-07 con evidencia
- Alcance de archivos: docs/pm/evidencia/hw/WP-6.1/**
- Interfaz: ninguna (físico)
- Trazabilidad: REQ-F-001, REQ-F-002, REQ-F-004, REQ-NF-002, REQ-NF-003
- Dependencias: WP-2.2, WP-2.4, WP-3.1, WP-3.3, WP-4.1
- Criterios de aceptación:
  - CA-6.1.1 [D]: VAL-01: una masa calibrada de 10 kg sube en menos de 15 s, cronometrado en video — Evidencia: docs/pm/evidencia/hw/WP-6.1/val01.mp4
  - CA-6.1.2 [S]: VAL-02: una masa de 11.8 kg no sube y quedan el evento SOBREPESO y la fila en la BD — Evidencia: docs/pm/evidencia/hw/WP-6.1/val02.mp4 y docs/pm/evidencia/hw/WP-6.1/val02_consulta.txt
  - CA-6.1.3 [S]: VAL-05: con el robot avanzando, una caja a 15 cm detiene los motores y se publica el evento — Evidencia: docs/pm/evidencia/hw/WP-6.1/val05.mp4 y docs/pm/evidencia/hw/WP-6.1/val05_log.txt
  - CA-6.1.4 [S]: VAL-07: la latencia desde que la celda detecta la tarima suelta hasta la fila en la BD es < 2 s, con `ts` de ambos lados, en 5 repeticiones — Evidencia: docs/pm/evidencia/hw/WP-6.1/val07.md

### WP-6.2 — Pruebas de rutas, llegada y traslado sostenido
- Riesgo: alto
- Tipo: integracion
- Entregable: resultados medidos de VAL-03, VAL-04 y VAL-06 con evidencia
- Alcance de archivos: docs/pm/evidencia/hw/WP-6.2/**
- Interfaz: ninguna (físico)
- Trazabilidad: REQ-F-006, REQ-NF-001, REQ-NF-004
- Dependencias: WP-4.3, WP-4.2, WP-6.1
- Criterios de aceptación:
  - CA-6.2.1 [S]: VAL-03: RUTA_1, RUTA_2 y RUTA_3 se completan sin colisión — Evidencia: docs/pm/evidencia/hw/WP-6.2/val03_ruta1.mp4, docs/pm/evidencia/hw/WP-6.2/val03_ruta2.mp4 y docs/pm/evidencia/hw/WP-6.2/val03_ruta3.mp4
  - CA-6.2.2 [D]: VAL-04: el error final es < 10 cm medido con cinta en cada ruta — Evidencia: docs/pm/evidencia/hw/WP-6.2/val04.md
  - CA-6.2.3 [S]: VAL-06: traslado de 3 min sin reinicio ni corte de energía — Evidencia: docs/pm/evidencia/hw/WP-6.2/val06.mp4

### WP-6.3 — Ensayo general y reporte
- Riesgo: medio
- Tipo: integracion
- Entregable: demo completa grabada, reporte con evidencia de VAL-01 a VAL-08 y cierre del proyecto
- Alcance de archivos: docs/pm/evidencia/hw/WP-6.3/**, docs/reporte/**
- Interfaz: ninguna
- Trazabilidad: REQ-NF-006, REQ-NF-007, REQ-NF-008
- Dependencias: WP-5.2, WP-6.1, WP-6.2
- Criterios de aceptación:
  - CA-6.3.1 [S]: existe una demo completa grabada el 30-nov o el 1-dic — Evidencia: docs/pm/evidencia/hw/WP-6.3/demo_completa.mp4
  - CA-6.3.2 [S]: el reporte presenta VAL-01 a VAL-08 cada una con su resultado medido y su evidencia enlazada; si una meta no se alcanzó, se reporta la medición real — Evidencia: inspección de docs/reporte/reporte_final.md
  - CA-6.3.3 [S]: el reporte lista los sensores y actuadores de cada integrante (Etapa 2) y el gasto total en MXN (≤ 10,000) — Evidencia: inspección de docs/reporte/reporte_final.md
  - CA-6.3.4 [S]: la bitácora del robot enlazada incluye fecha, cambios y resultados de las sesiones de integración — Evidencia: docs/pm/evidencia/hw/WP-6.3/bitacora.md
