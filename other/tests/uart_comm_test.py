"""
uart_comm_test.py — Equipo CHUISA ARCITEP (WRO 2026 Future Engineers)

PAPEL EN LA MISIÓN:
    Lado Raspberry Pi del enlace UART. Envia comandos al Arduino con el
    formato  S<steer>,<speed>*<checksum>  (checksum XOR). Es la semilla del
    modulo de protocolo final (uart_comm.py).

PUERTO: /dev/ttyAMA0 (UART de los pines GPIO en la Pi 5; alternativa /dev/serial0).
SEGURIDAD: la linea Arduino-TX -> Pi-RX pasa por un divisor de voltaje (1k/2.2k).
"""

import serial
import time

PUERTO = "/dev/ttyAMA0"     # si no funciona, probar "/dev/serial0"
BAUD = 115200

ser = serial.Serial(PUERTO, BAUD, timeout=1)
time.sleep(2)               # dar tiempo a que el enlace se estabilice


def checksum_xor(texto: str) -> int:
    """XOR de todos los caracteres del texto."""
    cs = 0
    for c in texto:
        cs ^= ord(c)
    return cs


def enviar_comando(steer: int, speed: int) -> None:
    """Arma 'S<steer>,<speed>*<checksum>' y lo envia por UART."""
    cuerpo = f"S{steer},{speed}"
    mensaje = f"{cuerpo}*{checksum_xor(cuerpo)}\n"
    ser.write(mensaje.encode("utf-8"))
    print("Envie:", mensaje.strip())


if __name__ == "__main__":
    print("Enviando comandos con checksum a 10/seg... (Ctrl+C para salir)")
    velocidad = 0
    try:
        while True:
            enviar_comando(0, velocidad)     # steer=0, speed variable
            velocidad += 10
            if velocidad > 100:
                velocidad = 0
            time.sleep(0.1)                  # 10 comandos por segundo (cerca de la operacion real)
    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")
        ser.close()
