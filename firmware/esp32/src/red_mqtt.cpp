#include "red_mqtt.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// ---------- Analisis del comando (portable, sin Arduino) ----------

static const char* saltarEsp(const char* p) {
  while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') p++;
  return p;
}

// Lee una cadena JSON desde la comilla de apertura. Devuelve puntero tras la comilla de cierre o NULL.
// Si no cabe en dst, marca *trunca (el campo se considera invalido) pero sigue avanzando.
static const char* leerCadena(const char* p, char* dst, size_t max, bool* trunca) {
  size_t n = 0;
  *trunca = false;
  p++;  // comilla de apertura
  while (*p && *p != '"') {
    char c = *p++;
    if (c == '\\') {
      if (!*p) return NULL;
      c = *p++;
    }
    if (n + 1 < max) dst[n++] = c; else *trunca = true;
  }
  if (*p != '"') return NULL;
  if (max) dst[n] = '\0';
  return p + 1;
}

static bool soloCaracteresNumericos(const char* t) {
  if (!*t) return false;
  for (; *t; t++) {
    if (!((*t >= '0' && *t <= '9') || *t == '+' || *t == '-' || *t == '.' || *t == 'e' || *t == 'E')) return false;
  }
  return true;
}

bool redParsearComando(const char* payload, ComandoMqtt& out) {
  memset(&out, 0, sizeof(out));
  bool idTrunco = false, cmdTrunco = false, tarimaTrunca = false;
  const char* p = saltarEsp(payload);
  if (*p != '{') return false;
  p = saltarEsp(p + 1);
  if (*p == '}') return false;
  for (;;) {
    char clave[24];
    bool kt;
    if (*p != '"') return false;
    p = leerCadena(p, clave, sizeof(clave), &kt);
    if (!p) return false;
    p = saltarEsp(p);
    if (*p != ':') return false;
    p = saltarEsp(p + 1);

    if (*p == '"') {
      char* dst = NULL; size_t max = 0; bool* trunca = NULL;
      char basura[2];
      if (!strcmp(clave, "id_cmd")) { dst = out.idCmd; max = sizeof(out.idCmd); trunca = &idTrunco; }
      else if (!strcmp(clave, "cmd")) { dst = out.cmd; max = sizeof(out.cmd); trunca = &cmdTrunco; }
      else if (!strcmp(clave, "id_tarima")) { dst = out.idTarima; max = sizeof(out.idTarima); trunca = &tarimaTrunca; }
      else { dst = basura; max = 1; trunca = &kt; }
      p = leerCadena(p, dst, max, trunca);
      if (!p) return false;
      // peso_kg como string JSON: invalido (se deja peso vacio)
      if (!strcmp(clave, "peso_kg")) out.peso[0] = '\0';
    } else if (*p == '{' || *p == '[') {
      return false;
    } else {
      char tok[32];
      size_t n = 0;
      bool largo = false;
      while (*p && *p != ',' && *p != '}' && *p != ' ' && *p != '\t' && *p != '\r' && *p != '\n') {
        if (n + 1 < sizeof(tok)) tok[n++] = *p; else largo = true;
        p++;
      }
      tok[n] = '\0';
      if (n == 0) return false;
      bool num = !largo && soloCaracteresNumericos(tok);
      if (!strcmp(clave, "peso_kg")) {
        if (num) strcpy(out.peso, tok); else out.peso[0] = '\0';
      } else if (!strcmp(clave, "pwm_izq")) {
        out.pwmIzq = num ? strtod(tok, NULL) : 0.0;
      } else if (!strcmp(clave, "pwm_der")) {
        out.pwmDer = num ? strtod(tok, NULL) : 0.0;
      }
    }
    p = saltarEsp(p);
    if (*p == ',') { p = saltarEsp(p + 1); continue; }
    if (*p == '}') { p = saltarEsp(p + 1); break; }
    return false;
  }
  if (*p != '\0') return false;
  if (idTrunco || cmdTrunco || tarimaTrunca) return false;
  if (!out.idCmd[0] || !out.cmd[0]) return false;
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

// ---------- Wi-Fi y MQTT 3.1.1 (solo en el ESP32) ----------
#ifdef ARDUINO
#include <Arduino.h>
#include <WiFi.h>
#include <time.h>
#include <sys/time.h>
#include "secrets.h"  // copiar de secrets.example.h; ignorado por git

#define KEEPALIVE_S 6
#define PING_CADA_MS 2000UL
#define SIN_RX_MAX_MS 5000UL
#define REINTENTO_MS 2000UL

static WiFiClient g_cli;
static RedAlComando g_alComando = NULL;
static bool g_mqtt = false;
static uint32_t g_ultimoRx = 0, g_ultimoPing = 0, g_ultimoIntento = 0;
static uint16_t g_pid = 0;
static uint8_t g_rx[RED_RX_MAX + 1];
static uint8_t g_tx[RED_RX_MAX + 128];

uint64_t redTsMs() {
  time_t s = time(NULL);
  if (s > 1700000000) {  // hora sincronizada por NTP
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (uint64_t)tv.tv_sec * 1000ULL + (uint64_t)(tv.tv_usec / 1000);
  }
  return (uint64_t)millis();
}

static bool leerBytes(uint8_t* b, size_t n, uint32_t plazoMs) {
  size_t got = 0;
  uint32_t t0 = millis();
  while (got < n) {
    int d = g_cli.read(b + got, n - got);
    if (d > 0) { got += d; continue; }
    if (!g_cli.connected() && !g_cli.available()) return false;
    if (millis() - t0 > plazoMs) return false;
    delay(1);
  }
  return true;
}

static bool descartar(size_t n, uint32_t plazoMs) {
  uint8_t tmp[64];
  while (n) {
    size_t k = n < sizeof(tmp) ? n : sizeof(tmp);
    if (!leerBytes(tmp, k, plazoMs)) return false;
    n -= k;
  }
  return true;
}

static size_t varint(uint8_t* dst, size_t v) {
  size_t i = 0;
  do {
    uint8_t b = v % 128;
    v /= 128;
    if (v) b |= 0x80;
    dst[i++] = b;
  } while (v);
  return i;
}

static void escribirU16(uint8_t* d, uint16_t v) { d[0] = v >> 8; d[1] = v & 0xFF; }

static size_t ponerCadena(uint8_t* d, const char* s) {
  size_t l = strlen(s);
  escribirU16(d, (uint16_t)l);
  memcpy(d + 2, s, l);
  return l + 2;
}

static void caer() {
  g_mqtt = false;
  g_cli.stop();
  g_ultimoIntento = millis();
}

bool redPublicar(const char* topic, const char* payload, bool retenido, uint8_t qos) {
  if (!g_mqtt) return false;
  size_t tl = strlen(topic), pl = strlen(payload);
  size_t resto = 2 + tl + (qos ? 2 : 0) + pl;
  if (resto + 5 > sizeof(g_tx)) return false;
  size_t i = 0;
  g_tx[i++] = 0x30 | (retenido ? 1 : 0) | ((qos & 1) << 1);
  i += varint(g_tx + i, resto);
  i += ponerCadena(g_tx + i, topic);
  if (qos) { if (++g_pid == 0) g_pid = 1; escribirU16(g_tx + i, g_pid); i += 2; }
  memcpy(g_tx + i, payload, pl);
  i += pl;
  if (g_cli.write(g_tx, i) != i) { caer(); return false; }
  return true;
}

static bool conectarMqtt() {
  if (!g_cli.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 1000)) return false;
  g_cli.setNoDelay(true);
  char will[128];
  snprintf(will, sizeof(will), "{\"ts\":%llu,\"robot_id\":\"" ROBOT_ID "\",\"estado\":\"FUERA_DE_LINEA\"}",
           (unsigned long long)redTsMs());
  uint8_t cuerpo[300];
  size_t i = 0;
  i += ponerCadena(cuerpo + i, "MQTT");
  cuerpo[i++] = 4;                       // nivel 3.1.1
  cuerpo[i++] = 0x02 | 0x04 | 0x08 | 0x20;  // clean + will + will QoS1 + will retain
  escribirU16(cuerpo + i, KEEPALIVE_S); i += 2;
  i += ponerCadena(cuerpo + i, "koleo-esp32");
  i += ponerCadena(cuerpo + i, TEMA_CONEXION);
  size_t wl = strlen(will);
  escribirU16(cuerpo + i, (uint16_t)wl); i += 2;
  memcpy(cuerpo + i, will, wl); i += wl;
  uint8_t cab[5];
  cab[0] = 0x10;
  size_t h = 1 + varint(cab + 1, i);
  g_cli.write(cab, h);
  g_cli.write(cuerpo, i);
  uint8_t ack[4];
  if (!leerBytes(ack, 4, 1000) || ack[0] != 0x20 || ack[3] != 0) { g_cli.stop(); return false; }
  g_mqtt = true;
  g_ultimoRx = g_ultimoPing = millis();
  // SUBSCRIBE a esp32/cmd con QoS 1
  uint8_t sub[64];
  size_t j = 0;
  sub[j++] = 0x82;
  size_t tl = strlen(TEMA_CMD);
  sub[j++] = (uint8_t)(2 + 2 + tl + 1);
  if (++g_pid == 0) g_pid = 1;
  escribirU16(sub + j, g_pid); j += 2;
  j += ponerCadena(sub + j, TEMA_CMD);
  sub[j++] = 1;
  g_cli.write(sub, j);
  char en[128];
  snprintf(en, sizeof(en), "{\"ts\":%llu,\"robot_id\":\"" ROBOT_ID "\",\"estado\":\"EN_LINEA\"}",
           (unsigned long long)redTsMs());
  return redPublicar(TEMA_CONEXION, en, true, 1);
}

