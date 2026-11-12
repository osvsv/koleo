# Paquete de validación — demo-1 (interno)

Punto: demo del incremento 1 (contratos, robot simulado y backend: WP-1.1, WP-1.2, WP-1.3, los tres Conformes).
Quién valida: el equipo (5 personas), en sesión con el robot simulado. Presupuesto: 20 min (perfil).
Cantidad: 10 preguntas (≈ 2 min cada una). Cada una decide exactamente una cosa.

Después de G1, toda corrección abre una solicitud de cambio con `/pm-cambio`; lo confirmado sin cambios puede pasar a [D] dentro de esa solicitud.

| ID | Pregunta | Formato | Decide (una sola decisión) | Afecta | Impacto |
| --- | --- | --- | --- | --- | --- |
| V-01 | Con tres misiones simuladas (RUTA_1 8.45 kg, RUTA_2 11.80 kg, RUTA_3 6.20 kg), ¿el resultado esperado en la base es: TAR-101 y TAR-103 ubicadas, TAR-102 bloqueada por sobrepeso, 2 filas de historial y 1 de rechazo? | Ejemplo | Que ese resultado es lo que debe mostrar la demo del incremento 1 (VAL-08) | EJ del REQ-F-008 y REQ-F-002, CA-1.3.4, CA-1.3.9 | Alto: es el criterio de salida del incremento |
| V-02 | Caso límite: ¿un peso de exactamente 10.0 kg se acepta y 10.1 kg se rechaza? | Ejemplo | Que el límite de 10 kg es inclusivo en la demo | SUP-010, CA-1.2.3 | Alto: rechazo por sobrepeso (requisito crítico) |
| V-03 | ¿Los destinos de las rutas del simulador son RUTA_1 → fila 4, columna 5 (150, 120 cm); RUTA_2 → fila 2, columna 3 (90, 60 cm); RUTA_3 → fila 3, columna 4 (120, 90 cm)? | Sí / No / Corregir | Los destinos de RUTA_2 y RUTA_3 en el simulador (RUTA_1 ya viene del plan) | CC-002, CA-1.2.7, CA-4.3.1 | Medio: el simulador y el mapa real deben coincidir |
| V-04 | Si el reloj del robot va adelantado respecto al servidor y la latencia sale negativa: ¿A, se guarda tal cual y se avisa en el registro; o B, se guarda 0 y se avisa? | A / B | Tratamiento de una latencia de red negativa | CC-003, CA-1.3.2, REQ-NF-003 | Medio: cambia lo que se reporta como latencia |
| V-05 | En el tablero, ¿"ocupación" es A, tarimas ubicadas en destino entre el total de tarimas registradas; o B, celdas ocupadas del mapa entre las 30 celdas? | A / B | Definición del indicador de ocupación | CC-003, CA-1.3.11, REQ-F-012 | Medio: lo que muestra el tablero |
| V-06 | ¿El tiempo de ciclo es el tiempo, en segundos, desde que el robot levanta la tarima hasta que la deposita? | Sí / No / Corregir | Definición del tiempo de ciclo | CC-003, CA-1.3.11 | Medio |
| V-07 | ¿La precisión de llegada es la distancia entre la última posición que reportó el robot y el destino con el que se registró el depósito? | Sí / No / Corregir | Definición del indicador de precisión | CC-003, CA-1.3.11, REQ-NF-002 | Alto: se confunde con la meta oficial de < 10 cm, que se mide con regla |
| V-08 | Si se rechaza una tarima por sobrepeso, ¿la posición que se guarda en el rechazo es la última posición reportada por el robot (y vacía si no reportó ninguna)? | Sí / No / Corregir | Qué coordenadas guarda un rechazo | CC-003, CA-1.3.12 | Bajo |
| V-09 | En el historial, ¿basta con guardar el nombre de la ruta (por ejemplo RUTA_1) o debe guardarse la lista de celdas recorridas? | A / B | Contenido de la ruta ejecutada en el historial | CC-003, CA-1.3.10, REQ-F-008 | Medio: cambia el esquema si se elige la lista |
| V-10 | ¿El robot reporta su posición y estado 2 veces por segundo (cada 500 ms)? | Sí / No / Corregir | Frecuencia de la telemetría | SUP-012, CA-1.2.5 | Medio: carga de red y tablero |

## Notas de diseño (internas)
- V-02 y V-03 son casos concretos de supuestos ya confirmados (SUP-010) o decididos en CC-002; se piden aquí con ejemplo para revalidarlos con quienes no estuvieron en G1.
- V-05, V-06, V-07, V-08 y V-09 son los supuestos que el ejecutor tomó y se aprobaron como [D] en CC-003; el equipo no los ha visto.
- V-10 es SUP-012, Pendiente, con 5 dependientes.
- Cada fila decide una sola cosa: V-05, V-06 y V-07 son tres indicadores distintos y no se juntan.
