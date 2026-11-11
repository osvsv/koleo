# KOLEO — Documento completo del proyecto

> Recopilación de todo lo trabajado en el proyecto KOLEO hasta el **11 de noviembre de 2026**: contexto, requisitos, componentes, compras, pinout, armado, configuración de la Raspberry Pi, código, base de datos, presentación, factibilidad y pendientes.

---

## Índice

1. [Qué es KOLEO](#1-qué-es-koleo)
2. [Equipo y curso](#2-equipo-y-curso)
3. [Requisitos del Reto IoT](#3-requisitos-del-reto-iot)
4. [Metas, criterios, hitos y presupuesto](#4-metas-criterios-hitos-y-presupuesto)
5. [Arquitectura del sistema](#5-arquitectura-del-sistema)
6. [Componentes finales](#6-componentes-finales)
7. [Historial de decisiones de componentes](#7-historial-de-decisiones-de-componentes)
8. [Compras de energía](#8-compras-de-energía)
9. [Pinout del ESP32](#9-pinout-del-esp32)
10. [Armado en banco (sin base)](#10-armado-en-banco-sin-base)
11. [Raspberry Pi 5: SSD y configuración](#11-raspberry-pi-5-ssd-y-configuración)
12. [Orden de encendido y pruebas](#12-orden-de-encendido-y-pruebas)
13. [Código de prueba de sensores (ESP32)](#13-código-de-prueba-de-sensores-esp32)
14. [Solución de problemas](#14-solución-de-problemas)
15. [Software: firmware, Raspberry Pi y base de datos](#15-software-firmware-raspberry-pi-y-base-de-datos)
16. [Presentación](#16-presentación)
17. [Análisis de factibilidad](#17-análisis-de-factibilidad)
18. [Pendientes](#18-pendientes)
19. [Referencias](#19-referencias)

**Anexos**

- [A. Firmware original del ESP32 (código completo)](#anexo-a-firmware-original-del-esp32)
- [B. Script de la Raspberry Pi 5 (QR, A\* y misión)](#anexo-b-script-de-la-raspberry-pi-5)
- [C. Demo de la base de datos (código)](#anexo-c-demo-de-la-base-de-datos)
- [D. Preguntas probables del profesor y cómo responder](#anexo-d-preguntas-probables-y-cómo-responder)
- [E. Historial de versiones del armado](#anexo-e-historial-de-versiones-del-armado)
- [F. Cálculos de factibilidad a detalle](#anexo-f-cálculos-de-factibilidad-a-detalle)
- [G. Comandos y valores de referencia rápida](#anexo-g-referencia-rápida)
- [H. Línea de tiempo del proyecto](#anexo-h-línea-de-tiempo-del-proyecto)

---

## 1. Qué es KOLEO

Robot autónomo a escala (~300 × 300 mm) que:

1. Se mete debajo de una tarima.
2. La levanta con un actuador lineal de 12 V (carga máxima de diseño: **10 kg**).
3. La transporta a su destino.
4. Actualiza la posición de la tarima en una base de datos vía Wi-Fi.

**Nombre:** referencia a los escarabajos (orden *Coleoptera*), que se deslizan por debajo de las cargas.

**Problema:** organización automática de tarimas en almacenes.

---

## 2. Equipo y curso

- **Curso:** Implementación de Internet de las Cosas (Gpo 501), Tec de Monterrey campus Guadalajara, agosto–diciembre 2026.
- **Integrantes:** Miranda Henry, Elías Tamez, Leonardo Alfonzo, Alvaro Alcaraz, Osvaldo Sierra.
- **Roles:** mecánica · hardware/electrónica · control/navegación · software/IoT · integración/documentación.

**Fuentes originales del proyecto:** Project Charter y WBS (10-oct-2026), presentación "Organización automática en almacenes" (avance), descripción del Reto IoT del Tec y una conversación previa con Gemini (BOM, pinout, script CAD, SQL, firmware ESP32, script RPi 5, demo SQLite).

---

## 3. Requisitos del Reto IoT

Lo que pide el profesor:

- **Al menos 2 sensores y 2 actuadores** por equipo.
- **Microcontroladores en red** (MQTT o HTTP).
- **Base de datos** con lectura/escritura en tiempo real + **Web API**.
- **Visualización en tiempo real** de al menos **5 indicadores**.
- **Etapa 2:** cada alumno conecta y programa "su" sensor y "su" actuador (5 alumnos).

**Etapas del reto:**

| Etapa | Contenido |
|---|---|
| 1 | Definición |
| 2 | Sensores / actuadores |
| 3 | Base de datos + Web API |
| 4 | Análisis / indicadores |
| 5 | Pruebas y presentación |

---

## 4. Metas, criterios, hitos y presupuesto

### Metas medibles

| Área | Criterio |
|---|---|
| Mecánica | Levantar 10 kg en **< 10 s**; transportarlos **≥ 3 min** sin fallas |
| Navegación | Llegar al destino con error **< 5 cm**, sin colisiones; **3 rutas autónomas** distintas |
| IoT | Latencia desde que se deja la tarima hasta la actualización en la BD **< 2 s**; la BD muestra ID, coordenada nueva y fecha |

### Hitos

| Semana | Hito |
|---|---|
| 3 | H1 — Prueba de banco con 10 kg |
| 6 | H2 y H3 — Tres rutas + latencia de BD; integración |
| 7 | Cierre |

### Cronograma por semana (basado en la WBS del Charter)

| Semana | Estado (al 21-oct) | Actividades | Hito |
|---|---|---|---|
| 1 | Completada | Charter y requisitos · CAD del chasis y la elevación | |
| 2 | Completada | Componentes verificados · Pinout y alimentación · Estructura de la base de datos | |
| 3 | En curso | Ensamble del chasis y la elevación · Tracción, celda y sensores · Prueba de banco de 10 kg | **Hito 1** |
| 4 | Pendiente | Control de motores y sensores · Web API y registro de tarimas · Transporte de 3 minutos | |
| 5 | Pendiente | Mapeo y planeación de rutas · Evasión de obstáculos | |
| 6 | Pendiente | Tres rutas autónomas · Latencia menor a 2 s · Integración completa | **Hitos 2 y 3** |
| 7 | Pendiente | Correcciones y pruebas finales · Documentación · Demostración final | |

> El ensamble del chasis se pasó de la semana 2 a la 3 porque aún no estaba armado. Al 11-nov el armado sigue en banco (sin chasis).

### Presupuesto

- **$8,000 MXN** (±25 %, tope **$10,000 MXN**).
- La lista ampliada de octubre (con drivers, reguladores, batería y paro) sumaba **~$9,900 MXN**, a $100 del tope y sin margen para repuestos.
- Decisión: **no agregar piezas nuevas**; la lista se recortó al mínimo (en noviembre se quitaron paro, alarma, fusible, LM2596, microSD y regletas).

---

## 5. Arquitectura del sistema

```
 ┌──────────────────────────┐        UART (3 cables)        ┌──────────────────────────┐
 │     Raspberry Pi 5        │ ───────────────────────────▶ │          ESP32            │
 │ • Camera Module 3 (QR)    │   comandos: LIFT/MOVE/STOP/   │ • 2 motores DC + encoder  │
 │ • RPLIDAR A1              │            DROP               │   (L298N)                 │
 │ • Planeación de rutas A*  │                               │ • Actuador lineal (BTS7960)│
 │ • SSD M.2 (PCIe)          │                               │ • HX711 + celda 20 kg     │
 └──────────────────────────┘                               │ • HC-SR04 • VL53L1X        │
                                                            └─────────────┬────────────┘
                                                                          │ Wi-Fi · HTTP POST
                                                                          ▼
                                                   /api/actualizar_tarima (Web API · Flask)
                                                                          │ SQL
                                                                          ▼
                                                     Base de datos SQL (SQLite en la demo)
                                                     tarimas · historial_movimientos ·
                                                     registro_rechazos_seguridad
```

- **Raspberry Pi 5:** cámara (lee el QR de cada tarima), RPLIDAR A1, planeación de rutas (A\*). Envía comandos por UART al ESP32.
- **ESP32:** motores DC con encoder (L298N), actuador lineal (BTS7960), HX711 + celda, HC-SR04, VL53L1X. Publica a la BD por HTTP.
- **Base de datos:** SQL relacional, tres tablas unidas por `id_tarima`.

---

## 6. Componentes finales

Lista final al **11-nov-2026**:

| Grupo | Pieza | Nota |
|---|---|---|
| Control | ESP32 ESP-32S NodeMCU de 38 pines | En protoboard de 830 puntos, filas 2–20, USB hacia arriba |
| Control | Raspberry Pi 5 + Active Cooler + SSD M.2 directo en la Pi (PCIe) | Arranca del SSD, sin microSD |
| Control | Protoboard y jumpers (macho-macho y macho-hembra) | |
| Drivers | L298N | Los dos motores |
| Drivers | BTS7960 (IBT-2) | El actuador |
| Actuadores | 2× motor GA25-370, 12 V, 130 RPM, con encoder | Cable de 6 hilos cada uno; reductora 46.8:1 |
| Actuadores | Actuador lineal 12 V, 75 kg, 50 mm de carrera | Trae finales de carrera internos |
| Sensores | Celda de carga de 20 kg + HX711 | Pesa la tarima |
| Sensores | VL53L1X (ToF) | Distancia por I2C |
| Sensores | HC-SR04 + resistencias de 1 kΩ y 2 kΩ | El divisor baja el Echo a 3.3 V |
| Sensores | RPLIDAR A1 + adaptador USB | Va a la Pi |
| Sensores | Camera Module 3 + cable de 22 a 15 pines | Va a la Pi |
| Energía | LiPo OVONIC 3S 2200 mAh 25C, conector T (paquete de 2) | La segunda es repuesto |
| Energía | Cargador balanceador 3S | Carga por el conector JST-XH |
| Energía | Conectores T con cable 14 AWG | Justo después de la batería |
| Energía | Buck 12 → 5.1 V, 5 A, salida USB-C | Alimenta la Pi |
| Mecánica | 2 ruedas de 65 mm, eje de 4 mm + ruedas locas | |
| Cables | Micro-USB del ESP32 a la Pi | Alimenta y permite programar el ESP32 |
| Cables | Cable 16 AWG rojo y negro, cinta para etiquetar | Para los 12 V |

**Quitados por decisión del equipo (11-nov):** paro de emergencia, alarma de LiPo, fusible, LM2596, microSD, regletas/WAGO.

**Candidatos a quitar (solo uno de los dos):** HC-SR04 o RPLIDAR.

### Mecánica planeada para el chasis (aún sin construir)

- 2 placas de 300 × 300 mm (aluminio de 3 mm, o acrílico/MDF de 6 mm): base y placa superior con hueco al centro para el actuador.
- 6 postes separadores M3 de ~55 mm entre placas.
- Plataforma elevadora rígida de ~200 × 150 mm.
- 4 guías verticales: varilla de 8 mm con buje lineal LM8UU.
- Adaptador vástago–celda (impreso en 3D o de aluminio) y 2 separadores de 3–5 mm para la celda.
- 2 soportes para motor GA25, tornillería M3 y M4 (revisar la rosca de la celda).
- Cadena de elevación: **actuador → adaptador → celda → plataforma**.

---

## 7. Historial de decisiones de componentes

| Decisión | Motivo |
|---|---|
| **Celda de 20 kg** en lugar de 10 kg | Tarima de 10 kg + plataforma + golpes al levantar dejan la de 10 kg en el límite |
| **VL53L1X** en lugar del VL53L5CX | El VL53L5CX casi no se consigue en México (solo DigiKey, US$17–31 + envío) y el código no usaba sus 8×8 zonas |
| **Un solo actuador** (no dos) | 75 kg ≈ 735 N levanta ~7 veces la tarima; dos actuadores DC no van sincronizados, se ladea la plataforma, doble consumo y costo |
| **Guías verticales** obligatorias | Los soportes con perno dejan pivotear al actuador; las guías absorben el ladeo |
| **Actuador de 50 mm** | Recogido mide ~15 cm entre barrenos; hay que sumar soportes, celda (~1.3 cm), separadores y plataforma dentro de ~19 cm de altura del robot. Si no cabe, bajar la base del actuador por debajo de la placa del chasis |
| **GA25-370 12 V 130 RPM con encoder** | Motores DC con reductora y encoder magnético (efecto Hall) |
| **LiPo 3S 2200 mAh con conector T** (en lugar de 5000 mAh con XT60) | Precio y disponibilidad; 3S es obligatorio (una 2S de 7.4 V no mueve bien los motores de 12 V) |
| **Pilas 23A / 27A: NO sirven** | Son pilas de control remoto (~20–55 mAh); el robot pide 4–5 A |
| **Eliminador de 12 V y ≥ 3 A** para pruebas de mesa | No se descarga y es seguro; con 3 A se prueba por partes (motores **o** actuador) |
| **ESP32 por micro-USB desde la Pi** (adiós LM2596) | Nunca recibe energía por dos lados y el pin 5V queda libre para el HC-SR04 |
| **SSD directo en la Pi por PCIe** | Más rápido que USB y aguanta mejor la vibración |
| **Sin fusible, paro ni alarma** | Simplificación decidida por el equipo; se compensa con stop por software y desconectando el conector T |

### Duración de la batería según capacidad (consumo de 4–5 A)

| Capacidad | Duración aprox. |
|---|---|
| 5000 mAh | ~60 min |
| 3000 mAh | ~35–40 min |
| 2200 mAh | ~25 min (estimación conservadora) |

> El análisis de factibilidad del 11-nov da para la de 2200 mAh (24 Wh) unos **50 min manejando** y **~30 min en el peor caso**.

**Capacidad de descarga (C):** lo que entrega la batería es capacidad × C. 2200 mAh × 20C = 44 A (sobra); 1000 mAh × 20C = 20 A (alcanza pero dura poco).

**Eliminador o fuente de menos de 5 A:** con 3 A se prueban los motores **o** el actuador; con todo encendido a la vez se cae el voltaje y el ESP32 o la Pi se reinician. Para el robot completo, 5 A o más.

**Batería de plomo-ácido 12 V 4.5/7 Ah** (de alarma o no-break): funciona y es recargable, pero pesa más de 1 kg y necesita su propio cargador.

### Cotizaciones encontradas (7-nov)

| Pieza | Dónde | Precio aprox. |
|---|---|---|
| Kit celda de carga (1/5/10 kg) + HX711 | UNIT Electronics (uelectronics.com), envío desde CDMX | $61–73 MXN (también hay de 20 kg) |
| VL53L5CX breakout (VL53L5CX-SATEL) | DigiKey México | US$17–31 + envío |
| VL53L0X (alternativa de un punto) | Mercado Libre | desde ~$82 MXN |
| Actuador lineal 12 V, 50 mm, 75 kg (735 N) | Mercado Libre | ~$537 MXN, envío gratis |
| Actuador lineal 12 V, 50 mm, 150 kg | Mercado Libre | ~$498 MXN |

**Criterio para el actuador:** 10 kg ≈ 100 N, así que mínimo **300 N**. Los "micro" de 20–64 N no levantan la tarima. Revisar la **longitud cerrada** en la ficha.

**Criterio para el driver de tracción:** se prefirió el **L298N** sobre el TB6612FNG porque aguanta mejor los picos de corriente con 10 kg encima.

---

## 8. Compras de energía

| Producto | Precio | Notas |
|---|---|---|
| [Baterías OVONIC 3S 2200 mAh 25C, paquete de 2](https://www.amazon.com.mx/gp/product/B08CZ4NQ7K) | $590.06 | 11.1 V, hasta 55 A, conector T + balanceo JST-XH, 105 × 33 × 20 mm, 144 g c/u |
| [Conectores T Hobbypark, 4 pares 14 AWG](https://www.amazon.com.mx/gp/product/B08HJXHJKS) | $155.60 | 4 machos + 4 hembras con cable, 2 correas; 25 A continuos |
| [Cargador balanceador Tosiicop](https://www.amazon.com.mx/dp/B0FS23G6KD) | $478.00 | Carga por el conector blanco JST-XH |
| **Total** | **$1,223.66** | |

Las baterías llegan con media carga: solo alcanzan para una prueba corta antes de cargarlas.

---

## 9. Pinout del ESP32

ESP-32S NodeMCU en protoboard, **filas 2–20, USB hacia arriba**; hoyos libres en las columnas **A** (izquierda) y **J** (derecha).

| Función | GPIO |
|---|---|
| HX711 DT / SCK | 4 / 5 |
| BTS7960 RPWM (sube) / LPWM (baja) | 25 / 26 |
| L298N motor izquierdo: ENA / IN1 / IN2 | 32 / 33 / 27 |
| L298N motor derecho: ENB / IN3 / IN4 | 14 / 23 / 13 |
| Encoder izquierdo A / B | 34 / 36 |
| Encoder derecho A / B | 35 / 39 |
| VL53L1X SDA / SCL | 21 / 22 |
| HC-SR04 TRIG / ECHO | 18 / 19 (ECHO por divisor 1 kΩ/2 kΩ) |
| UART con la Pi: RX2 ← pin 8 de la Pi | 16 |
| UART con la Pi: TX2 → pin 10 de la Pi | 17 |
| GND común con la Pi ← pin 6 de la Pi | GND (riel −) |

**Notas importantes del pinout**
- El **GPIO 12** es pin de arranque (strapping): no se usa.
- Los **GPIO 34–39** son solo de entrada y **no tienen pull-up interno**.
- **GPIO 14** debe ponerse en LOW al inicio del programa.
- Filas 3–5 (SD0–SD3, GPIO 15 y un GND de la flash): no conectar nada.

---

## 10. Armado en banco (sin base)

Documento completo con render 3D, diagrama de conexiones y vista de la protoboard: **["KOLEO — Armado final completo (sin base)"](https://claude.ai/artifact/2pCsPp8ojY1xXew9tZ5QT2)** (rev. 28, 11-nov).

### 10.1 Vista general

Todo queda en la mesa: la LiPo alimenta directo la Pi, los motores y el actuador, sin fusible ni paro de emergencia. La Raspberry Pi 5 le manda órdenes al ESP32 por UART y el ESP32 mueve los motores y el actuador.

**Código de colores del diagrama**
- **Rojo grueso:** 12 V de la LiPo. **Negro:** GND.
- **Naranja:** 5 V. **Amarillo:** 3.3 V (en los cables de los motores, el amarillo es el canal A del encoder).
- **Gris:** cables USB. Los demás colores son señales, cada una con su GPIO.

### 10.2 Energía

Sin regletas: los empalmes van en los tornillos del BTS7960 y del L298N, **máximo dos cables por tornillo**.

| Paso | De | A | Cable |
|---|---|---|---|
| 1 | LiPo + (conector T) | B+ del BTS7960 | Rojo, 14 AWG |
| 2 | B+ del BTS7960 (segundo cable) | 12V del L298N | Rojo, 16 AWG |
| 3 | 12V del L298N (segundo cable) | IN+ del buck de la Pi | Rojo, 18 AWG |
| 4 | LiPo − (conector T) | B− del BTS7960 | Negro, 14 AWG |
| 5 | B− del BTS7960 (segundo cable) | GND del L298N | Negro, 16 AWG |
| 6 | GND del L298N (segundo cable) | IN− del buck de la Pi | Negro, 18 AWG |
| 7 | USB-C del buck | Raspberry Pi 5 | Cable USB-C |

**Reglas de seguridad sin fusible ni paro**
- **Detener motores y actuador:** orden de stop desde la Pi. El ESP32 también los apaga solo si hay PWM y los encoders no se mueven.
- **Cortar todo:** desconectar el conector T.
- Conectar el conector T **al final**, con todo revisado; aislar los tornillos de B+ y 12V; desconectar la batería antes de mover cualquier cable.
- Dos cables en un tornillo: torcer juntas las puntas, apretar y jalar cada cable para comprobar.
- **Apagar:** `sudo shutdown now` en la Pi → esperar a que el LED verde deje de parpadear → desconectar el conector T.
- **Batería:** medir con multímetro entre pruebas; cargar si en reposo baja de **~10.8 V**. No dejarla conectada al terminar.
- Cargar la LiPo solo con el cargador balanceador, sobre superficie que no se queme y sin dejarla sola.
- **Sin LiPo:** eliminador de 12 V y 3 A en su lugar (+ a B+, − a B− del BTS7960). Probar por partes; no mover motores y actuador con la Pi encendida.

### 10.3 Protoboard, hoyo por hoyo

Los dos rieles **+** son de **3.3 V** y los dos **−** son **GND**.

| Fila | Hoyo libre izquierdo (A) | Hoyo libre derecho (J) |
|---|---|---|
| 2 | CLK, no usar | 5V: VCC del HC-SR04 |
| 6 | 2, no usar | GPIO 13: L298N IN4 |
| 7 | 0, no usar | GND: riel − derecho |
| 8 | GPIO 4: HX711 DT | 12, no usar |
| 9 | GPIO 16 (RX2): pin 8 de la Pi | GPIO 14: L298N ENB |
| 10 | GPIO 17 (TX2): pin 10 de la Pi | GPIO 27: L298N IN2 |
| 11 | GPIO 5: HX711 SCK | GPIO 26: BTS7960 LPWM |
| 12 | GPIO 18: Trig del HC-SR04 | GPIO 25: BTS7960 RPWM |
| 13 | GPIO 19: puente a A44 | GPIO 33: L298N IN1 |
| 14 | GND, libre | GPIO 32: L298N ENA |
| 15 | GPIO 21: VL53L1X SDA | GPIO 35: encoder derecho A |
| 16 | RX0, no usar | GPIO 34: encoder izquierdo A |
| 17 | TX0, no usar | GPIO 39: encoder derecho B |
| 18 | GPIO 22: VL53L1X SCL | GPIO 36: encoder izquierdo B |
| 19 | GPIO 23: L298N IN3 | EN, no usar |
| 20 | GND: riel − izquierdo | 3V3: riel + derecho |

**Fuera del ESP32**
- **Fila 40:** el Echo del HC-SR04 entra en A40. Resistencia de **1 kΩ** de C40 a C44.
- **Fila 44:** puente desde A13 (GPIO 19) a A44. Resistencia de **2 kΩ** de B44 al riel − izquierdo.
- **Fila 62:** puente amarillo une riel + izquierdo y derecho.
- **Fila 63:** puente negro une riel − izquierdo y derecho.
- Si la protoboard tiene los rieles partidos a la mitad, unir las dos mitades con un puente.
- **Los 12 V nunca entran a la protoboard.**

### 10.4 Sensores al ESP32

| Sensor | Pin | Va a |
|---|---|---|
| HX711 | VCC / GND | Riel + izq / riel − izq |
| HX711 | DT / SCK | A8 (GPIO 4) / A11 (GPIO 5) |
| Celda → HX711 | Rojo / negro / blanco / verde | E+ / E− / A− / A+ |
| VL53L1X | VIN / GND | Riel + izq / riel − izq |
| VL53L1X | SDA / SCL | A15 (GPIO 21) / A18 (GPIO 22) |
| VL53L1X | XSHUT, GPIO1 | Sin conectar |
| HC-SR04 | VCC / GND | J2 (5V) / riel − izq |
| HC-SR04 | Trig / Echo | A12 (GPIO 18) / A40 (entrada del divisor) |
| Encoder izquierdo | Azul (VCC) / negro (GND) | Riel + der / riel − der |
| Encoder izquierdo | Amarillo (A) / verde (B) | J16 (GPIO 34) / J18 (GPIO 36) |
| Encoder derecho | Azul (VCC) / negro (GND) | Riel + der / riel − der |
| Encoder derecho | Amarillo (A) / verde (B) | J15 (GPIO 35) / J17 (GPIO 39) |

- Rojo y blanco del cable del motor son la potencia y van al L298N. Si los colores no coinciden, guiarse por lo impreso en la plaquita del encoder (M1, M2, VCC, GND, C1/A, C2/B).
- **Encoders a 3.3 V, nunca a 5 V ni 12 V.**
- **Nunca conectar el Echo directo al ESP32** (sale a 5 V; el GPIO aguanta máx. 3.6 V). Si no hay 1 kΩ/2 kΩ, sirve cualquier par donde la de abajo valga el doble (10k/20k, 2.2k/4.7k, 1k/1.8k). Alternativa: **HC-SR04P** o RCWL-1601, que funcionan a 3.3 V sin divisor.

### 10.5 Drivers y actuadores

**L298N**

| Terminal | Va a |
|---|---|
| ENA | J14 (GPIO 32) |
| IN1 | J13 (GPIO 33) |
| IN2 | J10 (GPIO 27) |
| IN3 | A19 (GPIO 23), lado izquierdo; el cable pasa por debajo del ESP32 |
| IN4 | J6 (GPIO 13) |
| ENB | J9 (GPIO 14) |
| OUT1 / OUT2 | Rojo / blanco del motor izquierdo |
| OUT3 / OUT4 | Rojo / blanco del motor derecho |
| 12V | B+ del BTS7960 |
| GND | B− del BTS7960; del mismo tornillo sale el cable al IN− del buck |
| 5V | Vacía |

Quitar los jumpers de ENA y ENB; dejar puesto el de 5V. El L298N pierde ~2 V, los motores reciben ~10 V (giran un poco más lento, es normal). Quitar el jumper del GND del L298N a la protoboard: la tierra llega por el BTS7960 y la Pi.

**BTS7960**

| Terminal | Va a |
|---|---|
| RPWM | J12 (GPIO 25): sube |
| LPWM | J11 (GPIO 26): baja |
| R_EN, L_EN y VCC | Riel + derecho (**3.3 V**) |
| GND | Riel − derecho |
| R_IS, L_IS | Sin conectar |
| B+ / B− | LiPo + / LiPo − |
| M+ / M− | Los dos cables del actuador |

- Motor al revés → intercambiar su rojo y blanco en el L298N.
- Actuador al revés → intercambiar sus cables en M+ y M−.
- El actuador se detiene solo en los extremos (finales de carrera internos). Consume ~2–3 A con carga.

### 10.6 Raspberry Pi 5

| Conexión | Puerto de la Pi | Nota |
|---|---|---|
| Buck 5.1 V 5 A | USB-C | |
| A9 del ESP32 (GPIO 16, RX2) | Pin 8 (GPIO 14, TXD) | Ambos 3.3 V: directo |
| A10 del ESP32 (GPIO 17, TX2) | Pin 10 (GPIO 15, RXD) | Directo |
| Riel − izquierdo | Pin 6 (GND) | Tierra común |
| SSD M.2 | Conector PCIe | Arranca de aquí |
| Adaptador del RPLIDAR A1 | USB negro (USB 2) | |
| ESP32 (su micro-USB) | El otro USB negro | Le da 5 V y permite programarlo desde la Pi |
| Camera Module 3 | CAM/DISP 0 | Cable 22→15 pines, contactos metálicos hacia el puerto Ethernet |
| Active Cooler | FAN | |

### 10.7 Montaje en la mesa sin chasis

- **Motores:** sujetos con prensa o cinta, ruedas al aire.
- **Actuador:** amarrado por su soporte trasero, vástago libre.
- **Celda:** atornillada en voladizo a un trozo de madera con sus separadores (suelta da lecturas sin sentido).
- **RPLIDAR:** superficie plana con espacio libre alrededor (gira).
- **Cámara:** fija con cinta, apuntando a un QR impreso.
- **Drivers y buck:** sobre madera o plástico, nunca sobre mesa metálica.
- **LiPo:** lejos de los cables y sobre superficie que no se queme.
- **Etiquetas:** marcar cada cable con cinta ("ENC-I A", "IN3", etc.).

---

## 11. Raspberry Pi 5: SSD y configuración

### 11.1 Grabar el sistema en el SSD

1. Antes de grabar, revisar qué tiene el SSD (el Imager **borra todo**):
   - **Windows:** Explorador (`Win + E`) o Administración de discos (`Win + R` → `diskmgmt.msc`). "No asignado" = vacío; "RAW" o sin letra = probablemente Linux viejo.
   - **Mac:** Finder o Utilidad de Discos.
2. En **Raspberry Pi Imager** elegir **Raspberry Pi OS (64-bit)** (la *Recommended*). Picamera2, OpenCV y las librerías del RPLIDAR funcionan en 64 bits.
3. **Storage:** el SSD (verificar nombre y tamaño).
4. **Customisation:** hostname `koleo`, usuario y contraseña, Wi-Fi con país **MX**, zona horaria America/Mexico_City, **SSH activado**.
5. Grabar y verificar.

### 11.2 SSD NVMe por PCIe

```bash
sudo apt update && sudo apt full-upgrade -y
sudo rpi-eeprom-update -a
sudo reboot
lsblk            # debe aparecer nvme0n1
```

- Si no aparece con una HAT de otra marca: agregar `dtparam=pciex1` a `/boot/firmware/config.txt`.
- Orden de arranque: `sudo raspi-config` → *Advanced Options → Boot Order → NVMe/USB Boot*, o en `sudo rpi-eeprom-config --edit` poner `BOOT_ORDER=0xf416` (se lee de derecha a izquierda: NVMe, SD, USB).
- Opcional (más rápido, no certificado): `dtparam=pciex1_gen=3` en `config.txt`.
- Si solo se usa como almacenamiento: partición ext4 montada en `/mnt/ssd` con `nofail` en `/etc/fstab`.

### 11.3 Dos ajustes obligatorios para KOLEO

| Ajuste | Dónde | Para qué |
|---|---|---|
| `dtparam=uart0=on` | `/boot/firmware/config.txt` | Habilita el UART en GPIO 14/15 → `/dev/ttyAMA0` (enlace con el ESP32) |
| `PSU_MAX_CURRENT=5000` | `sudo rpi-eeprom-config --edit` | Sin fuente que negocie 5 A, la Pi 5 limita los USB a 600 mA. Ponerlo **solo si el buck de verdad da 5 A** |

También conviene desactivar la consola de login por serie (`raspi-config` → Interface Options → Serial Port: login shell **No**, hardware **Sí**).

### 11.4 Puertos serie y pruebas rápidas

- El LIDAR y el ESP32 aparecen como `/dev/ttyUSB0` o `/dev/ttyUSB1` y el número puede cambiar al reiniciar. En el código usar la ruta de `ls /dev/serial/by-id/`.
- Cámara: `rpicam-hello`.
- Enlace con el ESP32: `python3 -m serial.tools.miniterm /dev/ttyAMA0 115200`.
- Bajo voltaje: `vcgencmd get_throttled` debe dar `throttled=0x0`.

---

## 12. Orden de encendido y pruebas

De lo más seguro a lo más arriesgado:

1. **Sin batería, buscar cortos.** Multímetro en continuidad entre +12 V y GND: no debe pitar. *Obligatorio sin fusible.*
2. **ESP32 por el USB de la compu, sin 12 V.** Probar HX711, VL53L1X y HC-SR04 uno por uno. Girar cada rueda a mano: el contador sube en un sentido y baja en el otro.
3. **Buck de la Pi.** Si es ajustable, conectarlo a la batería sin la Pi y ajustar a **5.1 V**.
4. **Pi sola** (motores y actuador desconectados de sus drivers). Que arranque del SSD, `throttled=0x0`, que el LIDAR gire y `rpicam-hello` muestre imagen.
5. **Enlace Pi–ESP32.** Pasar el USB del ESP32 a la Pi y probar el UART con miniterm en `/dev/ttyAMA0` a 115200.
6. **Motores.** Adelante, atrás, distintas velocidades. Orden de stop desde la Pi: se detienen y la Pi sigue encendida.
7. **Actuador.** Subir y bajar sin carga. Luego con peso: el HX711 lo lee y bloquea la elevación arriba de 10 kg.
8. **Todo junto 3 minutos.** Al terminar, desconectar el conector T y medir la LiPo: en reposo ≥ ~10.8 V.

---

## 13. Código de prueba de sensores (ESP32)

Archivo `prueba_sensores.ino` (guardar dentro de una carpeta llamada `prueba_sensores`).

**Antes de subirlo**
- Librerías (Herramientas → Administrar bibliotecas):
  - **HX711 Arduino Library**, de Bogdan Necula.
  - **VL53L1X**, de **Pololu** (no la de SparkFun ni Adafruit).
- Placa: **ESP32 Dev Module** (no "4D Systems gen4-ESP32-S3" ni otra).
- Monitor serie a **115200** baudios.

**Comandos:** `t` = tara · `c 500` = calibrar con peso conocido en gramos (devuelve un factor para copiar en `factorCelda`).

```cpp
/*
  KOLEO - Prueba de sensores en el ESP32
  HC-SR04 (ultrasonico), VL53L1X (ToF) y HX711 con celda de carga.

  Conexiones (protoboard vertical, ESP-32S con USB arriba):
    HX711    DT  -> GPIO 4  (fila 8 izq)    SCK -> GPIO 5  (fila 11 izq)
             VCC -> riel + (3.3 V)          GND -> riel -
    HC-SR04  TRIG -> GPIO 18 (fila 12 izq)
             ECHO -> divisor 1k/2k -> GPIO 19 (fila 13 izq)
             VCC  -> pin 5V (fila 2 der)    GND -> riel -
    VL53L1X  SDA -> GPIO 21 (fila 15 izq)   SCL -> GPIO 22 (fila 18 izq)
             VIN -> riel + (3.3 V)          GND -> riel -

  Librerias (Arduino IDE > Administrador de bibliotecas):
    - "HX711 Arduino Library" de Bogdan Necula
    - "VL53L1X" de Pololu

  Monitor serie a 115200 baudios. Comandos:
    t        -> tara (pone la bascula en cero, sin peso encima)
    c 500    -> calibra con un peso conocido, en gramos (ej. 500 g)
*/

#include <Wire.h>
#include <HX711.h>
#include <VL53L1X.h>

// ---------- Pines ----------
const int PIN_HX_DT   = 4;
const int PIN_HX_SCK  = 5;
const int PIN_TRIG    = 18;
const int PIN_ECHO    = 19;
const int PIN_SDA     = 21;
const int PIN_SCL     = 22;

// Factor de calibracion de la celda. Cambialo por el que te de el comando "c".
float factorCelda = 420.0;

HX711 bascula;
VL53L1X tof;

bool hxOk  = false;
bool tofOk = false;

// ---------- HC-SR04 ----------
// Devuelve la distancia en cm, o -1 si no hubo eco.
float leerUltrasonico() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);

  unsigned long us = pulseIn(PIN_ECHO, HIGH, 30000);  // maximo ~5 m
  if (us == 0) return -1;
  return us * 0.0343 / 2.0;
}

// ---------- Escaner I2C ----------
void escanearI2C() {
  Serial.println("Buscando dispositivos I2C...");
  int encontrados = 0;
  for (byte dir = 1; dir < 127; dir++) {
    Wire.beginTransmission(dir);
    if (Wire.endTransmission() == 0) {
      Serial.printf("  Dispositivo en 0x%02X", dir);
      if (dir == 0x29) Serial.print("  <- VL53L1X");
      Serial.println();
      encontrados++;
    }
  }
  if (encontrados == 0) {
    Serial.println("  Nada. Revisa SDA (21), SCL (22), VIN (3.3 V) y GND del VL53L1X.");
  }
}

// ---------- Comandos por el monitor serie ----------
void revisarComandos() {
  if (!Serial.available()) return;
  String linea = Serial.readStringUntil('\n');
  linea.trim();
  if (linea.length() == 0) return;

  if (linea == "t") {
    if (!hxOk) { Serial.println("HX711 no responde, no se puede tarar."); return; }
    Serial.println("Tarando... no toques la celda.");
    bascula.tare(20);
    Serial.println("Listo, bascula en cero.");
  }
  else if (linea.startsWith("c")) {
    if (!hxOk) { Serial.println("HX711 no responde, no se puede calibrar."); return; }
    float gramos = linea.substring(1).toFloat();
    if (gramos <= 0) {
      Serial.println("Escribe el peso en gramos, por ejemplo: c 500");
      return;
    }
    Serial.printf("Calibrando con %.1f g. Deja el peso quieto...\n", gramos);
    bascula.set_scale(1.0);
    float lectura = bascula.get_value(20);   // ya descuenta la tara
    if (lectura == 0) { Serial.println("Lectura en cero: revisa la celda."); return; }
    factorCelda = lectura / gramos;
    bascula.set_scale(factorCelda);
    Serial.printf("Nuevo factor: %.3f  -> copialo en 'factorCelda' del codigo.\n", factorCelda);
  }
  else {
    Serial.println("Comandos: t (tara) | c <gramos> (calibrar)");
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println();
  Serial.println("=== KOLEO - prueba de sensores ===");

  // HC-SR04
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  digitalWrite(PIN_TRIG, LOW);

  // VL53L1X
  Wire.begin(PIN_SDA, PIN_SCL);
  Wire.setClock(400000);
  escanearI2C();
  tof.setTimeout(500);
  if (tof.init()) {
    tof.setDistanceMode(VL53L1X::Long);          // hasta ~4 m
    tof.setMeasurementTimingBudget(50000);       // 50 ms por medicion
    tof.startContinuous(50);
    tofOk = true;
    Serial.println("VL53L1X: OK");
  } else {
    Serial.println("VL53L1X: NO responde.");
  }

  // HX711
  bascula.begin(PIN_HX_DT, PIN_HX_SCK);
  if (bascula.wait_ready_timeout(1000)) {
    hxOk = true;
    bascula.set_scale(factorCelda);
    Serial.println("HX711: OK. Tarando, deja la celda sin peso...");
    bascula.tare(20);
    Serial.println("HX711: tara lista.");
  } else {
    Serial.println("HX711: NO responde. Revisa DT (4), SCK (5), VCC y GND.");
  }

  Serial.println("Comandos: t (tara) | c <gramos> (calibrar)");
  Serial.println("------------------------------------------");
}

void loop() {
  revisarComandos();

  // Ultrasonico
  float cmUS = leerUltrasonico();

  // ToF
  int mmToF = -1;
  bool tofValido = false;
  if (tofOk) {
    mmToF = tof.read();
    tofValido = !tof.timeoutOccurred() && tof.ranging_data.range_status == VL53L1X::RangeValid;
  }

  // Celda
  float gramos = 0;
  long crudo = 0;
  bool hxListo = hxOk && bascula.wait_ready_timeout(200);
  if (hxListo) {
    crudo  = bascula.read();
    gramos = bascula.get_units(5);
  }

  // Imprimir todo en una linea
  if (cmUS < 0) Serial.print("US: sin eco      ");
  else          Serial.printf("US: %6.1f cm  ", cmUS);

  if (!tofOk)          Serial.print("| ToF: no conectado  ");
  else if (!tofValido) Serial.print("| ToF: fuera de rango ");
  else                 Serial.printf("| ToF: %5d mm  ", mmToF);

  if (!hxOk)         Serial.print("| Celda: no conectada");
  else if (!hxListo) Serial.print("| Celda: sin datos");
  else               Serial.printf("| Celda: %8.1f g  (crudo %ld)", gramos, crudo);

  Serial.println();
  delay(300);
}
```

**Qué se ve al arrancar:** escaneo I2C (el VL53L1X aparece en **0x29**), "OK" o "NO responde" por sensor y luego una línea cada 0.3 s, por ejemplo:
`US: 23.4 cm | ToF: 231 mm | Celda: 0.0 g (crudo 84213)`

**Comprobación:** acercar la mano a los dos sensores de distancia (deben bajar casi igual; ToF en mm, US en cm). Presionar la celda: el valor "crudo" debe cambiar mucho.

---

## 14. Solución de problemas

### Error de compilación "exit status 1"
El error real está en las líneas rojas de más arriba en la consola.
1. `HX711.h` o `VL53L1X.h: No such file or directory` → falta la librería.
2. `'class HardwareSerial' has no member named 'printf'` → placa equivocada; elegir **ESP32 Dev Module**.
3. Errores con `setDistanceMode`, `RangeValid` o `ranging_data` → librería VL53L1X equivocada; usar la de **Pololu**.
4. "El chip es ESP32, no ESP32-S3" → se eligió una placa S3; buscar "esp32 dev".

### Ningún sensor responde
1. **El ESP32 está corrido una fila** (filas 1–19 en vez de 2–20): conectar guiándose por la **etiqueta impresa** de cada pin, no por el número de hoyo.
2. **Falta el GND del ESP32 al riel −:** medir continuidad entre un pin GND y el riel −; tiene que pitar.
3. **GND del HC-SR04 en la columna +:** debe ir en la columna pegada a la línea **azul (−)**.
4. **Divisor mal armado:** Echo + pata de la 1 kΩ en la misma fila; la otra pata de la 1 kΩ + pata de la 2 kΩ + cable al GPIO 19 en la misma fila; la otra pata de la 2 kΩ al riel −.
   - 1 kΩ: café-negro-negro-café · 2 kΩ: rojo-negro-negro-café.
5. Revisar alimentación de cada sensor: HX711 y VL53L1X a 3.3 V/GND; HC-SR04 a 5V/GND.

### Celda de carga
- El peso baja al poner carga / sale negativo → intercambiar blanco y verde, o usar factor negativo.
- El valor crudo no cambia → revisar los 4 cables de la celda al HX711.

### Encoders
- El contador no cambia o salta solo → faltan pull-ups (GPIO 34–39 no los traen). Para cada señal: cable del encoder a una fila libre del lado derecho (filas 28–31), resistencia de **10 kΩ** de esa fila al riel +, y puente de esa fila al hoyo J original.

---

## 15. Software: firmware, Raspberry Pi y base de datos

### 15.1 Firmware del ESP32 (secciones)

1. Configuración Wi-Fi y servidor
2. Definición de pines
3. Constantes de operación y seguridad (límite 10 kg, distancias)
4. Variables globales
5. Interrupciones de encoders
6. Inicialización (`setup`)
7. Lectura de sensores (peso y distancia)
8. Elevación con protección de 10 kg (`levantarTarima()`)
9. Depósito de tarima
10. Control de motores DC
11. Envío de datos a la base de datos (POST a `/api/actualizar_tarima`)
12. Bucle principal (comandos de la Raspberry Pi por UART)

**Lo esencial para presentar (4 diapositivas):** flujo general (12) · sensores y elevación segura (7+8+9) · movimiento (10+5) · comunicación IoT (11+1).

**Recomendaciones de código (factibilidad):**
- Interrupción solo en el canal A de los encoders (GPIO 34/35).
- GPIO 14 en LOW al inicio.
- El POST HTTP fuera del lazo de control.
- Stop por software y corte si hay PWM y los encoders no se mueven.
- Timeout del actuador ~8 s.

### 15.2 Script de la Raspberry Pi

- Lectura del QR de la tarima con la cámara (migrar a **Picamera2**).
- Planeación de rutas con la clase **`PlanificadorAStar`** (A\*), probada en simulación con 3 rutas.
- `ejecutar_mision()`: manda al ESP32 los comandos **LIFT, MOVE, STOP, DROP** por UART.
- Pendiente: usar el RPLIDAR (hoy el mapa es fijo).

### 15.3 Base de datos

**Tipo:** SQL relacional (SQLite en la demo, archivo `koleo_almacen.db`), tres tablas unidas por `id_tarima`.

| Tabla | Campos principales |
|---|---|
| `tarimas` | `id_tarima` (PK), `descripcion`, `peso_kg`, `coord_x_cm`, `coord_y_cm`, `estado`, `ultima_actualizacion` |
| `historial_movimientos` | `id_tarima`, `ruta`, `destino_x_cm`, `destino_y_cm`, `peso_kg`, `latencia_ms`, `fecha_hora` |
| `registro_rechazos_seguridad` | `id_tarima`, `peso_detectado_kg`, `motivo`, `fecha_hora` |

**Flujo:** ESP32 arma un JSON al levantar, depositar o rechazar → Wi-Fi · HTTP POST `/api/actualizar_tarima` → Web API (Flask) valida y escribe → `UPDATE tarimas` + `INSERT historial`.

**Ejemplo de paquete del ESP32:**
```json
{
  "id_tarima": "TAR-101",
  "peso_kg": 8.45,
  "coord_x_cm": 150.0,
  "coord_y_cm": 120.0,
  "estado": "EN_PISO"
}
```

**Demo `demo_avance_vivo.py`:**
- `inicializar_bd()`: crea las tablas desde cero y carga 3 tarimas semilla: TAR-101 (Lote Electrónica A, 8.45 kg), TAR-102 (Baterías, **11.80 kg**, para probar el rechazo), TAR-103 (Sensores Ópticos C, 6.20 kg).
- `procesar_paquete_esp32(conn, id_tarima, peso_kg, ruta, nuevo_x, nuevo_y)`:
  - Si pesa > 10 kg → estado `BLOQUEADA_SOBREPESO` + registro en `registro_rechazos_seguridad` con motivo `EXCEDE_LIMITE_10KG_ACTUADOR_PROTEGIDO`.
  - Si es válida → actualiza peso, coordenadas y estado `UBICADA_DESTINO`; mide latencia; inserta en `historial_movimientos`.
- `mostrar_estado_bodega()`: imprime ID, peso, coordenadas, estado y fecha.
- `__main__`: simula 3 paquetes (RUTA_1 → (150, 120); RUTA_2 → (90, 120) rechazada; RUTA_3 → (150, 0)).

**Esquema completo (diagrama entidad-relación de la presentación)**

| Tabla | Llave | Campo | Tipo |
|---|---|---|---|
| `tarimas` | PK | `id_tarima` | VARCHAR(32) |
| | | `descripcion` | TEXT |
| | | `peso_kg` | DECIMAL(5,2) |
| | | `coord_x_cm` / `coord_y_cm` | DECIMAL(6,2) |
| | | `estado` | VARCHAR(20) |
| | | `ultima_actualizacion` | TIMESTAMP |
| `historial_movimientos` | PK | `id_movimiento` | INTEGER |
| | FK | `id_tarima` | VARCHAR(32) |
| | | `ruta_ejecutada` | VARCHAR(32) |
| | | `origen_x_cm` / `origen_y_cm` | DECIMAL(6,2) |
| | | `destino_x_cm` / `destino_y_cm` | DECIMAL(6,2) |
| | | `peso_medido_kg` | DECIMAL(5,2) |
| | | `latencia_red_ms` | INTEGER |
| | | `fecha_hora` | TIMESTAMP |
| `registro_rechazos_seguridad` | PK | `id_alerta` | INTEGER |
| | FK | `id_tarima` | VARCHAR(32) |
| | | `peso_detectado_kg` | DECIMAL(5,2) |
| | | `motivo` | VARCHAR(100) |
| | | `coord_x_cm` / `coord_y_cm` | DECIMAL(6,2) |
| | | `fecha_hora` | TIMESTAMP |

- Relación **1 → N**: una tarima tiene muchos movimientos y muchos rechazos.
- En el SQL, la relación con los rechazos no tiene FOREIGN KEY declarada (línea punteada en el diagrama).
- Uso: el ESP32 actualiza `tarimas` al levantar y al depositar; cada traslado agrega una fila al historial; una carga de más de 10 kg se guarda en rechazos.

**Estados que se usan**

| Estado | Quién lo pone | Cuándo |
|---|---|---|
| `EN_TRANSITO` | ESP32 | Al levantar una tarima válida |
| `EN_PISO` | ESP32 | Al depositar |
| `RECHAZADA_SOBREPESO` | ESP32 | Al pesar más de 10 kg |
| `BLOQUEADA_SOBREPESO` | Demo de la BD | Equivalente al anterior (hay que unificar) |
| `UBICADA_DESTINO` | Demo de la BD | Carga válida actualizada |

**Registro que genera el ejemplo de JSON en `tarimas`:** `TAR-101 · 8.45 · 150.00 · 120.00 · EN_PISO · 2026-10-21 07:27`.

**Problemas conocidos de la BD**
- Falta la Web API (la base es local; los paquetes son simulados).
- Estados inconsistentes: el ESP32 manda `RECHAZADA_SOBREPESO` y la BD usa `BLOQUEADA_SOBREPESO`.
- La latencia solo mide el UPDATE local, no el trayecto ESP32 → BD (< 2 s extremo a extremo).
- Falta `AUTOINCREMENT` y campos `NOT NULL`.

### 15.4 Interfaz / dashboard

- **No existe todavía.** Debe mostrar **≥ 5 indicadores** en tiempo real (la presentación lista 8 en su diapositiva de Indicadores Métricos).
- **Propuesta de plataforma:**
  - **Flask (Python):** servidor web y Web API, mismo lenguaje que el resto del proyecto.
  - **HTML + CSS + JavaScript:** el tablero en el navegador, sin instalar nada.
  - **SQL:** lee la misma base donde escribe el robot.
- **Funciones propuestas:**
  1. Mapa del almacén: posición de cada tarima, estanterías y el robot.
  2. Indicadores en tiempo real: ocupación, peso, tiempo de ciclo, precisión y alertas.
  3. Historial de movimientos: ruta, destino, peso y fecha de cada traslado.
  4. Alertas: tarimas rechazadas por sobrepeso.
- **Comunicación:** el tablero consulta la Web API, que lee la base donde escribe el ESP32.
- Se llegó a hacer un diseño del tablero para la presentación, pero el equipo decidió **no incluir diapositivas de interfaz**.

---

## 16. Presentación

**Archivo:** "Organización automática en almacenes" (.pptx).

### Estructura requerida (avances generales del reto)
1. **Portada:** título, integrantes, fecha y curso.
2. **Introducción:** problema y objetivos.
3. **Sensores y actuadores:** listas con tipo, función y propósito; diagrama de conexión; justificación.
4. **Base de datos:** tipo, estructura, ejemplo de registro/flujo, conexión con dispositivos.
5. **Interfaz gráfica:** plataforma, capturas/diseño, funciones, comunicación.
6. **Trabajo realizado:** avances, logros, pruebas, dificultades y soluciones.
7. **Trabajo a realizar:** pendientes, mejoras, próximos pasos, cronograma.

### Versión final
- **37 diapositivas**, agrupadas en las 7 secciones del panel de PowerPoint.
- Agregados: curso/grupo/fecha en portada, índice, objetivos del Charter, tablas de sensores y actuadores con justificación, tipo y flujo de la BD con ejemplo, trabajo realizado (resumen, pruebas, dificultades), pendientes y cronograma.
- **Sección 5 (Interfaz):** solo la diapositiva de Indicadores Métricos ("Indicadores del almacén"); por decisión del equipo **no** se agregaron diapositivas de interfaz.
- Pruebas reportadas (solo lo real): A\* resolviendo las 3 rutas en simulación y la demo de BD rechazando la tarima de 11.8 kg.
- Cronograma: semana 3 como actual; el chasis pasó de la semana 2 a la 3.
- La diapositiva 4 de BD se cambió por un diagrama entidad-relación de las 3 tablas.
- Separadores de código: "Código 1 de 3" (para no confundir con las 7 secciones).

### Objetivos (diapositiva de Introducción)

| Área | Objetivo | Meta |
|---|---|---|
| Mecánica | Levantar y transportar la tarima de forma segura | 10 kg en < 10 s, y transportarlos 3 min sin fallas |
| Mapeo y navegación | Que el robot llegue de un punto a otro de forma autónoma, conociendo por dónde moverse | < 5 cm de error, en 3 rutas distintas y sin colisiones |
| Software e IoT | Que el robot envíe sus movimientos para actualizar la posición de cada tarima en la BD | < 2 s de latencia, desde que deja la tarima hasta que la base se actualiza |

### Tabla de sensores (tipo, función y justificación)

| Sensor | Tipo | Función en KOLEO | Por qué se eligió |
|---|---|---|---|
| Camera Module 3 | Visión (imagen) | Lee el QR con el ID de cada tarima | Se conecta directo a la Pi 5 por CSI y tiene autoenfoque para leer de cerca |
| RPLIDAR A1 | LIDAR 2D de 360° | Mapea el espacio y ubica obstáculos | Barre 360° con alcance de hasta 12 m a bajo costo; USB |
| VL53L1X (antes VL53L5CX) | Distancia por tiempo de vuelo | Confirma si el espacio de enfrente está libre | Preciso, I2C, barato y disponible |
| HC-SR04 | Distancia por ultrasonido | Paro si hay un objeto a menos de 12 cm | Barato y lo lee el ESP32 directo, así frena aunque la Raspberry falle |
| Celda de carga + HX711 | Fuerza / peso | Pesa la tarima y bloquea la elevación arriba de 10 kg | La celda da milivoltios; el HX711 los amplifica y digitaliza (24 bits) |
| Encoders de los motores | Magnético (efecto Hall) | Cuentan las vueltas de cada rueda | Vienen integrados; permiten medir distancia y velocidad |

### Tabla de actuadores

| Componente | Tipo | Aplicación | Por qué se eligió |
|---|---|---|---|
| Actuador lineal 12 V (75 kg, 50 mm) | Eléctrico lineal | Sube y baja la plataforma | Movimiento recto y compacto; levanta 10 kg con mucho margen |
| BTS7960 | Driver de potencia (43 A) | Controla subir/bajar del actuador con PWM | Soporta la corriente del actuador con carga sin sobrecalentarse |
| 2 motores GA25-370 con reductora | Motor DC 12 V + caja reductora | Tracción diferencial: avanzar, frenar y girar | La reductora da el torque para mover el robot con 10 kg encima |
| L298N | Driver doble | Velocidad y sentido de cada motor | Un solo módulo maneja las dos ruedas |

**Procesamiento:** Raspberry Pi 5 (alto nivel: cámara, LIDAR, rutas A\*; tiene la potencia para imagen y LIDAR) y ESP32 (tiempo real e IoT: sensores, motores y envío a la BD; Wi-Fi integrado, PWM e interrupciones por hardware).

### Trabajo realizado por área (al 21-oct)

| Área | Logros |
|---|---|
| Mecánica | CAD 3D del chasis de 300 × 300 mm · mecanismo de elevación con actuador lineal · vistas con la ubicación de cada componente |
| Hardware y electrónica | Lista completa con potencia y regulación ($9,900, dentro del tope) · pinout del ESP32 y de la Pi 5 · diagrama de alimentación de 12 V |
| Control y navegación | Planeador A\* que resuelve las 3 rutas · lectura del QR · protocolo UART con el ESP32 (LIFT, MOVE, STOP, DROP) |
| Software e IoT | Firmware del ESP32 con pesaje y límite de 10 kg · envío HTTP con JSON a la Web API · esquema SQL de 3 tablas y demo de la BD |

### Pruebas y validaciones (lo que sí se hizo)

| Prueba | Cómo se hizo | Resultado |
|---|---|---|
| Planeación de rutas A\* | Script de la Pi en simulación, mapa de 5 × 6 celdas | Encuentra las 3 rutas sin cruzar estanterías: 10, 6 y 8 celdas |
| Rechazo por sobrepeso | Demo de la BD con 3 paquetes simulados | TAR-102 (11.80 kg) queda bloqueada y registrada; TAR-101 y TAR-103 se actualizan |
| Escritura en la BD | Tiempo de cada actualización en la demo local | ~1 ms por registro (meta < 2 s) |
| Revisión de conexiones | Pinout contra hojas de datos del ESP32 | 2 ajustes: GPIO 12 y la resistencia de los encoders |
| Presupuesto | Lista completa contra el tope del Charter | $9,900 MXN, dentro de $10,000 |

### Dificultades y soluciones

| Dificultad | Solución |
|---|---|
| La lista inicial no tenía drivers de potencia ni reguladores | Se agregaron puentes H, reguladores y batería dentro del tope |
| Los picos de corriente de los motores pueden reiniciar las placas | Alimentación separada para la Pi y el ESP32, y tierra común |
| El HC-SR04 trabaja a 5 V y el ESP32 a 3.3 V | Divisor resistivo de 1 kΩ / 2 kΩ en ECHO |
| El GPIO 12 es pin de arranque del ESP32 | IN3 del motor derecho se movió al GPIO 23 |
| La Camera Module 3 no funciona con OpenCV en la Pi 5 | Leer la cámara con Picamera2 |
| Riesgo de levantar más de 10 kg (riesgo principal del Charter) | Pesar antes de levantar: si pasa de 10 kg baja la plataforma y registra el rechazo |

### Trabajo a realizar

| Tareas pendientes | Mejoras planificadas | Próximos pasos |
|---|---|---|
| Ensamblar chasis y elevación | Encoders para avanzar por distancia | Prueba de banco con 10 kg (Hito 1) |
| Instalar tracción, celda y sensores | Freno por obstáculo continuo y paro si se pierde la comunicación | Transporte de 3 minutos |
| Programar la Web API en Flask | Bloquear la elevación si falla la báscula | Tres rutas autónomas (Hito 2) |
| Conectar la Pi y el ESP32 por UART | Integrar el RPLIDAR al mapa y la cámara con Picamera2 | Latencia < 2 s (Hito 3) |

### Cómo presentar el firmware sin saturar

Regla: **un título con la idea, un diagrama o fragmento de código (no ambos) y máximo 3 viñetas**.
1. **Cómo coordina la Pi al ESP32:** diagrama de 4–5 cajas (comando UART → mover → levantar/depositar → reportar).
2. **Elevación con protección de 10 kg:** diagrama de decisión "¿peso > 10 kg?" → rechazar / levantar.
3. **Movimiento con encoders:** ~6 líneas (interrupción que cuenta pulsos + función de PWM).
4. **Envío a la BD:** el JSON y la flecha ESP32 → Wi-Fi → Web API → BD.

**Para explicar los encoders:** "Cada motor tiene un encoder magnético que manda pulsos al girar. El ESP32 los cuenta con interrupciones para no perder ninguno. Con los pulsos, la reductora y el perímetro de la rueda calculamos la distancia. Hoy ya los contamos; el siguiente paso es avanzar por distancia y no por tiempo."

### Errores visuales que se corrigieron en la presentación
- "02" del separador partido en "0" y "2".
- Erratas: "; l comando STOP", "Envío a la base de datosT", "koejecutar_mision()".
- Última línea del código (`conn.commit()`) cortada.
- Separadores de código renombrados a "Código 1 de 3".
- Tabla de conexiones muy pequeña para proyector; diapositivas del CAD sin el encabezado "IMPLEMENTACIÓN IOT.".

### Reparto para presentar
El Charter define los cinco roles pero no quién tiene cada uno; el reparto se hizo por rol para que cada quien hable en un bloque seguido: **problema → robot físico → electrónica → movimiento → datos**.

### Sensores según la presentación de medio término
1. Cámara RGB (Camera Module 3): lee el QR, CSI a la Pi.
2. RPLIDAR A1: LIDAR 2D 360°, USB a la Pi.
3. ToF VL53L5CX *(ya cambiado a VL53L1X)*: I2C, GPIO 21/22.
4. HC-SR04: paro si hay objeto a < 12 cm; GPIO 18/19 con divisor.
5. Celda + HX711: bloquea la elevación > 10 kg; GPIO 4/5.
6. Encoders Hall: integrados en los motores; GPIO 34/35.

### Inconsistencias que siguen en la presentación
- Menciones a **agricultura** y **Google Coral**.
- Falta la **Raspberry Pi 5** en algunos diagramas.
- Actualizar VL53L5CX → **VL53L1X** y los modelos finales del BOM.
- Cambiar GPIO 12 en la tabla de pines si aparece.

---

## 17. Análisis de factibilidad

**Conclusión (11-nov-2026): factible sin piezas nuevas.** Motores y actuador alcanzan; los riesgos están en la navegación, los apoyos, el LIDAR y el software.

| Aspecto | Resultado |
|---|---|
| **Motores** (46.8:1, ~9 V tras el L298N) | 0.7–2 kgf·cm c/u con 14 kg → 0.2–0.28 m/s, 0.2–0.55 A; margen ~2–3×. Ruedas locas de bola sucias → 50–80 % del stall. **Solo piso liso.** |
| **Actuador** | 106 N = 14 % de 750 N; 50 mm ≈ 5–6 s (cumple < 10 s). Timeout de software ~8 s |
| **Batería** (24 Wh) | ~50 min manejando, ~30 min peor caso |
| **Navegación** | En lazo abierto **no** cumple 5 cm. Usar encoders (~515 pulsos/vuelta), calibrar con y sin carga, corregir con LIDAR/QR |
| **Apoyos** | Dejar 2 ruedas locas o subirlas 1–2 mm. LIDAR abajo al frente |
| **Tarima** | Claro ≥ 20 cm, ≥ 40 cm entre patas, sin travesaño en la entrada, fondo plano |
| **Etapa 2** | 6 sensores (contando encoders) y 3 actuadores para 5 alumnos — confirmar con el profesor |
| **Plataforma** | Necesita guías en la base, no solo el vástago del actuador |
| **USB de la Pi** | 1.6 A en total; si el SSD o el ESP32 se desconectan, revisar el consumo |
| **Latencia** | Medirla desde que la celda detecta que se soltó la tarima (bajar el actuador ya son ~5 s) |

Los números a detalle están en el [Anexo F](#anexo-f-cálculos-de-factibilidad-a-detalle).

---

## 18. Pendientes

1. Presentación con inconsistencias (agricultura, Google Coral, falta Pi 5).
2. **Falta la Web API.**
3. **Falta el dashboard de ≥ 5 indicadores.**
4. RPLIDAR no se usa en el código; mapa fijo.
5. Usar **Picamera2** para la cámara.
6. Navegación en lazo abierto → pasar a lazo cerrado con encoders.
7. SQL: `AUTOINCREMENT`, estados inconsistentes, campos `NOT NULL`.
8. Medir la latencia **extremo a extremo** (ESP32 → BD).
9. CAD: 6 apoyos; la torre del LIDAR se traslapa con la plataforma.
10. Presupuesto sin margen para repuestos.
11. Decidir si se quita el HC-SR04 o el RPLIDAR.
12. Construir el chasis (placas, postes, guías, plataforma, adaptador de la celda).
13. Confirmar con el profesor el reparto de sensores/actuadores de la Etapa 2.
14. Definir las dimensiones de las tarimas a escala (el robot mide ~19 cm de alto con plataforma).
15. Actualizar el firmware al pinout final (IN3 en GPIO 23, canal B en 36/39, VL53L1X, GPIO 14 en LOW, timeout del actuador).
16. Distinguir "sin lectura" de "0 kg" en el HX711 y bloquear la elevación si falla la báscula.
17. Fijar el PWM a una frecuencia conocida (`analogWriteFrequency()`), hoy usa la de por defecto.
18. Quitar los `delay()` bloqueantes de la elevación (usar `millis()`).

### Estado de la revisión del 20-oct

| # | Problema | Estado |
|---|---|---|
| 1 | Presentación: "agricultura", Google Coral, falta Pi 5, LIDAR conectado directo a motores | Pendiente |
| 2 | No existe la Web API | Pendiente |
| 3 | No hay dashboard de indicadores | Pendiente |
| 4 | GPIO 12 (strapping) como IN3 | **Resuelto:** IN3 en GPIO 23 |
| 5 | Encoders sin pull-up y un solo canal | **Resuelto:** canal B en 36/39; pull-ups de 10 kΩ solo si la señal flota |
| 6 | VL53L5CX y RPLIDAR no se usan en el código; mapa fijo | Pendiente (VL53L5CX ya cambiado a VL53L1X) |
| 7 | `cv2.VideoCapture(0)` no sirve con Camera Module 3 | Pendiente: usar Picamera2 |
| 8 | Navegación en lazo abierto | Pendiente |
| 9 | SQL: AUTOINCREMENT (solo SQLite), estados inconsistentes, NOT NULL que el ESP32 no manda | Pendiente |
| 10 | Latencia medida solo en la escritura | Pendiente |
| 11 | CAD con 6 apoyos y torre del LIDAR traslapada | Pendiente |
| 12 | Dimensiones de tarimas sin definir | Pendiente |
| 13 | Presupuesto sin margen | Se resolvió quitando piezas |

---

## 19. Referencias

**Documentos del proyecto**
- Armado final completo (sin base): https://claude.ai/artifact/2pCsPp8ojY1xXew9tZ5QT2
- Contexto del proyecto: `claude/KOLEO_contexto.md` (en el proyecto KOLEO)

**Conversaciones**
- [Armado final del proyecto](https://claude.ai/chat/7864eecf-8a15-4804-b65e-10cd9bf47051) — 11-nov
- [Búsqueda de pila en Amazon](https://claude.ai/chat/0b0bb3d2-c310-42cf-b556-c106b06d2cca) — 10-nov
- [Armado de circuito sin base](https://claude.ai/chat/7cec0f30-0fad-4181-aea4-520519806201) — 9/10-nov
- [Configurar SSD en Raspberry Pi](https://claude.ai/chat/1dcdad8a-f955-41ea-8d0d-dfa2fd2fa241) — 9-nov
- [Sensores y actuadores para proyecto](https://claude.ai/chat/c107b3cc-2372-4565-9d93-1ee5a0d1dc4e) — 7-nov
- [Presentación de medio término](https://claude.ai/chat/c53c9dea-d5c4-4f63-83c7-350f5e6492cf) — 3-nov
- [Presentación esencial librerías](https://claude.ai/chat/13234c8e-1338-479d-9e0c-13fb042396e3) — 21-oct

**Productos**
- [Baterías OVONIC 3S 2200 mAh](https://www.amazon.com.mx/gp/product/B08CZ4NQ7K)
- [Conectores T Hobbypark](https://www.amazon.com.mx/gp/product/B08HJXHJKS)
- [Cargador Tosiicop](https://www.amazon.com.mx/dp/B0FS23G6KD)

---
---

# Anexos

## Anexo A. Firmware original del ESP32

Archivo `koleo_esp32_firmware.ino`, la versión de octubre (generada con Gemini y revisada para la presentación).

> ⚠️ **Usa el pinout viejo.** Antes de cargarlo al armado actual hay que cambiar:
> - `PIN_MOT_R_IN3` de **12 → 23** (el 12 es pin de arranque).
> - Agregar el canal B de los encoders: **36** (izq) y **39** (der).
> - `INPUT_PULLUP` no funciona en 34/35 (no tienen pull-up interno): usar `INPUT` y resistencias externas si la señal flota.
> - Poner **GPIO 14 en LOW** al inicio de `setup()`.
> - Cambiar `TIEMPO_ELEV_MS` a ~6000–8000 ms según la prueba real (50 mm ≈ 5–6 s).
> - Unificar `RECHAZADA_SOBREPESO` con la base de datos.
> - Cambiar SSID, contraseña y `SERVER_URL` por los reales.

```cpp
/*
 * PROYECTO KOLEO - FIRMWARE ESP32 (CONTROL TIEMPO REAL + SEGURIDAD + IoT)
 * Funciones:
 * 1. Lectura de Celda de Carga HX711 con bloqueo de seguridad a > 10.0 kg.
 * 2. Control de Actuador Lineal 12V y Motores DC con Encoders.
 * 3. Paro de emergencia con sensor ultrasónico HC-SR04.
 * 4. Envío HTTP POST a la Base de Datos en < 2 segundos tras dejar la tarima.
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include "HX711.h"

// ================= CONFIGURACIÓN WIFI Y SERVIDOR =================
const char* WIFI_SSID     = "Tec-IoT-Network";
const char* WIFI_PASSWORD = "password123";
const char* SERVER_URL    = "http://192.168.1.100:5000/api/actualizar_tarima";

// ================= DEFINICIÓN DE PINES (SEGÚN TABLA MAESTRA) =================
// Celda de carga HX711
#define PIN_HX711_DT   4
#define PIN_HX711_SCK  5

// Actuador Lineal Eléctrico 12V (Puente H BTS7960)
#define PIN_ACT_SUBIR  25
#define PIN_ACT_BAJAR  26

// Motores DC con Reductora
#define PIN_MOT_L_PWM  32
#define PIN_MOT_L_IN1  33
#define PIN_MOT_L_IN2  27
#define PIN_MOT_R_PWM  14
#define PIN_MOT_R_IN3  12   // <-- CAMBIAR A 23
#define PIN_MOT_R_IN4  13

// Encoders Cuadratura
#define PIN_ENC_L      34
#define PIN_ENC_R      35

// Sensor Ultrasónico HC-SR04 (Seguridad redundante)
#define PIN_TRIG       18
#define PIN_ECHO       19

// ================= CONSTANTES DE OPERACIÓN Y SEGURIDAD =================
const float PESO_MAXIMO_KG         = 10.00;  // Límite estricto del Charter (10 kg)
const float FACTOR_CALIBRACION     = 2280.0; // Ajustar con peso patrón en banco
const float DISTANCIA_PARO_CM      = 12.0;   // Paro anticolisión inmediato
const unsigned long TIEMPO_ELEV_MS = 8500;   // < 10 segundos (Métrica de éxito mecánica)

// Variables globales
HX711 balanza;
volatile long pulsosEncoderIzq = 0;
volatile long pulsosEncoderDer = 0;
float coordX_cm = 0.0;
float coordY_cm = 0.0;
String idTarimaActual = "TAR-101";

// Interrupciones para odometría de encoders
void IRAM_ATTR isrEncoderIzq() { pulsosEncoderIzq++; }
void IRAM_ATTR isrEncoderDer() { pulsosEncoderDer++; }

void setup() {
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, 16, 17); // UART con Raspberry Pi 5

  // Configurar pines de actuador y motores
  pinMode(PIN_ACT_SUBIR, OUTPUT);
  pinMode(PIN_ACT_BAJAR, OUTPUT);
  pinMode(PIN_MOT_L_PWM, OUTPUT);
  pinMode(PIN_MOT_L_IN1, OUTPUT);
  pinMode(PIN_MOT_L_IN2, OUTPUT);
  pinMode(PIN_MOT_R_PWM, OUTPUT);
  pinMode(PIN_MOT_R_IN3, OUTPUT);
  pinMode(PIN_MOT_R_IN4, OUTPUT);
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);

  // Configurar Encoders
  pinMode(PIN_ENC_L, INPUT_PULLUP);
  pinMode(PIN_ENC_R, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_ENC_L), isrEncoderIzq, RISING);
  attachInterrupt(digitalPinToInterrupt(PIN_ENC_R), isrEncoderDer, RISING);

  // Inicializar HX711
  balanza.begin(PIN_HX711_DT, PIN_HX711_SCK);
  balanza.set_scale(FACTOR_CALIBRACION);
  balanza.tare(); // Poner a cero sin carga

  // Conexión Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Conectando a WiFi");
  int intentos = 0;
  while (WiFi.status() != WL_CONNECTED && intentos < 20) {
    delay(500);
    Serial.print(".");
    intentos++;
  }
  Serial.println("\n[OK] Sistema KOLEO ESP32 Inicializado.");
}

// ================= FUNCIONES DE SENSORES Y SEGURIDAD =================
float medirPesoKg() {
  if (balanza.is_ready()) {
    float peso = balanza.get_units(5); // Promedio de 5 lecturas rápidas
    return (peso < 0.0) ? 0.0 : peso;
  }
  return 0.0;
}

float medirDistanciaUltrasonicoCm() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);
  long duracion = pulseIn(PIN_ECHO, HIGH, 25000); // Timeout 25 ms
  if (duracion == 0) return 999.0;
  return duracion * 0.034 / 2.0;
}

// ================= CONTROL DE ELEVACIÓN CON PROTECCIÓN DE 10 KG =================
bool levantarTarima(String idTarima) {
  Serial.println("Iniciando verificación de peso para tarima: " + idTarima);

  // 1. Extender 1.5 segundos para hacer contacto inicial con la tarima y pesarla
  analogWrite(PIN_ACT_SUBIR, 255);
  analogWrite(PIN_ACT_BAJAR, 0);
  delay(1500);
  analogWrite(PIN_ACT_SUBIR, 0); // Pausa para lectura limpia de celda de carga
  delay(300);

  float pesoActual = medirPesoKg();
  Serial.printf("Peso detectado: %.2f kg\n", pesoActual);

  // 2. VALIDACIÓN ESTRICTA DE RIESGO PRINCIPAL (> 10 KG)
  if (pesoActual > PESO_MAXIMO_KG) {
    Serial.println("[ALERTA CRÍTICA] Sobrecarga detectada (> 10 kg). Abortando elevación.");
    // Bajar actuador inmediatamente para proteger la estructura
    analogWrite(PIN_ACT_SUBIR, 0);
    analogWrite(PIN_ACT_BAJAR, 255);
    delay(1600);
    analogWrite(PIN_ACT_BAJAR, 0);

    // Notificar rechazo a la Base de Datos
    enviarActualizacionBD(idTarima, pesoActual, coordX_cm, coordY_cm, "RECHAZADA_SOBREPESO");
    return false;
  }

  // 3. Peso seguro (<= 10 kg): Completar elevación en menos de 10 segundos
  Serial.println("[OK] Peso dentro de rango seguro. Completando elevación...");
  analogWrite(PIN_ACT_SUBIR, 255);
  delay(TIEMPO_ELEV_MS - 1500);
  analogWrite(PIN_ACT_SUBIR, 0);

  enviarActualizacionBD(idTarima, pesoActual, coordX_cm, coordY_cm, "EN_TRANSITO");
  return true;
}

void depositarTarima(String idTarima, float nuevoX, float nuevoY) {
  Serial.println("Descendiendo actuador lineal para depositar tarima...");
  analogWrite(PIN_ACT_SUBIR, 0);
  analogWrite(PIN_ACT_BAJAR, 255);
  delay(TIEMPO_ELEV_MS);
  analogWrite(PIN_ACT_BAJAR, 0);

  coordX_cm = nuevoX;
  coordY_cm = nuevoY;
  float pesoFinal = medirPesoKg();

  // Inmediatamente actualizar la Base de Datos (Latencia objetivo < 2 segundos)
  enviarActualizacionBD(idTarima, pesoFinal, coordX_cm, coordY_cm, "EN_PISO");
}

// ================= CONTROL DE MOTORES DC =================
void moverMotores(int pwmIzq, int pwmDer) {
  // Paro de emergencia automático si hay obstáculo a menos de 12 cm
  if (medirDistanciaUltrasonicoCm() < DISTANCIA_PARO_CM && (pwmIzq > 0 || pwmDer > 0)) {
    detenerMotores();
    Serial2.println("ERR:OBSTACULO_CERCANO");
    return;
  }

  // Motor Izquierdo
  digitalWrite(PIN_MOT_L_IN1, pwmIzq >= 0 ? HIGH : LOW);
  digitalWrite(PIN_MOT_L_IN2, pwmIzq >= 0 ? LOW : HIGH);
  analogWrite(PIN_MOT_L_PWM, abs(pwmIzq));

  // Motor Derecho
  digitalWrite(PIN_MOT_R_IN3, pwmDer >= 0 ? HIGH : LOW);
  digitalWrite(PIN_MOT_R_IN4, pwmDer >= 0 ? LOW : HIGH);
  analogWrite(PIN_MOT_R_PWM, abs(pwmDer));
}

void detenerMotores() {
  analogWrite(PIN_MOT_L_PWM, 0);
  analogWrite(PIN_MOT_R_PWM, 0);
}

// ================= ENVÍO IOT A BASE DE DATOS (< 2 SEGUNDOS) =================
void enviarActualizacionBD(String idTarima, float peso, float x, float y, String estado) {
  unsigned long tInicio = millis();
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");

    String payload = "{";
    payload += "\"id_tarima\":\"" + idTarima + "\",";
    payload += "\"peso_kg\":" + String(peso, 2) + ",";
    payload += "\"coord_x_cm\":" + String(x, 1) + ",";
    payload += "\"coord_y_cm\":" + String(y, 1) + ",";
    payload += "\"estado\":\"" + estado + "\"";
    payload += "}";

    int httpResponseCode = http.POST(payload);
    unsigned long latencia = millis() - tInicio;

    Serial.printf("[IoT DB] Respuesta HTTP: %d | Latencia: %lu ms (< 2000 ms OK)\n", httpResponseCode, latencia);
    http.end();
  } else {
    Serial.println("[IoT DB] Error: WiFi desconectado.");
  }
}

// ================= BUCLE PRINCIPAL (ESCUCHA A RASPBERRY PI 5) =================
void loop() {
  if (Serial2.available()) {
    String comando = Serial2.readStringUntil('\n');
    comando.trim();

    // Ejemplo de trama desde RPi 5: "LIFT:TAR-101" o "DROP:TAR-101:120.0:180.0" o "MOVE:180:180"
    if (comando.startsWith("LIFT:")) {
      idTarimaActual = comando.substring(5);
      bool exito = levantarTarima(idTarimaActual);
      Serial2.println(exito ? "ACK:LIFT_OK" : "ERR:OVERWEIGHT");
    }
    else if (comando.startsWith("DROP:")) {
      int p1 = comando.indexOf(':', 5);
      int p2 = comando.indexOf(':', p1 + 1);
      String id = comando.substring(5, p1);
      float destX = comando.substring(p1 + 1, p2).toFloat();
      float destY = comando.substring(p2 + 1).toFloat();
      depositarTarima(id, destX, destY);
      Serial2.println("ACK:DROP_OK");
    }
    else if (comando.startsWith("MOVE:")) {
      int p1 = comando.indexOf(':', 5);
      int velL = comando.substring(5, p1).toInt();
      int velR = comando.substring(p1 + 1).toInt();
      moverMotores(velL, velR);
    }
    else if (comando == "STOP") {
      detenerMotores();
    }
  }
}
```

### Protocolo UART Pi ↔ ESP32 (115200 baudios, una línea por comando)

| Comando | Ejemplo | Qué hace | Respuesta |
|---|---|---|---|
| `LIFT:<id>` | `LIFT:TAR-101` | Pesa y levanta la tarima | `ACK:LIFT_OK` o `ERR:OVERWEIGHT` |
| `DROP:<id>:<x>:<y>` | `DROP:TAR-101:120.0:180.0` | Baja la tarima, guarda la coordenada y manda POST a la BD | `ACK:DROP_OK` |
| `MOVE:<izq>:<der>` | `MOVE:180:180` | PWM con signo para cada motor (−255 a 255) | Nada, o `ERR:OBSTACULO_CERCANO` |
| `STOP` | `STOP` | PWM de los dos motores a 0 | Nada |

### Explicación por partes
- **Librerías:** `WiFi.h` conecta a la red, `HTTPClient.h` manda el POST, `HX711.h` lee la celda (librería externa).
- **Constantes:** `PESO_MAXIMO_KG` (límite del Charter), `FACTOR_CALIBRACION` (provisional, se ajusta en banco), `DISTANCIA_PARO_CM` (frena si hay algo a < 12 cm), `TIEMPO_ELEV_MS` (8.5 s, cumple < 10 s).
- **Variables `volatile`:** los contadores de pulsos los cambia una interrupción; `volatile` obliga a leer el valor real de memoria.
- **`IRAM_ATTR`:** guarda la interrupción en memoria interna rápida; debe ser muy corta (solo suma).
- **`levantarTarima()`:** sube 1.5 s para hacer contacto, pausa 0.3 s, pesa; si pasa de 10 kg baja 1.6 s, reporta el rechazo y regresa `false`; si no, completa la subida y reporta `EN_TRANSITO`.
- **`depositarTarima()`:** baja durante `TIEMPO_ELEV_MS`, guarda la coordenada, mide el peso y reporta `EN_PISO`.
- **`moverMotores()`:** si hay obstáculo al avanzar, frena y avisa; el signo del PWM decide el sentido y `abs()` la intensidad. PWM = 0 no es frenado activo.
- **`enviarActualizacionBD()`:** arma el JSON, hace POST, mide e imprime la latencia (200 = OK).
- **`loop()`:** lee una línea de `Serial2`, le quita espacios y decide por el prefijo.

---

## Anexo B. Script de la Raspberry Pi 5

Archivo `koleo_pi5_navigation.py` (versión de octubre). Usa `heapq`, `time`, `cv2` (OpenCV) y `serial` (pyserial).

- **Mapa del almacén (`MAPA_ALMACEN`):** cuadrícula de **5 × 6 celdas de 30 × 30 cm**; `0` es pasillo libre y `1` es estantería u obstáculo.
- **Rutas de validación (`RUTAS_VALIDACION`):** las 3 rutas del Hito 2, cada una con `inicio`, `fin` y `tarima_default`. En simulación, A\* las resuelve con **10, 6 y 8 celdas**.
- **Coordenadas:** cada celda es (fila, columna); × 30 da centímetros.

### Lectura del QR

```python
def leer_qr_tarima(id_respaldo="TAR-101"):
    cap = cv2.VideoCapture(0)          # <-- NO funciona con Camera Module 3 en Pi 5: usar Picamera2
    detector = cv2.QRCodeDetector()
    t_inicio = time.time()

    while time.time() - t_inicio < 2.5:
        ret, frame = cap.read()
        if not ret:
            break
        datos, _, _ = detector.detectAndDecode(frame)
        if datos:
            cap.release()
            print(f"[CÁMARA RGB] Tarima: {datos}")
            return datos

    cap.release()
    # Sin QR: usa el ID asignado a la ruta
    return id_respaldo
```

Busca un QR durante 2.5 s; si no lo encuentra, usa el ID de respaldo para no detener la misión.

### Planeación de ruta A\*

```python
class PlanificadorAStar:
    @staticmethod
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @classmethod
    def calcular_ruta(cls, mapa, inicio, meta):
        filas, cols = len(mapa), len(mapa[0])
        frontera = [(0, inicio)]
        vino_de = {inicio: None}
        costo_g = {inicio: 0}
        while frontera:
            _, actual = heapq.heappop(frontera)
            if actual == meta:
                break
            for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                vecino = (actual[0] + df, actual[1] + dc)
                if 0 <= vecino[0] < filas and 0 <= vecino[1] < cols:
                    if mapa[vecino[0]][vecino[1]] == 1:
                        continue  # obstáculo
                    nuevo_costo = costo_g[actual] + 1
                    if vecino not in costo_g or nuevo_costo < costo_g[vecino]:
                        costo_g[vecino] = nuevo_costo
                        prioridad = nuevo_costo + cls.heuristica(vecino, meta)
                        heapq.heappush(frontera, (prioridad, vecino))
                        vino_de[vecino] = actual
        if meta not in vino_de:
            return []
        ruta, paso = [], meta
        while paso is not None:
            ruta.append(paso)
            paso = vino_de[paso]
        ruta.reverse()
        return ruta
```

- **Heurística:** distancia Manhattan.
- **Cola de prioridad:** `heapq` expande primero la celda con menor costo + heurística.
- **Vecinos:** 4 direcciones; descarta bordes y obstáculos.
- **Reconstrucción:** recorre `vino_de` desde la meta y lo invierte.
- **Limitación:** solo 4 direcciones y no vuelve a planear si aparece un obstáculo nuevo.

### Ejecutar la misión (resumido)

```python
def ejecutar_mision(nombre_ruta, puerto_serial=None):
    config = RUTAS_VALIDACION[nombre_ruta]
    inicio, meta = config["inicio"], config["fin"]
    # 1. Identificar la tarima
    id_tarima = leer_qr_tarima(config["tarima_default"])
    # 2. Calcular la ruta con A*
    ruta = PlanificadorAStar.calcular_ruta(MAPA_ALMACEN, inicio, meta)
    # 3. Levantar y pesar la tarima
    if puerto_serial:
        puerto_serial.write(f"LIFT:{id_tarima}\n".encode())
        respuesta = puerto_serial.readline().decode().strip()
        if respuesta == "ERR:OVERWEIGHT":
            return  # excede 10 kg: se cancela
    # 4. Recorrer la ruta (cada celda = 30 cm)
    for paso in ruta[1:]:
        if puerto_serial:
            puerto_serial.write(b"MOVE:180:180\n")
            time.sleep(0.8)
            puerto_serial.write(b"STOP\n")
    # 5. Depositar y actualizar la base de datos
    dest_x, dest_y = meta[1] * 30.0, meta[0] * 30.0
    if puerto_serial:
        puerto_serial.write(f"DROP:{id_tarima}:{dest_x}:{dest_y}\n".encode())

if __name__ == "__main__":
    ejecutar_mision("RUTA_1", puerto_serial=None)
    # ... igual con RUTA_2 y RUTA_3
```

**Limitaciones:** lazo abierto (0.8 s por celda, sin giros), no garantiza error < 5 cm; hoy corre en simulación sin abrir el puerto serie. En el armado actual el puerto es `/dev/ttyAMA0` a 115200.

---

## Anexo C. Demo de la base de datos

Archivo `demo_avance_vivo.py` (SQLite, `koleo_almacen.db`). Fragmentos tal como se presentaron (resumidos).

### Crear las tablas

```python
import sqlite3
import time
from datetime import datetime

def inicializar_bd():
    conn = sqlite3.connect("koleo_almacen.db")
    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS tarimas;
        -- (igual con las otras dos tablas)
        CREATE TABLE tarimas (
            id_tarima TEXT PRIMARY KEY,
            descripcion TEXT, peso_kg REAL,
            coord_x_cm REAL, coord_y_cm REAL,
            estado TEXT, ultima_actualizacion TEXT);
        -- + historial_movimientos
        -- + registro_rechazos_seguridad
        INSERT INTO tarimas VALUES
        ('TAR-101', 'Lote Electrónica A', 8.45, ...),
        ('TAR-102', 'Baterías (Sobrepeso)', 11.80, ...),
        ('TAR-103', 'Sensores Ópticos C', 6.20, ...);
    """)
    conn.commit()
    return conn
```

### Registrar cada paquete

```python
def procesar_paquete_esp32(conn, id_tarima, peso_kg, ruta, nuevo_x, nuevo_y):
    t_inicio = time.perf_counter()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Seguridad: rechazar si supera 10 kg
    if peso_kg > 10.0:
        cursor.execute("UPDATE tarimas SET "
            "estado='BLOQUEADA_SOBREPESO', "
            "ultima_actualizacion=? WHERE id_tarima=?",
            (ahora, id_tarima))
        cursor.execute("INSERT INTO registro_rechazos_seguridad "
            "(id_tarima, peso_detectado_kg, motivo, fecha_hora) "
            "VALUES (?, ?, ?, ?)", (id_tarima, peso_kg,
            "EXCEDE_LIMITE_10KG_ACTUADOR_PROTEGIDO", ahora))
        conn.commit()
        return
    # Carga válida: actualizar peso y coordenadas
    cursor.execute("UPDATE tarimas SET peso_kg=?, "
        "coord_x_cm=?, coord_y_cm=?, estado='UBICADA_DESTINO', "
        "ultima_actualizacion=? WHERE id_tarima=?",
        (peso_kg, nuevo_x, nuevo_y, ahora, id_tarima))
    latencia_ms = (time.perf_counter() - t_inicio) * 1000
    # Registrar el movimiento en el historial
    cursor.execute("INSERT INTO historial_movimientos "
        "(id_tarima, ruta, destino_x_cm, destino_y_cm, "
        "peso_kg, latencia_ms, fecha_hora) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)", (id_tarima, ruta,
        nuevo_x, nuevo_y, peso_kg, round(latencia_ms, 2), ahora))
    conn.commit()
```

### Consulta y simulación

```python
def mostrar_estado_bodega(conn):
    cursor = conn.cursor()
    for fila in cursor.execute(
            "SELECT id_tarima, peso_kg, coord_x_cm, coord_y_cm, "
            "estado, ultima_actualizacion FROM tarimas"):
        coord = f"({fila[2]:.0f}, {fila[3]:.0f}) cm"
        print(f"{fila[0]:<10} | {fila[1]:<10.2f} | "
              f"{coord:<16} | {fila[4]:<22} | {fila[5]}")

if __name__ == "__main__":
    conexion = inicializar_bd()
    mostrar_estado_bodega(conexion)

    # Paquetes que mandaría el ESP32
    time.sleep(1)
    procesar_paquete_esp32(conexion, "TAR-101", 8.45, "RUTA_1", 150.0, 120.0)
    time.sleep(1)
    procesar_paquete_esp32(conexion, "TAR-102", 11.80, "RUTA_2", 90.0, 120.0)  # > 10 kg
    time.sleep(1)
    procesar_paquete_esp32(conexion, "TAR-103", 6.20, "RUTA_3", 150.0, 0.0)

    mostrar_estado_bodega(conexion)
    conexion.close()
```

**Resultado de la demo:** TAR-101 y TAR-103 quedan en `UBICADA_DESTINO` con sus coordenadas nuevas; TAR-102 queda `BLOQUEADA_SOBREPESO` y aparece en `registro_rechazos_seguridad`. Cada escritura tarda ~1 ms.

### Lo que falta para la Web API
- Un endpoint Flask `POST /api/actualizar_tarima` que reciba el JSON del ESP32 y llame a la lógica de `procesar_paquete_esp32`.
- Endpoints de lectura para el tablero.
- Que el ESP32 mande lo que la tabla exige (ruta, origen) o quitar el `NOT NULL`.

---

## Anexo D. Preguntas probables y cómo responder

**Resumen para abrir la parte del ESP32 (~20 s):** "El ESP32 es el que ejecuta. Recibe órdenes de la Raspberry por UART: levantar, mover, detener y depositar. Antes de levantar pesa la tarima y la rechaza si pasa de 10 kg. Al depositar, manda la nueva posición a la base de datos por Wi-Fi."

| Pregunta | Respuesta |
|---|---|
| ¿Por qué dos procesadores? | La Raspberry piensa (cámara, mapa, rutas) y el ESP32 controla en tiempo real (motores, sensores, seguridad). Si la Raspberry se traba, el freno por obstáculo y el límite de peso siguen funcionando. |
| ¿Para qué sirven los encoders si no se usan? | Hoy solo cuentan pulsos. El siguiente paso es convertirlos a distancia (pulsos × perímetro ÷ pulsos por vuelta) para corregir la trayectoria. |
| ¿Qué pasa mientras levanta? | Los `delay()` bloquean ~8.5 s y no escucha a la Raspberry. Es aceptable porque el robot está detenido; la mejora es usar `millis()`. |
| ¿El PWM es a 5 kHz? | El código usa la frecuencia por defecto de `analogWrite`. Fijarla con `analogWriteFrequency()` está pendiente. |
| ¿La latencia medida es la del criterio? | Solo mide envío y respuesta. El criterio va desde que se deja la tarima hasta que la BD se actualiza; se medirá con la Web API funcionando. |
| ¿Por qué `enviarActualizacionBD` se usa antes de definirse? | El IDE de Arduino declara solas las funciones de un `.ino` antes de compilar. |
| ¿Qué tan seguro es el límite de 10 kg? | Depende de la calibración. Si el HX711 falla, la función regresa 0 kg y la tarima se levantaría; distinguir "sin lectura" de "0 kg" es una mejora pendiente. |
| ¿Existe la Web API? | Todavía no; la base es local y los paquetes son simulados. |
| ¿La navegación cumple 5 cm? | Hoy es en lazo abierto; se va a cerrar con encoders y corregir con LIDAR/QR. |
| ¿Hay tablero en tiempo real? | Los indicadores están definidos; el tablero aún no está conectado. |

---

## Anexo E. Historial de versiones del armado

| Fecha | Versión | Cambios principales |
|---|---|---|
| 9-nov | Armado v1 (sin base) | LiPo 3S 5000 mAh con XT60 → fusible 15 A → paro de emergencia → bus 12 V. Buck 5 V/5 A USB-C PD para la Pi y LM2596 a 5 V para el ESP32 (por VIN) y la lógica del BTS7960. Raspberry con microSD. |
| 9-nov | "Más sencillo" | Se quita el paro de emergencia porque es solo una prueba; se deja el fusible. Se sugiere probar primero solo el ESP32 sin la Pi. |
| 10-nov | Batería | Se elige la OVONIC 3S 2200 mAh 25C con conector T (paquete de 2) y conectores T Hobbypark; cargador Tosiicop. |
| 11-nov | Armado final (rev. 28) | Sin fusible, paro ni alarma; sin regletas (empalmes en los tornillos de los módulos); ESP32 alimentado por micro-USB desde la Pi (adiós LM2596); SSD M.2 directo en la Pi por PCIe (sin microSD); BTS7960 a 3.3 V; UART Pi–ESP32 con 3 cables; `dtparam=uart0=on` y `PSU_MAX_CURRENT=5000`. |
| 11-nov | Depuración de sensores | Ningún sensor respondía: ESP32 corrido una fila, posible falta de GND al riel, GND del HC-SR04 en la columna +, divisor mal armado. |

**Reglas que se mantuvieron en todas las versiones:** nunca alimentar el ESP32 por USB y por VIN a la vez; tierra común entre todo; 12 V nunca dentro de la protoboard; encoders a 3.3 V; Echo siempre por divisor.

---

## Anexo F. Cálculos de factibilidad a detalle

### Motores GA25-370 (12 V, 130 RPM, 46.8:1)
- Con ~9–10 V tras el L298N y 14 kg en total: 0.7–2 kgf·cm por motor → **0.2–0.28 m/s**, **0.2–0.55 A** cada uno. Margen ~2–3× sobre lo necesario.
- Ruedas locas de bola sucias pueden pedir 50–80 % del par de arranque (stall). **Solo piso liso.**
- Con ≥ 25 % del peso sobre las ruedas motrices hay ~**21 N** de tracción contra **8–12 N** necesarios.
- La rueda motriz va pegada a la caja: el eje de 4 mm queda en voladizo y no hay dato de carga radial.

### Actuador (75 kg, 750 N, 50 mm)
- Carga: 10.8 kg × g ≈ **106 N = 14 %** de su capacidad.
- Carrera de 50 mm en **~5–6 s** (cumple < 10 s). Timeout de software ~8 s.

### Batería OVONIC 3S 2200 mAh
- Energía: 11.1 V × 2.2 Ah ≈ **24.4 Wh**; útil (80 %) ≈ **19.5 Wh**.
- Consumo de 5 V: Pi (7–11 W) + SSD (~1.5 W) + LIDAR (1.5–2 W) + ESP32 (~0.6 W) + cámara (~1 W) + sensores (~0.2 W), con buck al 90 %.
- **Típico manejando ~50 min · peor caso ~30 min.**
- Olvidada prendida en reposo baja al 20 % en unas horas y luego se sobredescarga: **desconectar el conector T al terminar.**

### Odometría y precisión
- Encoder: 11 pulsos × 46.8 = **~515 pulsos por vuelta** (un canal, flanco de subida).
- Perímetro de la rueda: π × 65 mm ≈ **204 mm** → **~0.40 mm por pulso** (0.10 mm con cuadratura ×4).
- **1° de error de rumbo** = ~1.7 cm de desvío lateral por metro.
- **Ruedas con 0.5 mm de diferencia** de diámetro → ~6 cm de desvío en 2 m.
- **Llanta aplastada 1 mm** con carga → ~3 % de error → ~6 cm en 2 m.
- **Lazo abierto (0.8 s por celda):** la velocidad cambia mucho entre batería llena sin carga y batería baja con carga, así que la distancia recorrida varía; no cumple 5 cm.
- **Solución:** calibrar mm/pulso y la vía (distancia entre ruedas) con y sin carga; corregir con LIDAR (pared) o QR en el destino; rutas cortas.

### Apoyos, LIDAR y tarima
- 2 motrices + 4 locas = 6 apoyos (hiperestático): dejar 2 locas (adelante y atrás) o subirlas 1–2 mm.
- LIDAR abajo al frente, fuera de la plataforma; es ciego a < 15 cm; enmascarar las patas de la tarima.
- Tarima: claro libre ≥ 20 cm, ≥ 40 cm entre patas, sin travesaño en la entrada, fondo plano.

### Código
- Interrupción solo en el canal A (GPIO 34/35): los GPIO 36/39 tienen una errata con el Wi-Fi activo.
- GPIO 14 a LOW al inicio de `setup()`.
- POST HTTP fuera del lazo de control.
- Si hay PWM y los encoders no cuentan en ~0.5 s → PWM a 0 (cubre atascos).

---

## Anexo G. Referencia rápida

### Raspberry Pi 5

```bash
# Actualizar sistema y firmware
sudo apt update && sudo apt full-upgrade -y
sudo rpi-eeprom-update -a

# Ver discos (debe aparecer nvme0n1)
lsblk

# Configuración de arranque y corriente
sudo rpi-eeprom-config --edit      # BOOT_ORDER=0xf416, PSU_MAX_CURRENT=5000
sudo nano /boot/firmware/config.txt # dtparam=uart0=on

# Puertos serie
ls /dev/serial/by-id/
python3 -m serial.tools.miniterm /dev/ttyAMA0 115200

# Cámara y voltaje
rpicam-hello
vcgencmd get_throttled             # debe dar throttled=0x0

# Apagar
sudo shutdown now
```

### Valores clave

| Concepto | Valor |
|---|---|
| Velocidad UART Pi–ESP32 | 115200 baudios |
| Dirección I2C del VL53L1X | 0x29 |
| Límite de peso | 10 kg |
| Distancia de paro (HC-SR04) | 12 cm |
| Voltaje mínimo de la LiPo en reposo | ~10.8 V (3.6 V por celda) |
| Voltaje de salida del buck de la Pi | 5.1 V |
| Celda del mapa | 30 × 30 cm |
| Factor de calibración inicial (firmware original) | 2280.0 |
| Factor de calibración inicial (código de prueba) | 420.0 (se reemplaza con `c <gramos>`) |
| Colores de resistencias | 1 kΩ café-negro-negro-café · 2 kΩ rojo-negro-negro-café |

### Librerías de Arduino
- **HX711 Arduino Library** (Bogdan Necula)
- **VL53L1X** (Pololu)
- `WiFi.h` y `HTTPClient.h` (vienen con el paquete ESP32)
- Placa: **ESP32 Dev Module**

---

## Anexo H. Línea de tiempo del proyecto

| Fecha | Qué pasó |
|---|---|
| 10-oct-2026 | Project Charter y WBS |
| 20-oct | Revisión completa del proyecto: 13 problemas detectados |
| 21-oct | Presentación de avance: diapositivas del firmware, Raspberry y BD; 7 secciones; versión final de 37 diapositivas |
| 3-nov | Presentación de medio término |
| 7-nov | Compra de sensores y actuadores: celda 20 kg, VL53L1X, GA25-370, actuador 75 kg 50 mm |
| 9-nov | Configuración del SSD de la Pi; primer armado en banco; código de prueba de sensores |
| 10-nov | Elección y compra de la batería |
| 11-nov | Armado final (rev. 28), análisis de factibilidad, depuración de sensores y este documento |
