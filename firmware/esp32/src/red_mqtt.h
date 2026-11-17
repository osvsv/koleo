// WP-3.2: Wi-Fi y MQTT con PubSubClient + ArduinoJson (CC-011) para el broker de la Pi.
#pragma once
#include <stddef.h>
#include <stdint.h>

#define TEMA_CMD "koleo/robot1/esp32/cmd"
#define TEMA_RESP "koleo/robot1/esp32/resp"
#define TEMA_CONEXION "koleo/robot1/esp32/conexion"
#define ROBOT_ID "robot1"
#define RED_RX_MAX 512  // un mensaje de 512 bytes o mas se DESCARTA completo (nunca se procesa un prefijo)
#define RED_BUFFER_MQTT 768  // setBufferSize de PubSubClient: cabecera + tema (22 B) + RED_RX_MAX caben enteros

// Comando ya interpretado. peso[0]==0 significa "ausente o no numerico/no finito" -> PESO_INVALIDO.
struct ComandoMqtt {
  char idCmd[48];
  char cmd[8];
  char idTarima[48];
  char peso[32];  // solo se llena si peso_kg es un numero JSON finito (nunca si es string)
  double pwmIzq;
  double pwmDer;
};

// Analiza el JSON con ArduinoJson. payload debe terminar en '\0'.
// Falso si el JSON es invalido, no es objeto, o falta id_cmd o cmd (texto no vacio y que quepa).
bool redParsearComando(const char* payload, ComandoMqtt& out);
// Copia src escapando comillas, barras y caracteres de control. Devuelve la longitud.
size_t redEscapar(const char* src, char* dst, size_t max);

typedef void (*RedAlComando)(const char* payload, size_t len);

void redIniciar(RedAlComando alComando);  // arranca Wi-Fi; MQTT conecta desde redActualizar()
void redActualizar();                     // llamar en cada loop(); un reintento bloquea ~1 s como maximo
bool redConectado();                      // Wi-Fi Y MQTT arriba
// PubSubClient solo publica con QoS 0 (el parametro qos se conserva por compatibilidad y se ignora).
bool redPublicar(const char* topic, const char* payload, bool retenido, uint8_t qos);
uint64_t redTsMs();                       // epoch ms (NTP) o, sin hora, ms desde el arranque
