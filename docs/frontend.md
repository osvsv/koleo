# KOLEO — Documento de frontend

> **Copia pendiente.** La versión completa vive en Claude: https://claude.ai/artifact/9hMH13nyBzYAM8bbxm8zZM . Este archivo se reemplazará con el documento completo en cuanto se pueda exportar. Mientras tanto, este es el resumen.

## Decisiones tomadas

- **Un solo robot** en la demo.
- **Sin login ni roles.**
- El backend envía **telemetría en vivo** (posición, velocidad, obstáculos) y recibe **órdenes** (iniciar, cancelar, paro).
- **Tiempo real con MQTT**, no con consultas periódicas: la interfaz se conecta al broker por **WebSocket con mqtt.js**.
- Los nombres de datos siguen el diagrama E-R de `historial_movimientos`.

## Contenido del documento completo

- Alcance y perfiles de usuario.
- Requisitos funcionales RF-01 a RF-15.
- 8 pantallas en cuatro módulos: **Flotilla, Monitoreo, Control y Gestión logística** (Tarimas, Rutas completadas).
- Flujos principales.
- Tipos TypeScript y endpoints supuestos.
- Arquitectura: React + Vite + TypeScript + Tailwind, React Router, TanStack Query, Zustand, MSW para datos falsos, Recharts y mapa en SVG.
- Plan en 4 fases.

## Sistema visual

Estilo **Visitors** de Refero: claro y plano.

| Uso | Color |
|---|---|
| Acción principal | lavanda `#918df6` |
| Éxito / en destino | verde `#33c758` |
| Advertencia | ámbar `#ffa600` |
| Paro y sobrepeso | rojo `#ff3e00` |

Tipografía Inter (JetBrains Mono para IDs). Ver los [wireframes](wireframes/README.md).
