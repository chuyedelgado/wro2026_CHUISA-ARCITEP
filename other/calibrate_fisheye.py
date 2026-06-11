import cv2, numpy as np, glob, os

PATTERN_SIZE = (8,5)   # ⬅️ PON AQUÍ EL MISMO VALOR QUE EN capture_calibration.py
IMAGES_GLOB  = "calib_images/*.jpg"
OUTPUT       = "config/camera_calibration_fisheye.npz"
os.makedirs("config", exist_ok=True)

# El modelo fisheye exige los puntos 3D con forma (1, N, 3)
objp = np.zeros((1, PATTERN_SIZE[0]*PATTERN_SIZE[1], 3), np.float64)
objp[0, :, :2] = np.mgrid[0:PATTERN_SIZE[0], 0:PATTERN_SIZE[1]].T.reshape(-1, 2)

objpoints, imgpoints = [], []
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)

images = sorted(glob.glob(IMAGES_GLOB))
print(f"Procesando {len(images)} imágenes con modelo FISHEYE...")
shape = None
for f in images:
    img = cv2.imread(f)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    shape = gray.shape[::-1]
    found, corners = cv2.findChessboardCorners(gray, PATTERN_SIZE, None)
    if found:
        # Ventana pequeña (5x5): a 320x240 los cuadros son chicos, una ventana grande estorba
        corners = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)
        objpoints.append(objp)
        imgpoints.append(corners)
        print(f"  ✓ {os.path.basename(f)}")
    else:
        print(f"  ✗ {os.path.basename(f)} (ignorada)")

N = len(objpoints)
print(f"\n{N} imágenes usables.")
if N < 10:
    print("⚠️ Pocas. Repite la captura."); raise SystemExit

K = np.zeros((3, 3))
D = np.zeros((4, 1))
rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for _ in range(N)]
tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for _ in range(N)]
flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_FIX_SKEW

rms, K, D, _, _ = cv2.fisheye.calibrate(
    objpoints, imgpoints, shape, K, D, rvecs, tvecs, flags, criteria)

print(f"\nError de reproyección FISHEYE (menor = mejor): {rms:.4f}")
np.savez(OUTPUT, camera_matrix=K, dist_coeffs=D, model="fisheye", image_size=shape)
print(f"Guardado: {OUTPUT}")

# Comparación antes/después (el fisheye usa funciones propias, no cv2.undistort)
sample = cv2.imread(images[0]); h, w = sample.shape[:2]
newK = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, (w, h), np.eye(3), balance=0.0)
map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), newK, (w, h), cv2.CV_16SC2)
undist = cv2.remap(sample, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
cv2.imwrite("comparacion_fisheye.jpg", np.hstack((sample, undist)))
print("Comparación: comparacion_fisheye.jpg")
