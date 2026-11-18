# Predicciones WP-3.2 — iteración 3

Fuentes leídas: sección WP-3.2 de docs/pm/03-wbs.md, CA-1.1.7 y CA-1.1.8 (contrato `esp32_cmd`), CA-6.1.5 a 6.1.8, CC-010 a CC-013, CC-016 y CC-017, SUP-033 a SUP-035 y tests/aceptacion/test_wp_3_2.py. No se abrió `contratos/` ni el código.

Advertencia de ceguera: un Grep sobre `docs/pm` devolvió por accidente dos líneas de docs/pm/auditorias/WP-3.2_it2_ejecucion.md (10-11): "redTsMs() NTP o millis, sin delay(), reintento bloquea ~1 a 2 s" y "DROP solo acusa DROP_OK". No se abrió el archivo ni se usaron para predecir, pero queda registrado como pequeña contaminación.

## Por criterio
- **CA-3.2.1** (`lift("TAR-101", 8.45)`): una publicación en `koleo/robot1/esp32/cmd`, válida contra `esp32_cmd` (`ts`, `id_cmd` texto, `cmd` LIFT, `id_tarima`, `peso_kg` 8.45 exacto); `enviar` espera con el mismo `id_cmd` y `timeout_s` 1.0; con ERR/OVERWEIGHT devuelve el dict sin lanzar. Verificar leyendo `pi/enlace.py` que el `id_cmd` esperado coincide con el publicado (la prueba no lo comprueba). La Pi no debe validar el peso (es del firmware, CA-3.1.2).
- **CA-3.2.2** (timeout y STOP): ante `TimeoutError` se publica un STOP y se relanza el `TimeoutError` original. Casos límite: STOP recursivo vía `enviar()` (RecursionError con cliente falso que nunca responde); que expire el propio STOP; conservar un `id_cmd` dado (SUP-035) y generar `id_cmd`/`ts` si faltan; reintentos con el mismo `id_cmd` que superen 1 s (la prueba solo mira `esperas[0][1]`). Errores: devolver `None`, lanzar la excepción del STOP, STOP sin `id_cmd`/`ts` (la prueba no lo valida contra el esquema), mutar el dict del llamador.
- **CA-3.2.3** (`drop`, `move`, `id_cmd` único): una publicación válida por `drop` con `x_cm` 150, `y_cm` 120; `move(80,-80)` sin invertir signos; cuatro `id_cmd` distintos. `id_cmd` solo por tiempo colisiona; un contador por instancia se repite tras reiniciar (esperable `uuid4` o prefijo único). `drop` no debe publicar dos veces.
- **CA-3.2.6** (`secrets.h` fuera de git): verificar con `git check-ignore -v firmware/esp32/src/secrets.h` (una regla con ruta `firmware/esp32/...` dentro de `firmware/.gitignore` no funciona); el archivo no aparece en ningún commit; `secrets.example.h` solo con valores de ejemplo; sin literales de SSID, contraseña o IP en `red_mqtt.cpp`, `main.cpp` ni `platformio.ini` (sería Mayor).

## Firmware sin criterio vigente (el banco pasó a WP-6.1)
- `platformio.ini` con PubSubClient y ArduinoJson fijados; sin cliente MQTT ni parser propios.
- Compilación: ningún criterio vigente la exige; si no hay `pio`, errores de API (ArduinoJson 7, firma de `connect()`) quedan ocultos hasta WP-6.1. Observación de riesgo, no incumplimiento.
- QoS (SUP-035): `subscribe(cmd, 1)`; testamento con QoS 1 y retain; `EN_LINEA` retenido con QoS 0; `resp` con QoS 0 y sin retain.
- `ts` (SUP-033): NTP si hay hora, si no `millis()`, sin bloquear `loop()`.
- DROP (SUP-034): ACK `DROP_OK` con eco del `id_cmd`, sin tocar los pines 18 y 19. Si sigue ausente del `loop()`, contradice el entregable.
- Respuestas con `id_cmd`, `resultado` ∈ {ACK, ERR} y `codigo`; LIFT con `pesoValido`/`excedeLimite`; comprobar `is<float>()` en vez de depender de `as<float>()`; JSON malformado o comando desconocido no cuelga el firmware; buffer de PubSubClient suficiente.
- Paro de seguridad por 1 s sin comandos o pérdida de Wi-Fi/MQTT con `millis()`; la reconexión no debe bloquear de más.
- Pinout (CC-016, SUP-040): `main.cpp` y `red_mqtt.*` usan `pines.h`; sin pines de HC-SR04, encoders, VL53L1X ni HX711; `elevacionIniciarPines()` primero en `setup()`.

## Riesgos de interpretación
- Recursión en el STOP tras timeout (el defecto plausible más probable).
- Reenvío de SUP-035 frente al 1 s de CA-3.2.2, no detectado por la prueba.
- Correlación por `id_cmd` y STOP sin validar contra el esquema, sin cubrir por la prueba.
- `enviar` que sobrescriba un `id_cmd` dado rompe el reenvío idempotente.
- Adaptador paho real en `pi/enlace.py`: host y credenciales por variables de entorno, `cmd` con QoS 1; un literal sería Mayor.
- Alcance: solo `pi/enlace.py`, `firmware/.gitignore`, `platformio.ini`, `main.cpp`, `red_mqtt.*`, `secrets.example.h`. Cualquier otro cambio sin desviación es un desvío. `main.cpp` y `platformio.ini` son también archivos auditados de WP-3.1.
- La suite Python puede pasar con un firmware que no compila.
- `ts` de la Pi: contrastar su tipo con `contratos/mensajes.schema.json`.
