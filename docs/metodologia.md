# KOLEO — Metodología y plan de trabajo

> **Copia pendiente.** La versión completa vive en Claude: https://claude.ai/artifact/6LwjXnLGYn41icZTZ9ti3G . Este archivo se reemplazará con el documento completo en cuanto se pueda exportar. Mientras tanto, este es el resumen.

## Cómo trabajamos

- **Kanban con ciclos de una semana:** planeación el lunes, check-in diario por chat, **sesión de integración con el robot a media semana**, demo y retro el viernes.
- **WIP de 2 tareas por persona.** Cada tarea dura de 2 a 6 horas, tiene un resultado verificable, una prueba, sus dependencias y **un solo dueño**.
- **Contratos primero:** antes de programar se fijan los mensajes MQTT, los estados y el esquema SQL.
  - Temas MQTT: `koleo/robot1/telemetria`, `koleo/robot1/evento`, `koleo/robot1/orden`, `koleo/robot1/orden/ack`, `koleo/robot1/conexion`.
  - Estados del sistema unificados (hoy `EN_PISO` y `UBICADA_DESTINO` viven en módulos distintos).
  - Esquema SQL con los nombres del diagrama E-R: `tarimas`, `historial_movimientos`, `registro_rechazos_seguridad`.
- **Robot falso en Python** que publica el mismo MQTT que el robot real, para que backend e interfaz avancen sin hardware.
- **Puertas semanales:** cada semana cierra cuando ciertas pruebas VAL (VAL-01..08, ver la documentación general) están aprobadas.

## Dueños propuestos

| Subsistema | Dueño |
|---|---|
| Mecánica | Álvaro |
| Electrónica y alimentación | Miranda |
| Firmware ESP32 | Leo |
| Raspberry Pi y navegación | Elías |
| Contratos MQTT, backend, SQLite e interfaz | Osvaldo |

## Calendario

| Semana | Fechas | Objetivo |
|---|---|---|
| 1 | 11–17 nov | Esqueleto: contratos, robot falso, piezas básicas funcionando |
| 2 | 18–24 nov | Robot real conectado y seguridad (sobrepeso, paro por proximidad) |
| 3 | 25 nov–1 dic | Navegación, interfaz completa y validación |
| Entrega | 2 dic | Demostración final |

El plan tiene 24 tareas (T01–T24) repartidas en estas semanas; el detalle está en el documento completo.

**Fuera de alcance:** RPLIDAR y Google Coral, porque ninguna prueba VAL los necesita.
