from picamera2 import Picamera2
import cv2, time, os

PATTERN_SIZE = (8, 5)        # esquinas INTERNAS del tablero (no cuadrados)
SAVE_DIR = "calib_images"
TARGET_GOOD = 20             # cuántas fotos buenas queremos

os.makedirs(SAVE_DIR, exist_ok=True)

picam2 = Picamera2()
# Calibramos a la MISMA resolución que usará el robot (320x240): así la
# calibración sirve directo, sin reescalar nada.
config = picam2.create_preview_configuration(main={"size": (320, 240), "format": "RGB888"})
picam2.configure(config)
picam2.start()
time.sleep(2)

good = 0
print(f"Capturaremos {TARGET_GOOD} fotos buenas del tablero {PATTERN_SIZE}.")
print("Entre fotos, MUEVE el tablero: inclinado, cerca, lejos, rotado y en las ORILLAS.")
print("El tablero debe estar PLANO y bien iluminado, sin brillos.\n")

while good < TARGET_GOOD:
    input(f"[{good}/{TARGET_GOOD}] Coloca el tablero y presiona ENTER...")
    frame = picam2.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    found, corners = cv2.findChessboardCorners(gray, PATTERN_SIZE, None)
    if found:
        good += 1
        path = os.path.join(SAVE_DIR, f"calib_{good:02d}.jpg")
        cv2.imwrite(path, frame)   # el color no importa para calibrar (solo geometría)
        print(f"  ✓ Tablero detectado. Guardada {path}")
    else:
        print("  ✗ No se detectó. Revisa: todo el tablero visible, buena luz, sin reflejos, sin movimiento.")

picam2.stop()
print(f"\nListo: {good} fotos en '{SAVE_DIR}/'. Ahora corre el script de calibración.")
