# KOLEO — Organización automática de tarimas en almacenes

Robot autónomo a escala (~30 × 30 cm) que se mete debajo de una tarima, la levanta con un actuador lineal (carga máxima de diseño: **10 kg**), la lleva a su destino y registra el movimiento en una base de datos por Wi-Fi. El nombre viene de los escarabajos (*Coleoptera*), que se deslizan por debajo de las cargas.

Proyecto de la materia **Implementación de Internet de las Cosas (Gpo. 501)**, Tecnológico de Monterrey, Campus Guadalajara, agosto–diciembre 2026.

**Equipo:** Miranda Henry · Álvaro Alcaraz · Osvaldo Sierra · Elías Tamez · Leonardo Alfonzo

**Entrega final:** 2 de diciembre de 2026

> Por ahora este repositorio solo contiene la **planeación y documentación**. El código (firmware, Raspberry Pi, backend y frontend) se irá agregando conforme avance el plan.

---

## Arquitectura en una imagen

```
 Raspberry Pi 5 ──UART──▶ ESP32 ──Wi-Fi──▶ Broker MQTT ──▶ Backend (Web API) ──▶ SQLite
 cámara (QR), rutas A*     motores, actuador,                 │
                           celda de carga, sensores           └──▶ Interfaz web (React) vía MQTT sobre WebSocket
```

| Subsistema | Tecnología |
|---|---|
| Mecánica | Chasis ~300 × 300 mm, actuador lineal 12 V |
| Firmware | ESP32: 2 motores DC con encoder (L298N), actuador (BTS7960), HX711 + celda 20 kg, HC-SR04, VL53L1X |
| Navegación | Raspberry Pi 5 + Camera Module 3 (lectura de QR), planeación A\* sobre cuadrícula |
| Comunicación | MQTT (temas `koleo/robot1/...`) |
| Datos | SQLite: `tarimas`, `historial_movimientos`, `registro_rechazos_seguridad` |
| Interfaz | React + Vite + TypeScript + Tailwind, estilo visual *Visitors* (Refero) |

---

## Documentación

Empieza por la **metodología**: dice quién hace qué y en qué orden.

| Documento | Qué contiene |
|---|---|
| [Metodología y plan de trabajo](docs/metodologia.md) | Cómo trabajamos (Kanban semanal), dueños por subsistema, contratos MQTT/SQL, robot falso, tareas T01–T24 y puertas de validación por semana |
| [Documento de frontend](docs/frontend.md) | Requisitos RF-01..RF-15, pantallas, flujos, modelo de datos, arquitectura de la UI y sistema visual |
| [Wireframes](docs/wireframes/README.md) | Pantallas de Monitoreo, Control y Tarimas (imagen + HTML) |
| [Documentación general del proyecto](pm/importado/KOLEO_Documentacion_General.md) | Especificación técnica completa: arquitectura, sensores, ciclo operativo, seguridad, brechas técnicas, plan de integración y pruebas VAL-01..08 |
| [Documento completo (estado al 11-nov)](pm/importado/KOLEO_todo.md) | Componentes finales, compras, pinout del ESP32, armado en banco, configuración de la Raspberry Pi, código de prueba y pendientes |
| [Presentación de avance (21-oct)](docs/fuentes/KOLEO_Organizacion_Automatica_Almacenes.md) | Contenido de las 32 diapositivas en Markdown |

Las versiones vivas (editables, con comentarios) de la metodología, el frontend y los wireframes están en Claude; los archivos de este repo son una copia al **13 de noviembre de 2026**. Si cambias algo importante, actualiza también la copia aquí.

---

## Estructura del repositorio

```
.
├── README.md                 ← estás aquí
├── docs/
│   ├── metodologia.md        plan de trabajo y tareas
│   ├── frontend.md           diseño de la interfaz
│   ├── wireframes/           pantallas (PNG + HTML)
│   └── fuentes/              presentación original convertida
└── pm/importado/             documentación previa del equipo
```

Cuando empiece el código, la idea es agregar carpetas por subsistema (por ejemplo `firmware/`, `raspberry/`, `backend/`, `frontend/`, `simulador/`).

## Cómo contribuir

1. Trabaja en una rama propia (`git checkout -b tu-nombre/tarea-T07`).
2. Usa el ID de la tarea (T01–T24) en el nombre de la rama y en el mensaje del commit.
3. Abre un Pull Request hacia `main` y pide revisión a alguien del equipo.
