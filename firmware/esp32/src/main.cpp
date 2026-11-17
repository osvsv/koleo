// Esqueleto WP-3.1. Depuracion por monitor serie USB: "LIFT <peso_kg>" (WP-3.2 agrega MQTT).
#include <Arduino.h>
#include "elevacion.h"

static String linea;

void setup() {
  Serial.begin(115200);
  elevacionIniciarPines();
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c != '\n') { if (linea.length() < 64) linea += c; continue; }  // buffer acotado
    linea.trim();
    if (linea.startsWith("LIFT")) {
      String arg = linea.substring(4);
      arg.trim();
      CodigoLift r = elevacionSolicitar(arg.length() ? arg.c_str() : NULL);
      Serial.println(codigoLiftTexto(r));
    }
    linea = "";
  }
  elevacionActualizar();
}
