// Prueba interna en PC: g++ -I src test/test_elevacion.cpp src/elevacion.cpp
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include "elevacion.h"
int main() {
  assert(!pesoValido(0) && !pesoValido(-1) && !pesoValido(NAN) && !pesoValido(INFINITY) && pesoValido(0.1f));
  assert(!excedeLimite(10.0f) && excedeLimite(10.1f) && excedeLimite(11.8f));
  assert(evaluarLift(NULL) == PESO_INVALIDO && evaluarLift("") == PESO_INVALIDO);
  assert(evaluarLift("abc") == PESO_INVALIDO && evaluarLift("0") == PESO_INVALIDO);
  assert(evaluarLift("-2") == PESO_INVALIDO && evaluarLift("nan") == PESO_INVALIDO);
  assert(evaluarLift("5x") == PESO_INVALIDO);
  assert(evaluarLift("11.8") == OVERWEIGHT && evaluarLift("10.1") == OVERWEIGHT);
  assert(evaluarLift("10.0") == LIFT_OK && evaluarLift("0.1") == LIFT_OK);
  assert(elevacionSolicitar(NULL) == PESO_INVALIDO && !elevacionActiva());
  assert(elevacionSolicitar("11.8") == OVERWEIGHT && !elevacionActiva());
  assert(elevacionSolicitar("0.1") == LIFT_OK && elevacionActiva());
  elevacionActualizarEn(7999); assert(elevacionActiva());
  elevacionActualizarEn(8000); assert(!elevacionActiva());
  puts("OK");
}
