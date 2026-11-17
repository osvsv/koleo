#include "red_mqtt.h"
#include <ArduinoJson.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// ---------- Analisis del comando (ArduinoJson) ----------

// Copia un campo de texto. Falso si no es texto o no cabe (nunca se trunca).
static bool copiarTexto(JsonVariantConst v, char* dst, size_t max) {
  if (!v.is<const char*>()) return false;
  const char* s = v.as<const char*>();
  if (!s || strlen(s) >= max) return false;
  strcpy(dst, s);
  return true;
}

bool redParsearComando(const char* payload, ComandoMqtt& out) {
  memset(&out, 0, sizeof(out));
  if (!payload) return false;
  JsonDocument doc;
  if (deserializeJson(doc, payload)) return false;
  if (!doc.is<JsonObject>()) return false;
  JsonObjectConst o = doc.as<JsonObjectConst>();

  if (!copiarTexto(o["id_cmd"], out.idCmd, sizeof(out.idCmd)) || !out.idCmd[0]) return false;
  if (!copiarTexto(o["cmd"], out.cmd, sizeof(out.cmd)) || !out.cmd[0]) return false;
  if (!o["id_tarima"].isNull() && !copiarTexto(o["id_tarima"], out.idTarima, sizeof(out.idTarima))) return false;

  // peso_kg: solo un numero JSON finito cuenta; string, objeto, NaN, inf -> peso vacio (PESO_INVALIDO)
  JsonVariantConst p = o["peso_kg"];
  if (p.is<double>()) {
    double d = p.as<double>();
    if (isfinite(d)) snprintf(out.peso, sizeof(out.peso), "%.9g", d);
  }
  JsonVariantConst i = o["pwm_izq"], r = o["pwm_der"];
  out.pwmIzq = i.is<double>() ? i.as<double>() : 0.0;
  out.pwmDer = r.is<double>() ? r.as<double>() : 0.0;
  if (!isfinite(out.pwmIzq)) out.pwmIzq = 0.0;
  if (!isfinite(out.pwmDer)) out.pwmDer = 0.0;
  return true;
}

size_t redEscapar(const char* src, char* dst, size_t max) {
  size_t n = 0;
  for (; *src && n + 2 < max; src++) {
    unsigned char c = (unsigned char)*src;
    if (c == '"' || c == '\\') { dst[n++] = '\\'; dst[n++] = (char)c; }
    else if (c >= 0x20) dst[n++] = (char)c;
  }
  if (max) dst[n] = '\0';
  return n;
}

// ---------- Wi-Fi y MQTT (solo en el ESP32) ----------
#ifdef ARDUINO
#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <time.h>
#include <sys/time.h>
#include "secrets.h"  // copiar de secrets.example.h; ignorado por git

#define KEEPALIVE_S 6
#define REINTENTO_MS 2000UL

static WiFiClient g_cli;
static PubSubClient g_mqtt(g_cli);
static RedAlComando g_alComando = NULL;
static uint32_t g_ultimoIntento = 0;

uint64_t redTsMs() {
  time_t s = time(NULL);
  if (s > 1700000000) {  // hora sincronizada por NTP
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (uint64_t)tv.tv_sec * 1000ULL + (uint64_t)(tv.tv_usec / 1000);
  }
  return (uint64_t)millis();  // sin Internet: ms desde el arranque
}

static void alMensaje(char* topic, uint8_t* payload, unsigned int len) {
  if (strcmp(topic, TEMA_CMD) != 0 || !g_alComando) return;
  // PubSubClient ya ignora mensajes mayores que su buffer; defensa extra: nunca procesar un prefijo.
  if (len >= RED_RX_MAX) return;
  static char buf[RED_RX_MAX + 1];
  memcpy(buf, payload, len);
  buf[len] = '\0';
  g_alComando(buf, len);
}

bool redPublicar(const char* topic, const char* payload, bool retenido, uint8_t qos) {
  (void)qos;
  if (!g_mqtt.connected()) return false;
  return g_mqtt.publish(topic, payload, retenido);
}

static bool conectarMqtt() {
  char will[128];
  snprintf(will, sizeof(will), "{\"ts\":%llu,\"robot_id\":\"" ROBOT_ID "\",\"estado\":\"FUERA_DE_LINEA\"}",
           (unsigned long long)redTsMs());
  if (!g_mqtt.connect("koleo-esp32", NULL, NULL, TEMA_CONEXION, 1, true, will, true)) return false;
  g_mqtt.subscribe(TEMA_CMD, 1);
  char en[128];
  snprintf(en, sizeof(en), "{\"ts\":%llu,\"robot_id\":\"" ROBOT_ID "\",\"estado\":\"EN_LINEA\"}",
           (unsigned long long)redTsMs());
  return g_mqtt.publish(TEMA_CONEXION, en, true);
}

void redIniciar(RedAlComando alComando) {
  g_alComando = alComando;
  g_cli.setTimeout(1000);
  g_mqtt.setServer(MQTT_BROKER_HOST, MQTT_BROKER_PORT);
  g_mqtt.setBufferSize(RED_BUFFER_MQTT);
  g_mqtt.setKeepAlive(KEEPALIVE_S);
  g_mqtt.setSocketTimeout(1);
  g_mqtt.setCallback(alMensaje);
  WiFi.mode(WIFI_STA);
  WiFi.setAutoReconnect(true);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  configTime(0, 0, "pool.ntp.org");  // si no hay Internet, redTsMs() usa ms desde el arranque
  g_ultimoIntento = millis();
}

bool redConectado() { return g_mqtt.connected() && WiFi.status() == WL_CONNECTED; }

void redActualizar() {
  if (WiFi.status() != WL_CONNECTED) {
    if (g_cli.connected()) g_cli.stop();
    return;
  }
  if (!g_mqtt.connected()) {
    if (millis() - g_ultimoIntento >= REINTENTO_MS) {
      g_ultimoIntento = millis();
      if (!conectarMqtt()) g_cli.stop();
    }
    return;
  }
  g_mqtt.loop();
}
#endif  // ARDUINO
