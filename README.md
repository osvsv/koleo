# KOLEO — Organización automática de tarimas en almacenes

Robot móvil semiautónomo a escala (~30 × 30 cm) que se mete debajo de una tarima, la levanta con un actuador lineal, la lleva a su destino y registra el movimiento en una base de datos. El nombre viene de los escarabajos (*Coleoptera*), que se deslizan por debajo de las cargas.

Proyecto de la materia **Implementación de Internet de las Cosas (Gpo. 501)**, Tecnológico de Monterrey, Campus Guadalajara, agosto–diciembre 2026.

**Equipo:** Miranda Henry · Álvaro Alcaraz · Osvaldo Sierra · Elías Tamez · Leonardo Alfonzo

**Entrega final:** 2 de diciembre de 2026 (tentativa)

---

## Empieza aquí

La planeación oficial es la **línea base en [`docs/pm/`](docs/pm/)**. Si algo de otro documento la contradice, manda `docs/pm/`.

| Documento | Para qué sirve |
|---|---|
| [Estado del proyecto](docs/pm/estado.md) | Qué paquetes de trabajo están terminados, en corrección o pendientes. Es un archivo generado: no se edita a mano |
| [Charter](docs/pm/01-charter.md) | Propósito, objetivos medibles (OBJ-01 a OBJ-06), alcance, lo que queda fuera y criterios de cierre |
| [Requisitos](docs/pm/02-requisitos.md) | Requisitos funcionales y no funcionales con ejemplos |
| [WBS](docs/pm/03-wbs.md) | Los paquetes de trabajo (WP-1.1 a WP-6.3), sus criterios de aceptación y su evidencia |
| [Riesgos](docs/pm/05-riesgos.md) · [Supuestos](docs/pm/supuestos.md) | Riesgos y supuestos vigentes |
| [Cambios](docs/pm/cambios.md) | Solicitudes de cambio aprobadas (CC-001 en adelante): qué cambió y por qué |
| [Bloqueos](docs/pm/bloqueos.md) · [Desviaciones](docs/pm/desviaciones.md) | Lo que está detenido y por qué |

### Cambios recientes que hay que conocer

- **CC-004 (13-nov):** salen del proyecto la celda de carga con HX711 y el VL53L1X por falla de hardware. El rechazo por sobrepeso (más de 10 kg) se hace con el **peso declarado** de la tarima, que se registra en el tablero. En las demos la carga física es de **100 g**.
- El ESP32 y la Raspberry Pi hablan **por MQTT**, con el broker en la Pi; no hay cable de datos entre ellos.
- El trabajo se reparte **por paquetes de trabajo**, no por dueños de subsistema (SUP-016).
- RPLIDAR y Google Coral quedan fuera de alcance.

## Cómo trabajamos

El proyecto se gestiona con el **Método PM** (ver [`CLAUDE.md`](CLAUDE.md)):

- Se trabaja solo sobre paquetes de la [WBS](docs/pm/03-wbs.md).
- Nada está terminado sin dictamen **CONFORME** del auditor y evidencia en [`docs/pm/evidencia/`](docs/pm/evidencia/).
- La línea base solo cambia con una solicitud de cambio (se registra en [`cambios.md`](docs/pm/cambios.md)).
- Los paquetes físicos (tipo `integracion`: chasis, elevación, energía, sensores y pruebas en piso) los hacen personas, y su evidencia (fotos, videos, mediciones) va a `docs/pm/evidencia/hw/<WP>/`.
- Las credenciales (Wi-Fi, MQTT) van en variables de entorno, nunca en el repositorio.

---

## Arquitectura

```
 ESP32 (motores, actuador, HC-SR04, encoders) ──┐
                                                ├──▶ Broker MQTT ──▶ Backend (Flask) ──▶ SQLite
 Raspberry Pi 5 (A*, lectura QR, puente MQTT) ──┘   (en la Pi)              │
                                                                            ▼
                                                              Web API ──▶ Tablero (React)
```

| Subsistema | Tecnología | Carpeta |
|---|---|---|
| Contratos | Temas MQTT, comandos del ESP32, estados y esquema SQL | [`contratos/`](contratos/) |
| Firmware | ESP32 (PlatformIO): tracción diferencial, actuador lineal, HC-SR04, encoders | [`firmware/esp32/`](firmware/esp32/) |
| Raspberry Pi | Raspberry Pi 5: lectura QR; planificador A\* y puente MQTT según la WBS | [`pi/`](pi/) |
| Simulador | Robot falso que publica el mismo MQTT que el real | [`simulador/`](simulador/) |
| Backend | Python + Flask: MQTT → SQLite → Web API | [`backend/`](backend/) |
| Tablero | React + Vite + Tailwind | [`ui/`](ui/) |
| Pruebas | Suite de aceptación por paquete de trabajo (pytest) | [`tests/aceptacion/`](tests/aceptacion/) |

## Cómo correr las pruebas

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt       # en Windows: .venv\Scripts\pip.exe
.venv/bin/python -m pytest tests/aceptacion -q
```

Tablero:

```bash
cd ui
npm install
npm run dev
```

---

## Otros documentos

| Documento | Qué contiene |
|---|---|
| [Documento de frontend](docs/frontend.md) | Propuesta de diseño del tablero (11-nov): pantallas, flujos, modelo de datos y sistema visual. Donde difiera, manda la WBS |
| [Wireframes](docs/wireframes/README.md) | Monitoreo, Control y Tarimas con el estilo visual Visitors (imagen + HTML) |
| [Documentación previa](docs/pm/importado/) | Lo que había antes de la línea base: [documentación general](docs/pm/importado/KOLEO_Documentacion_General.md), [documento completo al 11-nov](docs/pm/importado/KOLEO_todo.md) (BOM, pinout, armado), [propuesta de metodología](docs/pm/importado/KOLEO_Metodologia_y_plan.md) y [diagnóstico](docs/pm/importado/diagnostico.md) |
| [Presentación de avance (21-oct)](docs/fuentes/KOLEO_Organizacion_Automatica_Almacenes.md) | Las 32 diapositivas en Markdown |

La documentación previa y la propuesta de frontend son históricas: sirven de contexto, pero algunas cosas ya cambiaron (por ejemplo, la celda de carga y el VL53L1X ya no están).

## Estructura del repositorio

```
.
├── README.md         ← estás aquí
├── CLAUDE.md         reglas del Método PM
├── contratos/        MQTT, comandos del ESP32, estados, esquema SQL
├── firmware/esp32/   firmware del ESP32 (PlatformIO)
├── pi/               software de la Raspberry Pi
├── simulador/        robot falso
├── backend/          ingesta MQTT, SQLite y Web API
├── ui/               tablero web
├── tests/aceptacion/ pruebas de aceptación por WP
└── docs/
    ├── pm/           línea base, estado, evidencia, auditorías
    ├── frontend.md   propuesta de diseño del tablero
    ├── wireframes/   pantallas (PNG + HTML)
    └── fuentes/      presentación original
```
