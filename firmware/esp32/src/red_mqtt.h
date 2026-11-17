// WP-3.2: Wi-Fi y cliente MQTT 3.1.1 minimo (sin librerias externas) para el broker de la Pi.
#pragma once
#include <stddef.h>
#include <stdint.h>

#define TEMA_CMD "koleo/robot1/esp32/cmd"
#define TEMA_RESP "koleo/robot1/esp32/resp"
#define TEMA_CONEXION "koleo/robot1/esp32/conexion"
#define ROBOT_ID "robot1"
#define RED_RX_MAX 512  // un mensaje mas grande se DESCARTA completo (nunca se procesa un prefijo)

// Comando ya interpretado. peso[0]==0 significa "ausente o no numerico" -> PESO_INVALIDO.
struct ComandoMqtt {
  char idCmd[48];
  char cmd[8];
  char idTarima[48];
  char peso[32];  // solo se llena si peso_kg es un numero JSON (nunca si es string)
  double pwmIzq;
  double pwmDer;
};

// Funcion pura (se prueba en el host). payload debe terminar en '\0'.
// Falso si el JSON es invalido, anidado, o falta id_cmd o cmd.
bool redParsearComando(const char* payload, ComandoMqtt& out);
// Copia src escapando comillas, barras y caracteres de control. Devuelve la longitud.
size_t redEscapar(const char* src, char* dst, size_t max);

typedef void (*RedAlComando)(const char* payload, size_t len);

void redIniciar(RedAlComando alComando);  // arranca Wi-Fi; MQTT conecta desde redActualizar()
void redActualizar();                     // no bloquea mas de ~1 s; llamar en cada loop()
bool redConectado();                      // Wi-Fi Y MQTT arriba
bool redPublicar(const char* topic, const char* payload, bool retenido, uint8_t qos);
uint64_t redTsMs();                       // epoch ms (NTP) o, sin hora, ms desde el arranque
