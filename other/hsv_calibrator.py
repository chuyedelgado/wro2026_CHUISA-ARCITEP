import cv2
import numpy as np
from picamera2 import Picamera2
import time

# ===================== AJUSTES =====================
SWAP_RB = False    # Si los colores se ven invertidos (rojo se ve azul), pon True
USE_UNDISTORT = False
CALIB_FILE = "config/camera_calibration_fisheye.npz"
SIZE = (320, 240)
# ===================================================

# --- Cargar calibración fisheye: calibramos sobre lo MISMO que verá el robot ---
map1 = map2 = None
if USE_UNDISTORT:
    try:
        data = np.load(CALIB_FILE)
        K, D = data["camera_matrix"], data["dist_coeffs"]
        w, h = SIZE
        newK = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(
            K, D, (w, h), np.eye(3), balance=0.0)
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(
            K, D, np.eye(3), newK, (w, h), cv2.CV_16SC2)
        print("Calibración fisheye cargada: se mostrará la imagen corregida.")
    except Exception as e:
        print(f"(Aviso) No cargué la calibración ({e}). Sigo sin undistort.")

# --- Sliders ---
def nada(x): pass
cv2.namedWindow("Controles", cv2.WINDOW_NORMAL)
for name, val, mx in [("H min",0,179),("H max",179,179),("S min",0,255),
                      ("S max",255,255),("V min",0,255),("V max",255,255)]:
    cv2.createTrackbar(name, "Controles", val, mx, nada)

# --- Cámara ---
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(
    main={"size": SIZE, "format": "RGB888"}))
picam2.start()
time.sleep(2)

# Bloquear exposición y balance de blancos con lo que el auto eligió
md = picam2.capture_metadata()
picam2.set_controls({
    "AeEnable": False,                          # apaga auto-exposición
    "AwbEnable": False,                         # apaga auto-balance de blancos
    "ExposureTime": int(md["ExposureTime"]),
    "AnalogueGain": float(md["AnalogueGain"]),
    "ColourGains": tuple(md["ColourGains"]),
})
time.sleep(0.5)
print(f"Exposicion bloqueada: {md['ExposureTime']} us, gain {md['AnalogueGain']:.2f}")

print("\nApunta a un pilar. Ajusta los sliders hasta que SOLO ese color quede blanco.")
print("Teclas:  p = imprimir valores   |   q = salir\n")

while True:
    frame = picam2.capture_array()
    if SWAP_RB:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)   # 'frame' queda en BGR
    if map1 is not None:
        frame = cv2.remap(frame, map1, map2, cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    g = lambda n: cv2.getTrackbarPos(n, "Controles")
    lower = np.array([g("H min"), g("S min"), g("V min")])
    upper = np.array([g("H max"), g("S max"), g("V max")])

    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    combo = np.hstack((frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), result))
    cv2.imshow("Original | Mascara | Resultado", combo)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('p'):
        print(f"  lower = [{lower[0]}, {lower[1]}, {lower[2]}]   "
              f"upper = [{upper[0]}, {upper[1]}, {upper[2]}]")
    elif key == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