static void atenderPaquete() {
  uint8_t cab;
  if (!leerBytes(&cab, 1, 200)) { caer(); return; }
  size_t len = 0, mult = 1;
  for (int k = 0; k < 4; k++) {
    uint8_t b;
    if (!leerBytes(&b, 1, 200)) { caer(); return; }
    len += (b & 0x7F) * mult;
    mult *= 128;
    if (!(b & 0x80)) break;
    if (k == 3) { caer(); return; }
  }
  g_ultimoRx = millis();
  bool esPublish = (cab >> 4) == 3;
  if (len > RED_RX_MAX) {
    // Mensaje demasiado grande: se descarta COMPLETO (se acusa recibo si es QoS1 para no atascar al broker).
    if (esPublish && ((cab >> 1) & 3) == 1) {
      uint8_t ini[96];
      size_t k = len < sizeof(ini) ? len : sizeof(ini);
      if (!leerBytes(ini, k, 200)) { caer(); return; }
      size_t tl = (ini[0] << 8) | ini[1];
      if (2 + tl + 2 <= k) {
        uint8_t pa[4] = {0x40, 0x02, ini[2 + tl], ini[3 + tl]};
        g_cli.write(pa, 4);
      }
      if (!descartar(len - k, 200)) { caer(); return; }
    } else if (!descartar(len, 200)) { caer(); return; }
    return;
  }
  if (len && !leerBytes(g_rx, len, 300)) { caer(); return; }
  g_rx[len] = 0;
  if (!esPublish || len < 2) return;  // CONNACK/SUBACK/PINGRESP/PUBACK: solo cuentan como actividad
  uint8_t qos = (cab >> 1) & 3;
  size_t tl = (g_rx[0] << 8) | g_rx[1];
  size_t pos = 2 + tl;
  if (pos > len) return;
  uint16_t pid = 0;
  if (qos) {
    if (pos + 2 > len) return;
    pid = (g_rx[pos] << 8) | g_rx[pos + 1];
    pos += 2;
  }
  bool esCmd = tl == strlen(TEMA_CMD) && !memcmp(g_rx + 2, TEMA_CMD, tl);
  if (qos == 1) {
    uint8_t pa[4] = {0x40, 0x02, (uint8_t)(pid >> 8), (uint8_t)(pid & 0xFF)};
    g_cli.write(pa, 4);
  }
  if (esCmd && g_alComando) g_alComando((const char*)g_rx + pos, len - pos);
}

