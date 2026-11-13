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
CodigoLift elevacionSolicitar(const char* pesoTexto);
// Version con reloj inyectado (sin delay): llamar desde loop().
void elevacionActualizarEn(uint32_t ahoraMs);
void elevacionActualizar();  // usa millis()
bool elevacionActiva();
void elevacionIniciarPines();
const char* codigoLiftTexto(CodigoLift c);
