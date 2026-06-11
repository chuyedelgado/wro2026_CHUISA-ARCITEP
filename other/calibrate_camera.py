import cv2, numpy as np, glob, os

PATTERN_SIZE = (8, 5)                       # igual que en la captura
IMAGES_GLOB  = "calib_images/*.jpg"
OUTPUT       = "config/camera_calibration.npz"
os.makedirs("config", exist_ok=True)

# Puntos 3D del tablero. Usamos cuadrados de tamaño 1: el tamaño real NO afecta
# la corrección de distorsión (solo importaría para medir distancias absolutas).
objp = np.zeros((PATTERN_SIZE[0]*PATTERN_SIZE[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:PATTERN_SIZE[0], 0:PATTERN_SIZE[1]].T.reshape(-1, 2)

objpoints, imgpoints = [], []
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

images = sorted(glob.glob(IMAGES_GLOB))
print(f"Procesando {len(images)} imágenes...")
shape = None
for f in images:
    img = cv2.imread(f)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    shape = gray.shape[::-1]
    found, corners = cv2.findChessboardCorners(gray, PATTERN_SIZE, None)
    if found:
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        objpoints.append(objp); imgpoints.append(corners)
        print(f"  ✓ {os.path.basename(f)}")
    else:
        print(f"  ✗ {os.path.basename(f)} (ignorada)")

print(f"\n{len(objpoints)} imágenes usables.")
if len(objpoints) < 10:
    print("⚠️ Pocas. Captura más fotos variadas y repite.")
    raise SystemExit

err, K, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, shape, None, None)
print(f"\nError de reproyección (menor = mejor; ideal < 0.5 px): {err:.4f}")

np.savez(OUTPUT, camera_matrix=K, dist_coeffs=dist)
print(f"Guardado: {OUTPUT}")

# Prueba visual antes/después
sample = cv2.imread(images[0]); h, w = sample.shape[:2]
newK, _ = cv2.getOptimalNewCameraMatrix(K, dist, (w, h), 1, (w, h))
undist = cv2.undistort(sample, K, dist, None, newK)
cv2.imwrite("comparacion_calibracion.jpg", np.hstack((sample, undist)))
print("Comparación lado a lado: comparacion_calibracion.jpg")

