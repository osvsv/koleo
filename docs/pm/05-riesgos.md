# Registro de riesgos — KOLEO
Versión: 1.2 (G1, respuestas de Osvaldo aplicadas; CC-004)

| ID | Riesgo | Probabilidad | Impacto | Mitigación | WP |
| --- | --- | --- | --- | --- | --- |
| RK-01 | El ensamble mecánico (chasis, elevación) no queda listo: bloquea VAL-01 y 03 a 07. Hoy es un armado básico en banco y nada ha funcionado bien. | Alta | Alto | Hacerlo primero (Inc. 1); probar por niveles (banco, subsistema, robot); regla de puerta: si no cierra, recortar alcance, no acumular atraso. | WP-2.1, WP-2.2 |
| RK-02 | Quemar ESP32/Pi o la LiPo por energizado inseguro (sin paro físico, tierra, divisor ECHO). | Media | Alto | Lista antes de energizar; fusible de 10 A; prueba de cortos con multímetro; un cambio a la vez. | WP-2.3 |
| RK-03 | Un `LIFT` sin peso declarado válido se tomaría como 0 kg y la elevación continuaría (CC-004: ya no hay báscula). | Media | Alto | `LIFT` exige `peso_kg` válido; sin él responde PESO_INVALIDO y no energiza el actuador. | WP-3.1 |
| RK-04 | Navegación en lazo abierto no cumple <10 cm. | Alta | Alto | Encoders con calibración con y sin carga; reportar medición real si no se alcanza (DP-13). | WP-4.2, WP-6.2 |
| RK-05 | Cerrado en G1: el Reto IoT exige microcontroladores en red y ahora el ESP32 se conecta él mismo a la red (V-06). | — | — | Cerrado | WP-3.2 |
| RK-06 | Picos de corriente reinician Pi o ESP32; USB de la Pi cerca de su límite (1.6 A). | Media | Medio | ESP32 por USB desde la Pi; medir consumo; tierra común. | WP-2.3 |
| RK-07 | Latencia mal medida (solo la escritura local). | Media | Medio | `ts` en origen y recepción; definición SUP-011. | WP-1.3, WP-6.1 |
| RK-08 | Calendario: 3 semanas, 5 personas con 4 a 6 h por semana cada una (≈ 60 a 90 h de equipo); el plan completo probablemente excede esa capacidad. | Alta | Alto | Se mantienen los 19 WP y se recorta por puerta (DP-17); orden de recorte sugerido [S]: WP-5.2, WP-4.4 y rutas 2 y 3. | Todos |
| RK-09 | Presupuesto sin margen para repuestos. | Media | Medio | No comprar piezas nuevas; reparar antes de reemplazar. | WP-6.3 |
| RK-10 | Contradicciones heredadas entre documentos (C1 a C11 del diagnóstico) generan rework. | Media | Medio | Validar en G1 los [S] de mayor impacto. | G1 |
| RK-11 | Fecha del plan importado inconsistente (18-nov es miércoles). | Alta | Bajo | Calendario propio de este perfil (DP-12). | Perfil |
| RK-12 | El ESP32 recibe comandos por Wi-Fi: la latencia o la pérdida de red pueden retrasar un STOP enviado desde la Pi. | Media | Alto | El paro por obstáculo y el paro por pérdida de comandos o de red corren en el ESP32, sin depender de la red. | WP-3.2, WP-3.3 |
| RK-13 | Cerrado en CC-004: la celda de carga salió del proyecto (falla del HX711). | — | — | Cerrado | WP-3.1 |
| RK-14 | Con el peso declarado, un peso mal registrado en el tablero deja pasar una tarima pesada o rechaza una ligera; el robot no puede detectarlo. | Media | Medio | Aceptado: el peso se verifica solo como dato declarado (CC-004); registrar el peso real de la carga de demostración (0.1 kg) y documentar la limitación en el reporte. | WP-3.1, WP-4.1, WP-6.1 |
