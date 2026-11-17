#include "elevacion.h"
#include <math.h>
#include <stdlib.h>
#include <string.h>

#ifdef ARDUINO
#include <Arduino.h>
#include "esp_timer.h"
#include "pines.h"
static portMUX_TYPE g_mux = portMUX_INITIALIZER_UNLOCKED;
static esp_timer_handle_t g_timerCorte = NULL;
#define SC_ENTRAR() portENTER_CRITICAL(&g_mux)
#define SC_SALIR() portEXIT_CRITICAL(&g_mux)
#else
#define SC_ENTRAR()
#define SC_SALIR()
#endif

// g_activa se comparte entre loop() y el callback del temporizador de corte.
static volatile bool g_activa = false;
static volatile uint32_t g_inicioMs = 0;

bool pesoValido(float kg) { return isfinite(kg) && kg > 0.0f; }
bool excedeLimite(float kg) { return kg > PESO_LIMITE_KG; }

CodigoLift evaluarLift(const char* pesoTexto) {
  if (pesoTexto == NULL || *pesoTexto == '\0') return PESO_INVALIDO;  // ausente: nunca 0 kg
  char* fin = NULL;
  double v = strtod(pesoTexto, &fin);
  while (fin && (*fin == ' ' || *fin == '\t' || *fin == '\r' || *fin == '\n')) fin++;
  if (fin == pesoTexto || (fin && *fin != '\0')) return PESO_INVALIDO;  // no numerico
  if (!isfinite(v) || v <= 0.0) return PESO_INVALIDO;
  if (v > (double)PESO_LIMITE_KG) return OVERWEIGHT;  // comparar en double antes de convertir a float
  float kg = (float)v;
  if (!pesoValido(kg)) return PESO_INVALIDO;  // p. ej. subdesbordamiento a 0
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

// Corte independiente de loop() y de la red. Se llama desde el callback de esp_timer
// (o desde pruebas de host). Idempotente y sin bloqueos: solo apaga el pin y marca estado.
// Solo corta si ya transcurrio el limite, asi un callback tardio de una elevacion anterior
// no corta una elevacion nueva.
void elevacionCorteTimerEn(uint32_t ahora) {
  SC_ENTRAR();
  if (g_activa && (uint32_t)(ahora - g_inicioMs) >= ELEVACION_MAX_MS) {
    actuadorSube(false);
    g_activa = false;
  }
  SC_SALIR();
}

#ifdef ARDUINO
static void cbCorte(void*) { elevacionCorteTimerEn((uint32_t)(esp_timer_get_time() / 1000ULL)); }
#endif

void elevacionIniciarPines() {
#ifdef ARDUINO
  if (g_timerCorte == NULL) {
    esp_timer_create_args_t a = {};
    a.callback = &cbCorte;
    a.name = "elev_corte";
    esp_timer_create(&a, &g_timerCorte);
  }
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

CodigoLift elevacionSolicitarEn(const char* pesoTexto, uint32_t ahora) {
  CodigoLift c = evaluarLift(pesoTexto);
  bool inicio = false;
  if (c == LIFT_OK) {  // solo se energiza con LIFT_OK; si ya esta activa no reinicia el limite
    SC_ENTRAR();
    if (!g_activa) {
      g_activa = true;
      g_inicioMs = ahora;
      actuadorSube(true);
      inicio = true;
    }
    SC_SALIR();
  }
#ifdef ARDUINO
  if (inicio && g_timerCorte != NULL) {
    esp_timer_stop(g_timerCorte);  // por si quedo armado; error ignorable si no lo estaba
    esp_timer_start_once(g_timerCorte, (uint64_t)ELEVACION_MAX_MS * 1000ULL);
  }
#else
  (void)inicio;
#endif
  return c;
}

CodigoLift elevacionSolicitar(const char* pesoTexto) { return elevacionSolicitarEn(pesoTexto, ahoraMs()); }

void elevacionActualizarEn(uint32_t ahora) {
  elevacionCorteTimerEn(ahora);  // mismo corte, mismo candado: sin carrera con el temporizador
#ifdef ARDUINO
  if (!g_activa && g_timerCorte != NULL) esp_timer_stop(g_timerCorte);  // ya termino: cancelar
#endif
}

void elevacionActualizar() { elevacionActualizarEn(ahoraMs()); }
bool elevacionActiva() { return g_activa; }
