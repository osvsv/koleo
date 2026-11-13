#include "elevacion.h"
#include <math.h>
#include <stdlib.h>
#include <string.h>

#ifdef ARDUINO
#include <Arduino.h>
#include "pines.h"
#endif

static bool g_activa = false;
static uint32_t g_inicioMs = 0;

bool pesoValido(float kg) { return isfinite(kg) && kg > 0.0f; }
bool excedeLimite(float kg) { return kg > PESO_LIMITE_KG; }

CodigoLift evaluarLift(const char* pesoTexto) {
  if (pesoTexto == NULL || *pesoTexto == '\0') return PESO_INVALIDO;  // ausente: nunca 0 kg
  char* fin = NULL;
  double v = strtod(pesoTexto, &fin);
  while (fin && (*fin == ' ' || *fin == '\t' || *fin == '\r' || *fin == '\n')) fin++;
  if (fin == pesoTexto || (fin && *fin != '\0')) return PESO_INVALIDO;  // no numerico
  float kg = (float)v;
  if (!pesoValido(kg)) return PESO_INVALIDO;
  if (excedeLimite(kg)) return OVERWEIGHT;
  return LIFT_OK;
}

const char* codigoLiftTexto(CodigoLift c) {
  switch (c) {
    case LIFT_OK: return "LIFT_OK";
    case OVERWEIGHT: return "OVERWEIGHT";
    default: return "PESO_INVALIDO";
  }
}

static void actuadorSube(bool on) {
#ifdef ARDUINO
  digitalWrite(PIN_ACT_LPWM, LOW);
  digitalWrite(PIN_ACT_RPWM, on ? HIGH : LOW);
#else
  (void)on;
#endif
}

void elevacionIniciarPines() {
#ifdef ARDUINO
  pinMode(PIN_ACT_RPWM, OUTPUT);
  pinMode(PIN_ACT_LPWM, OUTPUT);
  pinMode(PIN_MD_ENB, OUTPUT);
  digitalWrite(PIN_MD_ENB, LOW);  // GPIO 14 en bajo al inicio
  actuadorSube(false);
#endif
}

static uint32_t ahoraMs() {
#ifdef ARDUINO
  return millis();
#else
  return 0;
#endif
}

CodigoLift elevacionSolicitar(const char* pesoTexto) {
  CodigoLift c = evaluarLift(pesoTexto);
  if (c == LIFT_OK) {  // el actuador solo se energiza con LIFT_OK
    g_activa = true;
    g_inicioMs = ahoraMs();
    actuadorSube(true);
  }
  return c;
}

void elevacionActualizarEn(uint32_t ahora) {
  if (g_activa && (uint32_t)(ahora - g_inicioMs) >= ELEVACION_MAX_MS) {
    actuadorSube(false);
    g_activa = false;
  }
}

void elevacionActualizar() { elevacionActualizarEn(ahoraMs()); }
bool elevacionActiva() { return g_activa; }
