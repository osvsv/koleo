# Evidencia de banco pendiente — WP-3.1

La aportan personas, con el firmware compilado con PlatformIO (aún no compilado para ESP32).

- `peso_invalido.txt` (CA-3.1.3): salida serie de `LIFT` sin peso -> `PESO_INVALIDO`, actuador sin energizar.
- `umbral.txt` (CA-3.1.5): `LIFT 11.8` y `LIFT 10.1` -> `OVERWEIGHT`; `LIFT 10.0` y `LIFT 0.1` -> `LIFT_OK`.
