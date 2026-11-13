// Pinout final del ESP32 (importado/KOLEO_todo.md §9).
// CC-004: sin pines de HX711 ni de VL53L1X.
#pragma once

// Actuador lineal, BTS7960
#define PIN_ACT_RPWM 25  // sube
#define PIN_ACT_LPWM 26  // baja

// L298N motor izquierdo
#define PIN_MI_ENA 32
#define PIN_MI_IN1 33
#define PIN_MI_IN2 27

// L298N motor derecho
#define PIN_MD_ENB 14  // debe ponerse en LOW al inicio del programa
#define PIN_MD_IN3 23
#define PIN_MD_IN4 13

// Encoders (GPIO 34-39: solo entrada, sin pull-up interno)
#define PIN_ENC_IZQ_A 34
#define PIN_ENC_IZQ_B 36
#define PIN_ENC_DER_A 35
#define PIN_ENC_DER_B 39

// HC-SR04 (ECHO por divisor 1k/2k)
#define PIN_US_TRIG 18
#define PIN_US_ECHO 19

// UART con la Pi
#define PIN_UART_RX2 16
#define PIN_UART_TX2 17

// GPIO 12 (strapping) y GPIO 15 / SD0-SD3: no se usan.
