# Evidencia de WP-5.1 — método y límites

Capturas tomadas el 2026-11-13 con el navegador automatizado, sobre `npm run dev` (Vite, puerto 5173, proxy de `/api` al backend en 5000) y el backend Flask real (`crear_app`) contra una BD SQLite temporal fuera del repositorio. La BD se sembró con `simulador.robot_falso.generar_mision` (RUTA_1 con 8.45 kg y RUTA_2 con 11.80 kg) alimentando `procesar_mensaje` directamente, sin broker MQTT, más una misión RUTA_1 a medias con una orden INICIAR aceptada. Los `ts` del simulador quedan en el futuro respecto de la recepción, por eso `latencia_red_ms` sale negativa en esta siembra; no afecta al tablero.

| Archivo | Criterio | Qué muestra |
| --- | --- | --- |
| `build.txt` | CA-5.1.1 | Salida de `npm run build` (código 0), con códigos de color ANSI |
| `flotilla.png` | CA-5.1.2 | robot1: EN_LINEA, EN_RUTA y su alerta TAR-102 SOBREPESO 11.8 kg |
| `monitoreo.png` | CA-5.1.3 | Peso declarado 8.45 de 10 kg, velocidad 20 cm/s, ruta RUTA_1 e historial reciente |
| `indicadores_antes.png`, `indicadores_despues.png` | CA-5.1.4 (parcial) | Seis indicadores antes y después de publicar una telemetría nueva (posición (0, 90) → (90, 120), peso 8.4 → 6.2 kg, velocidad 20 → 35 cm/s) |
| `sin_conexion.png` | CA-5.1.5 | Con el backend detenido: banner "Sin conexión con el backend", sin datos |

## Límites
- **CA-5.1.4 pide `indicadores.mp4` y no existe.** El navegador automatizado solo exporta GIF y no hay herramienta de video en este entorno. Las dos capturas muestran que los indicadores cambian tras publicar la telemetría; se publicó a las 08:19:40.9 y la captura "después" se tomó tras una espera de 1.5 s más la latencia de la herramienta. Es una evidencia aproximada: no mide el tiempo con precisión ni sustituye el video con el cronometraje del criterio. Falta que una persona grabe el video, o que se acepte la sustitución con un cambio de criterio.
- La siembra usa la BD directamente, sin MQTT ni robot real.
