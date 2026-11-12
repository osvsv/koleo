# Revisión externa — demo-1 (para pegar en claude.ai)

**Encargo para el revisor:** Revisa este paquete de validación antes de que lo responda. Señala: (a) preguntas que junten dos decisiones; (b) opciones sesgadas o que falten; (c) supuestos de alto impacto que no se preguntan; (d) recomendaciones que no se sostienen. No respondas las preguntas por mí.

## Contexto mínimo
- **Proyecto:** KOLEO, un robot móvil semiautónomo que sube, transporta y deposita tarimas de hasta 10 kg y registra cada movimiento en una base de datos (curso de IoT, 5 personas, entrega final tentativa el 2-dic-2026).
- **Nivel de rigor:** Estándar. La línea base ya fue congelada (G1); toda corrección de lo que se valida aquí pasa por una solicitud de cambio.
- **Punto de validación:** demo del incremento 1 (contratos de datos, robot simulado y backend de persistencia, con los tres paquetes de trabajo auditados como conformes).
- **Quién responde:** los 5 integrantes del equipo, en sesión con el robot simulado. Presupuesto: 20 minutos.
- **Origen de varias decisiones:** un modelo (el agente que implementó el backend) tomó supuestos donde la línea base no definía el comportamiento, y el responsable del proyecto los aprobó como decisiones. El equipo todavía no los ha visto.

## Decisiones en juego
| ID | Pregunta | Decide | Impacto |
| --- | --- | --- | --- |
| V-01 | ¿Con tres misiones simuladas (8.45, 11.80 y 6.20 kg) la base debe terminar con 2 tarimas entregadas, 1 bloqueada por sobrepeso, 2 filas de historial y 1 de rechazo? | Resultado que debe mostrar la demo del incremento | Alto: criterio de salida |
| V-02 | ¿10.0 kg se acepta y 10.1 kg se rechaza? | Límite inclusivo de peso | Alto: requisito crítico |
| V-03 | ¿Los destinos de las rutas 1, 2 y 3 en el simulador son (fila 4, col 5), (2, 3) y (3, 4)? | Destinos de rutas 2 y 3 en el simulador | Medio: el mapa real debe coincidir |
| V-04 | Latencia negativa por relojes desfasados: A guardarla tal cual con aviso, B guardar 0 con aviso | Tratamiento de latencia negativa | Medio |
| V-05 | "Ocupación": A tarimas entregadas / tarimas registradas, B celdas ocupadas / 30 celdas | Definición de ocupación | Medio |
| V-06 | Tiempo de ciclo = de levantar a depositar, en segundos | Definición de tiempo de ciclo | Medio |
| V-07 | Precisión de llegada = distancia entre la última posición reportada y el destino registrado | Definición del indicador de precisión | Alto: puede confundirse con la meta oficial de < 10 cm, que se mide con regla |
| V-08 | Posición guardada en un rechazo por sobrepeso = última posición reportada, o vacía | Coordenadas del rechazo | Bajo |
| V-09 | Ruta en el historial: A solo el nombre, B lista de celdas | Contenido de la ruta ejecutada | Medio: B cambia el esquema de la base |
| V-10 | ¿El robot reporta posición y estado 2 veces por segundo? | Frecuencia de telemetría | Medio |

## Supuestos que quedan fuera por presupuesto (con su impacto)
- El tablero se actualiza por consulta cada 1 s y no por WebSocket (afecta tablero y control; 3 dependientes). No entra porque el tablero no es parte de este incremento.
- El backend es Flask con SQLite y corre en la Raspberry Pi o en una laptop, sin definir cuál (6 dependientes). Ya funciona en laptop; la decisión de dónde correrá la define el montaje físico.
- Los siete estados del robot (INACTIVO, EN_MISION, ELEVANDO, EN_RUTA, DEPOSITANDO, DETENIDO_OBSTACULO, ERROR) están sin confirmar (4 dependientes). Se ven en la demo pero no se preguntan por separado. ¿Debería entrar?
- Observaciones técnicas abiertas sin pregunta (por ser de implementación): un campo de texto libre en las respuestas del ESP32, un comentario desactualizado y falta de manejo de errores cuando el broker no responde.

## Recomendaciones del modelo
Ninguna: las preguntas describen alternativas sin marcar una preferida.
