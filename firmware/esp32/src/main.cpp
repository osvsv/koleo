// WP-3.2: el ESP32 atiende LIFT, MOVE, STOP y DROP por MQTT (contratos/esp32.md).
// Se flashea por USB una sola vez; en operacion no hay USB (CC-010).
#include <Arduino.h>
#include <stdio.h>
#include <string.h>
#include "elevacion.h"
#include "pines.h"
#include "red_mqtt.h"

#define WATCHDOG_MOVE_MS 1000UL  // sin comandos mas de 1 s con MOVE activo -> paro
#define PWM_HZ 1000
#define PWM_BITS 8
#define CACHE_CMD 8

static bool moveActivo = false;
static bool pwmListo = false;
static uint32_t ultimoCmdMs = 0;

struct Atendido { char id[48]; bool ok; const char* codigo; bool usado; };
static Atendido cache[CACHE_CMD];
static uint8_t cacheSig = 0;

// ---------- Traccion ----------
static void pwmEscribir(int pin, int canal, int duty) {
#if defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR >= 3
  (void)canal;
  ledcWrite(pin, duty);
#else
  ledcWrite(canal, duty);
#endif
}

static void pwmPrepara() {
  if (pwmListo) return;
#if defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR >= 3
  ledcAttach(PIN_MI_ENA, PWM_HZ, PWM_BITS);
  ledcAttach(PIN_MD_ENB, PWM_HZ, PWM_BITS);
#else
  ledcSetup(0, PWM_HZ, PWM_BITS); ledcAttachPin(PIN_MI_ENA, 0);
  ledcSetup(1, PWM_HZ, PWM_BITS); ledcAttachPin(PIN_MD_ENB, 1);
#endif
  pwmListo = true;
}

static void detenerTraccion() {
  if (pwmListo) {
    pwmEscribir(PIN_MI_ENA, 0, 0);
    pwmEscribir(PIN_MD_ENB, 1, 0);
  } else {
    digitalWrite(PIN_MD_ENB, LOW);
    digitalWrite(PIN_MI_ENA, LOW);
  }
  digitalWrite(PIN_MI_IN1, LOW); digitalWrite(PIN_MI_IN2, LOW);
  digitalWrite(PIN_MD_IN3, LOW); digitalWrite(PIN_MD_IN4, LOW);
  moveActivo = false;
}

static void ruedas(double izq, double der) {
  auto lado = [](double v, int in1, int in2, int pin, int canal) {
    if (v > 255) v = 255;
    if (v < -255) v = -255;
    digitalWrite(in1, v > 0 ? HIGH : LOW);
    digitalWrite(in2, v < 0 ? HIGH : LOW);
    pwmEscribir(pin, canal, (int)(v < 0 ? -v : v));
  };
  pwmPrepara();
  lado(izq, PIN_MI_IN1, PIN_MI_IN2, PIN_MI_ENA, 0);
  lado(der, PIN_MD_IN3, PIN_MD_IN4, PIN_MD_ENB, 1);
  moveActivo = (izq != 0 || der != 0);
}

// ---------- Respuestas ----------
static void responder(const char* idCmd, bool ok, const char* codigo) {
  char id[100], buf[240];
  redEscapar(idCmd, id, sizeof(id));
  snprintf(buf, sizeof(buf), "{\"ts\":%llu,\"id_cmd\":\"%s\",\"resultado\":\"%s\",\"codigo\":\"%s\"}",
           (unsigned long long)redTsMs(), id, ok ? "ACK" : "ERR", codigo);
  redPublicar(TEMA_RESP, buf, false, 1);
}

static void alComando(const char* payload, size_t len) {
  if (len >= RED_RX_MAX) return;  // defensa: nunca procesar un mensaje truncado
  ComandoMqtt c;
  if (!redParsearComando(payload, c)) return;  // invalido: descartado (sin id_cmd no hay a quien responder)
  bool conocido = !strcmp(c.cmd, "LIFT") || !strcmp(c.cmd, "MOVE") || !strcmp(c.cmd, "STOP") || !strcmp(c.cmd, "DROP");
  if (!conocido) return;
  ultimoCmdMs = millis();

  // id_cmd ya atendido: no repite la accion, solo reenvia la respuesta
  for (uint8_t i = 0; i < CACHE_CMD; i++) {
    if (cache[i].usado && !strcmp(cache[i].id, c.idCmd)) {
      responder(c.idCmd, cache[i].ok, cache[i].codigo);
      return;
    }
  }

  bool ok = true;
  const char* codigo = "STOP_OK";
  if (!strcmp(c.cmd, "LIFT")) {
    CodigoLift r = elevacionSolicitar(c.peso[0] ? c.peso : NULL);
    ok = (r == LIFT_OK);
    codigo = codigoLiftTexto(r);
  } else if (!strcmp(c.cmd, "MOVE")) {
    ruedas(c.pwmIzq, c.pwmDer);
    codigo = "MOVE_OK";
  } else if (!strcmp(c.cmd, "STOP")) {
    detenerTraccion();
    codigo = "STOP_OK";
  } else {  // DROP: el contrato solo exige el acuse
    codigo = "DROP_OK";
  }

  Atendido& a = cache[cacheSig];
  cacheSig = (cacheSig + 1) % CACHE_CMD;
  strncpy(a.id, c.idCmd, sizeof(a.id) - 1);
  a.id[sizeof(a.id) - 1] = '\0';
  a.ok = ok;
  a.codigo = codigo;
  a.usado = true;
  responder(c.idCmd, ok, codigo);
}

static void vigilante() {
  if (!moveActivo) return;
  if (!redConectado() || (uint32_t)(millis() - ultimoCmdMs) > WATCHDOG_MOVE_MS) detenerTraccion();
}

void setup() {
  Serial.begin(115200);
  elevacionIniciarPines();  // deja GPIO 14 (ENB) en LOW
  pinMode(PIN_MI_ENA, OUTPUT); digitalWrite(PIN_MI_ENA, LOW);
  pinMode(PIN_MI_IN1, OUTPUT); pinMode(PIN_MI_IN2, OUTPUT);
  pinMode(PIN_MD_IN3, OUTPUT); pinMode(PIN_MD_IN4, OUTPUT);
  digitalWrite(PIN_MI_IN1, LOW); digitalWrite(PIN_MI_IN2, LOW);
  digitalWrite(PIN_MD_IN3, LOW); digitalWrite(PIN_MD_IN4, LOW);
  redIniciar(alComando);
}

void loop() {
  vigilante();       // antes: un reintento de conexion no retrasa el paro
  redActualizar();
  vigilante();
  elevacionActualizar();
}
