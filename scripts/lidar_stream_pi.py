"""Emite una línea JSON por vuelta del RPLIDAR A1, sin parar (se ejecuta EN la Pi, lo lanza ver_lidar.sh vivo).

Cada línea es una lista de pares (ángulo, distancia_cm) en el marco del robot: 0° al frente, positivo a
la izquierda. Termina (y apaga el motor) cuando el lector cierra la tubería o con Ctrl+C.
"""
import json
import sys
import time

sys.path.insert(0, "/home/koleo")
import serial
import rplidar_leer as L

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=2)
ser.dtr = False  # CP2102: DTR bajo = motor encendido
time.sleep(0.5)
try:
    L.enviar(ser, L.CMD_STOP)
    time.sleep(0.5)
    ser.reset_input_buffer()
    L.salud(ser)
    time.sleep(1.5)
    v = []
    primera = True
    for nueva, _q, ang, d in L.escanear(ser):
        if nueva and v:
            if primera:  # la primera vuelta puede venir parcial
                primera = False
            else:
                sys.stdout.write(json.dumps(v) + "\n")
                sys.stdout.flush()
            v = []
        if d > 0:
            a = (0.0 - ang + 180.0) % 360.0 - 180.0
            v.append((180.0 if a == -180.0 else a, d / 10.0))
except (BrokenPipeError, KeyboardInterrupt):
    pass
finally:
    try:
        L.enviar(ser, L.CMD_STOP)
    except Exception:
        pass
    ser.dtr = True
    ser.close()
