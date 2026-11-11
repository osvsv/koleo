# KOLEO — Preguntas para el equipo (≈ 10 minutos)

Hola. Estamos fijando el plan del robot antes de empezar a construir. Cada pregunta se responde con una letra o con "sí / no / corregir". Si respondes "no" o "corregir", escribe qué cambiarías. Tiempo estimado: 10 minutos. Por favor responde antes de la sesión del lunes.

## Equipo y tiempo

**1.** Propuesta de responsables: mecánica, Álvaro · electrónica y energía, Miranda · programación del ESP32, Leo · Raspberry Pi, Elías · datos y tablero, Osvaldo. ¿Es correcto? (sí / no / corregir)

**2.** ¿Puedes dedicar al menos 10 horas por semana hasta el 2 de diciembre? (sí / no, cuántas)

**3.** ¿Ya tienen en su poder todas las piezas del listado final del 11 de noviembre? (sí / no, cuáles faltan)

## Tecnología

**4.** El software de la Raspberry Pi, el servidor de datos y el simulador se escribirían en Python. ¿Estás de acuerdo? (sí / no, cuál prefieres)

**5.** El "buzón" de mensajes (MQTT) necesita correr en algún equipo. ¿Dónde?
- A: en la Raspberry Pi del robot
- B: en una laptop del equipo
- C: otro (di cuál)

**6.** El reto del curso pide microcontroladores conectados en red. En nuestro plan, el ESP32 habla con la Raspberry Pi por cable y es la Pi la que se conecta a la red.
- A: el profesor ya confirmó que así cuenta
- B: no lo hemos preguntado
- C: el profesor dijo que el ESP32 debe conectarse él mismo a la red

## Seguridad

**7.** ¿Qué sensor detiene al robot ante un obstáculo?
- A: solo el sensor ultrasónico (HC-SR04); el lidar y Google Coral quedan fuera
- B: el ultrasónico y también el sensor de distancia láser (VL53L1X)
- C: el lidar en lugar del ultrasónico

**8.** El 11 de noviembre se decidió quitar el fusible. La batería puede entregar muchos amperes en un corto.
- A: instalar un fusible de 10 A (cuesta unos pocos pesos)
- B: mantener la decisión de no usar fusible

**9.** ¿A qué distancia de un obstáculo debe detenerse el robot?
- A: 12 cm
- B: 15 cm
- C: 20 cm

**10.** Si el sensor de obstáculos deja de dar lectura mientras el robot avanza, el robot se detiene por seguridad. ¿Es lo que esperas? (sí / no, qué debería pasar)

## Recorridos y pesos

**11.** El almacén de prueba es una cuadrícula de 5 filas por 6 columnas, con celdas de 30 cm. Tres recorridos: 1) de la esquina superior izquierda a la esquina inferior derecha; 2) de la fila 1, columna 3 a la fila 4, columna 5; 3) de la fila 5, columna 3 a la fila 1, columna 6. ¿Son los que se evaluarán? (sí / no / corregir)

**12.** Una masa de exactamente 10.0 kg: ¿el robot debe levantarla? (sí / no)

**13.** Con la báscula bien conectada y sin nada encima (0.0 kg), le piden al robot elevar. El robot no sube y avisa "sin carga". ¿Es lo que esperas? (sí / no, qué debería pasar)

## Datos

**14.** Cuando una tarima termina de depositarse, ¿qué estado se le asigna?
- A: "ubicada en destino"; "en piso" queda solo para tarimas recién registradas que aún no se movieron
- B: "en piso", igual que al registrarse; cambia solo su posición

**15.** El tiempo máximo de 2 segundos para actualizar la base de datos, ¿desde cuándo se cuenta?
- A: desde que la celda de carga detecta que la tarima ya se soltó
- B: desde que el actuador termina de bajar

**16.** Si el robot no puede leer el código QR de la tarima:
- A: no inicia el traslado
- B: usa el identificador asignado a la ruta, como en el prototipo
- C: la persona escribe el identificador en el tablero

**17.** Si el robot informa dos veces la misma entrega, el historial muestra una sola entrega. ¿Es lo que esperas? (sí / no)

## Metas y fechas

**18.** ¿Cuáles son las metas oficiales que se entregan al profesor?
- A: levantar 10 kg en menos de 15 s y llegar con error menor a 10 cm
- B: levantar 10 kg en menos de 10 s y llegar con error menor a 5 cm (las del documento original del proyecto)

**19.** Fechas de revisión con el robot: viernes 20 de noviembre, viernes 27 de noviembre y 30 de noviembre o 1 de diciembre; entrega el 2 de diciembre. ¿Son correctas? (sí / no / corregir)

---

**Ejemplo de cómo responder:** 1: sí · 2: no, 6 horas · 3: no, falta la celda de carga · 4: sí · 5: A · … · 19: corregir, el 27 no puedo
