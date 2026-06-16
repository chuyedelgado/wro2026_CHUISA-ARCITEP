"""
telemetria_rx_test.py — Equipo CHUISA ARCITEP (WRO 2026 Future Engineers)

PAPEL EN LA MISIÓN:
    Lado Raspberry Pi: recibe la telemetria del Arduino, verifica el checksum
    (XOR) y descarta los mensajes corruptos. Es la base de como la Pi leera los
    sensores en tiempo real para la maquina de estados y el PID.

FORMATO RECIBIDO (alcance actual):  T<tof_izq>,<tof_der>,<yaw>*<checksum>
    (la version completa de la arquitectura agregara el 3er ToF y el encoder).

PUERTO: /dev/ttyAMA0 (alternativa /dev/serial0).
"""

import serial
import time

PUERTO = "/dev/ttyAMA0"
BAUD = 115200

ser = serial.Serial(PUERTO, BAUD, timeout=1)
time.sleep(2)


def checksum_xor(texto: str) -> int:
    cs = 0
    for c in texto:
        cs ^= ord(c)
    return cs


print("Escuchando telemetria del Arduino... (Ctrl+C para salir)")
try:
    while True:
        linea = ser.readline().decode("utf-8", errors="ignore").strip()
        if not linea or not linea.startswith("T") or "*" not in linea:
            continue

        cuerpo, _, cs_txt = linea.partition("*")
        try:
            cs_recibido = int(cs_txt)
        except ValueError:
            continue

        if cs_recibido != checksum_xor(cuerpo):
            print("DESCARTADO (checksum):", linea)
            continue

        datos = cuerpo[1:].split(",")   # quita la 'T'
        if len(datos) == 3:
            izq, der, yaw = datos
            print(f"ToF Izq: {izq} mm  |  ToF Der: {der} mm  |  Yaw: {yaw} grados")
except KeyboardInterrupt:
    print("\nDetenido por el usuario.")
    ser.close()
