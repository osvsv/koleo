"""Captura N vueltas del RPLIDAR A1 en la Raspberry Pi (se ejecuta EN la Pi, lo lanza ver_lidar.sh).

Usa ~/rplidar_leer.py de la Pi (pyserial crudo; enciende el motor con DTR bajo, como exige el
adaptador CP2102). Guarda /tmp/koleo_cap/vueltas.json con pares (ángulo, distancia_cm) en el marco
del robot: 0° al frente, positivo a la izquierda.
"""
import json
import sys
import time

sys.path.insert(0, "/home/koleo")
import serial
import rplidar_leer as L

n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=2)
ser.dtr = False
time.sleep(0.5)
vueltas = []
try:
    L.enviar(ser, L.CMD_STOP)
    time.sleep(0.5)
    ser.reset_input_buffer()
    L.salud(ser)
    time.sleep(1.5)
    v = []
    for nueva, _q, ang, d in L.escanear(ser):
        if nueva and v:
            vueltas.append(v)
            v = []
            if len(vueltas) >= n + 1:
                break
        if d > 0:
            a = (0.0 - ang + 180.0) % 360.0 - 180.0
            v.append((180.0 if a == -180.0 else a, d / 10.0))
finally:
    try:
        L.enviar(ser, L.CMD_STOP)
    except Exception:
        pass
    ser.dtr = True
    ser.close()
vueltas = vueltas[1:]  # la primera puede venir parcial
json.dump(vueltas, open("/tmp/koleo_cap/vueltas.json", "w"))
print(len(vueltas), [len(x) for x in vueltas])
