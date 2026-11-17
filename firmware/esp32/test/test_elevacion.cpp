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
  // H-3: un LIFT valido con elevacion activa no reinicia el limite de 8 s
  assert(elevacionSolicitarEn("5", 1000) == LIFT_OK && elevacionActiva());
  assert(elevacionSolicitarEn("5", 5000) == LIFT_OK);
  elevacionActualizarEn(8999); assert(elevacionActiva());
  elevacionActualizarEn(9000); assert(!elevacionActiva());
  // H-4: valor > 10 que redondea a 10.0f en float sigue siendo OVERWEIGHT
  assert(evaluarLift("10.0000000001") == OVERWEIGHT);
  // H-1: corte por temporizador sin que nadie llame a elevacionActualizar
  elevacionActualizarEn(100000); assert(!elevacionActiva());
  assert(elevacionSolicitarEn("5", 20000) == LIFT_OK && elevacionActiva());
  elevacionCorteTimerEn(27999); assert(elevacionActiva());
  elevacionCorteTimerEn(28000); assert(!elevacionActiva());
  // sin carrera: corte normal y luego callback tardio es idempotente
  assert(elevacionSolicitarEn("5", 30000) == LIFT_OK);
  elevacionActualizarEn(38000); assert(!elevacionActiva());
  elevacionCorteTimerEn(38000); assert(!elevacionActiva());
  // callback tardio de la elevacion anterior no corta una elevacion nueva
  assert(elevacionSolicitarEn("5", 38100) == LIFT_OK && elevacionActiva());
  elevacionCorteTimerEn(38200); assert(elevacionActiva());
  elevacionCorteTimerEn(46100); assert(!elevacionActiva());
  // envoltura de reloj uint32
  assert(elevacionSolicitarEn("5", 0xFFFFF000u) == LIFT_OK);
  elevacionCorteTimerEn(0xFFFFF000u + 7999u); assert(elevacionActiva());
  elevacionCorteTimerEn(0xFFFFF000u + 8000u); assert(!elevacionActiva());
  puts("OK");
}
