# KOLEO

Robot móvil semiautónomo para transportar tarimas (curso IoT, Tec de Monterrey GDL). Entrega: 2026-12-02.

## Método PM

Este proyecto se gestiona con el Método PM. La línea base está en `docs/pm/`.

- Ejecuta trabajo solo por paquetes de `docs/pm/03-wbs.md`, con `/pm-ejecutar`.
- Nada se considera terminado sin dictamen CONFORME del auditor y evidencia en
  `docs/pm/evidencia/`.
- Desde `baseline-v1.0`, la línea base solo cambia por `/pm-cambio`.
- `docs/pm/estado.md` es generado; no lo edites a mano.
- Las credenciales (contraseña de Wi-Fi, etc.) van en variables de entorno, nunca en el repositorio.
- Si algo contradice la línea base, detente y propón una solicitud de cambio.
- Los WP de tipo `integracion` son físicos. Las personas hacen WP-2.1, 2.2 y 2.3; WP-2.4, 6.1, 6.2 y 6.3 los ejecuta el agente desde la Raspberry Pi con una persona presente (DP-09, CC-009). Su evidencia va a `docs/pm/evidencia/hw/<WP>/`.
