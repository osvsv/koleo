#pragma once
#include <stdint.h>

#define PESO_LIMITE_KG 10.0f
#define ELEVACION_MAX_MS 8000UL  // tiempo maximo de energizado del actuador

enum CodigoLift { LIFT_OK, OVERWEIGHT, PESO_INVALIDO };

// Falso si no es finito o es <= 0.
bool pesoValido(float kg);
// Verdadero si kg > 10.0 (el limite es inclusivo: 10.0 se acepta).
bool excedeLimite(float kg);

// Valida el peso declarado. NULL (ausente) o texto no numerico -> PESO_INVALIDO.
CodigoLift evaluarLift(const char* pesoTexto);

// Evalua y, solo si LIFT_OK, inicia la elevacion. Devuelve el codigo de respuesta.
// Un LIFT valido con la elevacion ya activa devuelve LIFT_OK pero NO reinicia el limite de 8 s.
CodigoLift elevacionSolicitar(const char* pesoTexto);
CodigoLift elevacionSolicitarEn(const char* pesoTexto, uint32_t ahoraMs);  // reloj inyectado
// Version con reloj inyectado (sin delay): llamar desde loop().
void elevacionActualizarEn(uint32_t ahoraMs);
// Corte de respaldo independiente de loop() y de la red: lo invoca un temporizador one-shot
// de esp_timer armado a ELEVACION_MAX_MS al iniciar la elevacion (en host, se simula).
void elevacionCorteTimerEn(uint32_t ahoraMs);
void elevacionActualizar();  // usa millis()
bool elevacionActiva();
void elevacionIniciarPines();
const char* codigoLiftTexto(CodigoLift c);
