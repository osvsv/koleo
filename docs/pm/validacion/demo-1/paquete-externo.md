# KOLEO — Revisión de la primera demo

Hola. Ya tenemos funcionando la parte de software que no depende del robot físico: un robot "de mentira" (simulador) que manda sus datos, y una base de datos que los recibe y los guarda. En la sesión lo veremos correr. Estas 10 preguntas son para confirmar que lo que hace es lo que esperamos. Tomará unos 20 minutos.

Responde con **sí**, **no** o la letra de la opción. Si algo no te parece, escribe qué cambiarías.

**1. Tres misiones de prueba.** Se simulan tres entregas: una tarima de 8.45 kg, otra de 11.80 kg y otra de 6.20 kg. ¿Es correcto que al final la base muestre esto?
- La tarima de 8.45 kg y la de 6.20 kg quedan "entregadas en su destino".
- La de 11.80 kg queda "bloqueada por sobrepeso".
- Hay 2 registros de movimientos y 1 registro de rechazo (el de 11.80 kg).

**2. Caso límite del peso.** El peso máximo es 10 kg. ¿Es correcto que una tarima de exactamente 10.0 kg **sí** se acepte y una de 10.1 kg **no**?

**3. Destinos de las rutas de prueba.** En el simulador, las rutas terminan aquí (fila, columna del mapa de 30 cm por celda):
- Ruta 1: fila 4, columna 5 (a 150 cm de lado y 120 cm de fondo).
- Ruta 2: fila 2, columna 3 (90 cm, 60 cm).
- Ruta 3: fila 3, columna 4 (120 cm, 90 cm).

¿Son los destinos que tendrán esas rutas en el mapa real?

**4. Retraso de red negativo.** A veces el reloj del robot va adelantado respecto al servidor y el retraso calculado sale negativo. ¿Qué se guarda?
- **A:** el número tal cual (negativo) y se deja un aviso en el registro.
- **B:** 0 y se deja un aviso en el registro.

**5. Ocupación.** En el tablero, ¿qué significa "ocupación"?
- **A:** tarimas ya entregadas entre el total de tarimas registradas.
- **B:** celdas ocupadas del mapa entre las 30 celdas.

**6. Tiempo de ciclo.** ¿Es el tiempo, en segundos, que pasa desde que el robot levanta la tarima hasta que la deja en su destino?

**7. Precisión de llegada.** ¿Es la distancia entre la última posición que reportó el robot y el destino con el que se registró la entrega? (Ojo: no es la medición con regla de la meta de menos de 10 cm.)

**8. Posición de un rechazo.** Cuando se rechaza una tarima por sobrepeso, ¿se guarda como posición la última que reportó el robot (y vacía si no reportó ninguna)?

**9. Ruta en el historial.** En el historial de movimientos, ¿qué debe guardarse de la ruta?
- **A:** solo su nombre (por ejemplo "RUTA_1").
- **B:** la lista de celdas por las que pasó.

**10. Frecuencia de reporte.** ¿El robot debe reportar su posición y estado 2 veces por segundo (cada medio segundo)?

---

**Ejemplo de cómo responder:** 1: sí · 2: sí · 3: no, la ruta 2 termina en fila 3 columna 3 · 4: A · 5: A · 6: sí · 7: no, debería ser… · 8: sí · 9: B · 10: sí
