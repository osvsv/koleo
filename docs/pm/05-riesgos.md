# Registro de riesgos — KOLEO
Versión: 1.0 (borrador previo a G1)

| ID | Riesgo | Probabilidad | Impacto | Mitigación | WP |
| --- | --- | --- | --- | --- | --- |
| RK-01 | El ensamble mecánico (chasis, elevación) no queda listo: bloquea VAL-01 y 03 a 07. Hoy es un armado básico en banco y nada ha funcionado bien. | Alta | Alto | Hacerlo primero (Inc. 1); probar por niveles (banco, subsistema, robot); regla de puerta: si no cierra, recortar alcance, no acumular atraso. | WP-2.1, WP-2.2 |
| RK-02 | Quemar ESP32/Pi o la LiPo por energizado inseguro (sin paro físico, tierra, divisor ECHO). | Media | Alto | Lista antes de energizar; fusible de 10 A; prueba de cortos con multímetro; un cambio a la vez. | WP-2.3 |
| RK-03 | La báscula devuelve 0.0 si falla y la elevación continuaría. | Alta | Alto | Distinguir "sin lectura" de 0 kg; error SCALE_FAIL y no energizar el actuador. | WP-3.1 |
| RK-04 | Navegación en lazo abierto no cumple <10 cm. | Alta | Alto | Encoders con calibración con y sin carga; reportar medición real si no se alcanza (DP-13). | WP-4.2, WP-6.2 |
| RK-05 | El Reto IoT exige microcontroladores en red y el ESP32 no se conecta (MQTT desde la Pi). | Media | Alto | Confirmar con el profesor que la Pi cuenta (SUP-001); si no, el ESP32 publica HTTP/MQTT directo. | WP-4.1, WP-1.3 |
| RK-06 | Picos de corriente reinician Pi o ESP32; USB de la Pi cerca de su límite (1.6 A). | Media | Medio | ESP32 por USB desde la Pi; medir consumo; tierra común. | WP-2.3 |
| RK-07 | Latencia mal medida (solo la escritura local). | Media | Medio | `ts` en origen y recepción; definición SUP-011. | WP-1.3, WP-6.1 |
| RK-08 | Calendario: 3 semanas, 5 personas, horas desconocidas. | Alta | Alto | Tres incrementos con puerta; recorte de alcance (QR, tablero de control) antes que atraso. | Todos |
| RK-09 | Presupuesto sin margen para repuestos. | Media | Medio | No comprar piezas nuevas; reparar antes de reemplazar. | WP-6.3 |
| RK-10 | Contradicciones heredadas entre documentos (C1 a C11 del diagnóstico) generan rework. | Media | Medio | Validar en G1 los [S] de mayor impacto. | G1 |
| RK-11 | Fecha del plan importado inconsistente (18-nov es miércoles). | Alta | Bajo | Calendario propio de este perfil (DP-12). | Perfil |
