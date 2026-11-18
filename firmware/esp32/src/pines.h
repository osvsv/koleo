// Pinout real del prototipo (CC-016): driver L293D + actuador BTS7960.
// CC-004: sin pines de HX711 ni de VL53L1X.
#pragma once

// Actuador lineal, BTS7960
#define PIN_ACT_RPWM 18  // sube
#define PIN_ACT_LPWM 19  // baja

// L293D motor izquierdo (EN = velocidad por PWM)
#define PIN_MI_EN 14  // debe ponerse en LOW al inicio del programa
#define PIN_MI_IN1 26
#define PIN_MI_IN2 25

// L293D motor derecho (EN = velocidad por PWM)
#define PIN_MD_EN 27  // debe ponerse en LOW al inicio del programa
#define PIN_MD_IN3 33
#define PIN_MD_IN4 32

// UART con la Pi
#define PIN_UART_RX2 16
#define PIN_UART_TX2 17

// Sin asignar (no cableados; se asignan en WP-2.4, SUP-040):
//  - HC-SR04 (TRIG/ECHO)
//  - Encoders de rueda
// Al asignarlos no se pueden repetir 14, 18, 19, 25, 26, 27, 32 ni 33.
// GPIO 12 (strapping) y GPIO 15 / SD0-SD3: no se usan.