void redIniciar(RedAlComando alComando) {
  g_alComando = alComando;
  WiFi.mode(WIFI_STA);
  WiFi.setAutoReconnect(true);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  configTime(0, 0, "pool.ntp.org");  // si no hay Internet, redTsMs() usa ms desde el arranque
  g_ultimoIntento = millis();
}

bool redConectado() { return g_mqtt && WiFi.status() == WL_CONNECTED; }

void redActualizar() {
  if (WiFi.status() != WL_CONNECTED) {
    if (g_mqtt || g_cli.connected()) caer();
    return;
  }
  if (!g_mqtt) {
    if (millis() - g_ultimoIntento >= REINTENTO_MS) {
      g_ultimoIntento = millis();
      if (!conectarMqtt()) { g_mqtt = false; g_cli.stop(); }
    }
    return;
  }
  uint8_t guardia = 8;  // paquetes por vuelta, para no acaparar el loop
  while (g_mqtt && g_cli.available() && guardia--) atenderPaquete();
  if (!g_mqtt) return;
  if (!g_cli.connected() && !g_cli.available()) { caer(); return; }
  uint32_t ahora = millis();
  if (ahora - g_ultimoRx > SIN_RX_MAX_MS) { caer(); return; }
  if (ahora - g_ultimoPing >= PING_CADA_MS) {
    uint8_t ping[2] = {0xC0, 0x00};
    g_cli.write(ping, 2);
    g_ultimoPing = ahora;
  }
}
#endif  // ARDUINO
