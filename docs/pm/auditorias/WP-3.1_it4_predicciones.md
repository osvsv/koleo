# Predicciones WP-3.1 — iteración 4
(Escritas por el auditor antes de ver el código corregido; guardadas por el orquestador, resumidas.)

Contexto: la it3 quedó NO CONFORME por H-1 [Mayor] (redActualizar() bloquea loop() y el corte de elevacionActualizar() puede llegar después de 8 s). Corrección elegida: esp_timer one-shot en elevacion.cpp, independiente de loop() y de la red. Por la regla de hallazgos congelados, en la it4 solo se evalúa el cierre de H-1, la regresión y hallazgos nuevos Mayores.

## CA-3.1.6
- Creación: esp_timer_create una sola vez en elevacionIniciarPines(), handle estático, se comprueba el esp_err_t; si falla, el resultado debe ser seguro (LIFT no energiza o no responde LIFT_OK sin protección). Llamarla dos veces no debe crear un segundo timer.
- Armado: en el mismo punto donde se energiza, solo después de validar el peso. Unidades: microsegundos (8 000 000); un valor mayor que 8 s sería Mayor.
- Sin rearme por LIFT repetido: esp_timer_stop seguido de start_once reabriría H-3 (Mayor).
- Cancelación: esp_timer_stop al terminar la elevación; ESP_ERR_INVALID_STATE debe tolerarse. Un callback viejo no debe cortar una elevación nueva sin dejar el estado coherente.
- El callback debe actuar sobre el hardware (pines en LOW y estado inactivo); si solo levanta una bandera que lee loop(), H-1 no se cierra (Mayor). Sin delay, Serial ni MQTT en el callback.
- Concurrencia (doble núcleo): estado volatile y secciones críticas (portMUX); buscar que loop() no vuelva a escribir HIGH tras el corte (Mayor). Despacho por tarea, no ISR.
- millis() y delay(): elevacionActualizar sigue con millis() como respaldo (resta sin signo, >= 8000UL); sin delay() en elevacion.cpp.
- Lógica probable en host con pruebas: 7999 no corta, 8000 corta, desbordamiento de millis(), LIFT repetido no reinicia, tras el corte un elevacionActualizar posterior no reenergiza. Código ESP32 detrás de #ifdef con stub de host.

## CA-3.1.1
pines.h sin cambios; pinMode y digitalWrite(PIN_MD_ENB, LOW) siguen primero en elevacionIniciarPines(); la creación del timer va después. main.cpp sigue llamándola primero en setup().

## CA-3.1.2
elevacionSolicitar mantiene el orden: validación, sobrepeso (> 10.0 inclusivo, SUP-010), y solo entonces energiza y arma. PESO_INVALIDO y OVERWEIGHT no arman el timer ni tocan pines. Riesgo: que la refactorización mueva el armado antes de la validación o cambie firmas o códigos.

## Interfaz
Se mantienen pesoValido(float), excedeLimite(float), LIFT_OK, OVERWEIGHT y PESO_INVALIDO. Funciones nuevas aceptables si no rompen a main.cpp de WP-3.2. Idealmente no se toca main.cpp ni red_mqtt.*; si se tocan, WP-3.2 se reverifica.

## Riesgos de interpretación
- Corte no independiente (solo bandera) no cierra H-1 aunque pasen las pruebas de host.
- Confundir µs con ms: verificar la constante en el código, no en la prueba de host.
- Rearme con LIFT repetido reabre H-3.
- Reenergizado tras el corte por carrera entre núcleos: revisar cada digitalWrite HIGH del actuador.
- Alcance del "actuador": si DROP o el descenso usan el mismo actuador y no pasan por el timer, el límite no los cubre (solo sería hallazgo si es Mayor y demostrable).
- Verificabilidad (H-5, Observación): sin compilación para ESP32 ni prueba en hardware; orden de inicializadores designados de esp_timer_create_args_t y versión del core de Arduino-ESP32; las pruebas de host solo demuestran la lógica.
- Confirmar dónde consta que las pruebas de host corrieron, ya que run_acceptance.py no ejecuta test_elevacion.cpp.
- Comprobar que test_elevacion.cpp no pierde ni relaja casos de it1 e it2.
- El residuo `10.0)` en la raíz hará que el log marque "Árbol limpio: no".
