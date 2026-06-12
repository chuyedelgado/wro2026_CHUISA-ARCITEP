"""
config.py — WRO 2026 Future Engineers — CHUISA ARCITEP
====================================================
Central configuration file. All tunable parameters live here.

COMPETITION RULE (Rule 9.9): Introducing data via physical adjustments
is NOT permitted during competition. All calibration must happen here,
before the round starts.

Usage:
    from config import Config
    cfg = Config()
    print(cfg.HSV_RED_LOW1)
"""

import numpy as np


class Config:
    """
    All system parameters grouped by subsystem.
    Tune these values during practice sessions.
    """

    # ── Challenge mode ────────────────────────────────────────────────────────
    # Set this before each round. "OPEN" or "OBSTACLE".
    CHALLENGE = "OBSTACLE"

    # ── Camera ────────────────────────────────────────────────────────────────
    FRAME_WIDTH  = 320      # Resolution width (pixels)
    FRAME_HEIGHT = 240      # Resolution height (pixels)
    TARGET_FPS   = 30       # Target frames per second

    # Region of Interest: crop out background above walls and floor below
    # Tune by watching the camera feed and identifying where walls appear
    ROI_TOP    = 60         # Pixels from top where ROI starts
    ROI_BOTTOM = 200        # Pixels from top where ROI ends

    # ── HSV Color Thresholds ─────────────────────────────────────────────────
    # IMPORTANT: Tune these at each new venue using calibration.py
    # OpenCV uses H: 0-179, S: 0-255, V: 0-255
    #
    # Quick calibration process:
    #   1. Run: python3 other/calibration.py
    #   2. Point camera at each game element
    #   3. Adjust trackbars until mask is clean (solid white on target, black elsewhere)
    #   4. Copy final values here

    # Orange lines (wall direction, H: ~10-25 in OpenCV scale)
    HSV_ORANGE_LOW  = np.array([10, 120, 100])
    HSV_ORANGE_HIGH = np.array([25, 255, 255])

    # Blue lines (wall direction, H: ~100-130)
    HSV_BLUE_LOW  = np.array([100, 100,  80])
    HSV_BLUE_HIGH = np.array([130, 255, 255])

    # Red pillars — IMPORTANT: Red wraps around H=0/180, needs TWO ranges
    HSV_RED_LOW1  = np.array([  0, 120,  80])
    HSV_RED_HIGH1 = np.array([  8, 255, 255])
    HSV_RED_LOW2  = np.array([172, 120,  80])
    HSV_RED_HIGH2 = np.array([180, 255, 255])

    # Green pillars (H: ~45-80)
    HSV_GREEN_LOW  = np.array([ 45,  80,  60])
    HSV_GREEN_HIGH = np.array([ 80, 255, 255])

    # Magenta parking markers (H: ~140-165)
    HSV_MAGENTA_LOW  = np.array([140,  80,  80])
    HSV_MAGENTA_HIGH = np.array([165, 255, 255])

    # ── Detection Thresholds ─────────────────────────────────────────────────
    LINE_MIN_PIXELS   = 300   # Min white pixels in mask to confirm a line
    PILLAR_MIN_AREA   = 500   # Min contour area (px²) to confirm a pillar
    MAGENTA_MIN_AREA  = 200   # Min contour area for parking marker detection

    # ── PID Control ──────────────────────────────────────────────────────────
    # Proportional-Integral-Derivative gains for steering correction.
    # Tuning procedure:
    #   1. Set Ki=0, Kd=0. Increase Kp until vehicle oscillates. Back off 50%.
    #   2. Increase Kd until oscillations dampen. Do not exceed ~0.5.
    #   3. Add small Ki (0.001–0.05) to eliminate steady-state drift.
    PID_KP = 0.80    # Proportional gain (primary steering response)
    PID_KI = 0.01    # Integral gain (eliminates long-term drift, small!)
    PID_KD = 0.10    # Derivative gain (dampens oscillations)

    # ── Speed Control ────────────────────────────────────────────────────────
    # Values are 0.0–1.0 relative to max motor PWM.
    # Decision rationale: see README.md Section 1.3
    BASE_SPEED             = 0.45   # Normal driving speed
    PARKING_APPROACH_SPEED = 0.25   # Slow approach when searching for parking
    PARKING_REVERSE_SPEED  = 0.20   # Reverse speed during parking maneuver

    # ── Pillar Avoidance ─────────────────────────────────────────────────────
    # When a pillar is detected, we shift the target x-position in the frame
    # so the PID steers the vehicle to pass on the correct side.
    #
    # RED pillar → pass on RIGHT → target shifts LEFT in frame
    # GREEN pillar → pass on LEFT → target shifts RIGHT in frame
    #
    # Unit: pixels from frame center. Tune based on vehicle width vs lane width.
    RED_OFFSET   = 60    # Pixels to offset target for red pillar avoidance
    GREEN_OFFSET = 60    # Pixels to offset target for green pillar avoidance

    # ── Lap Counting ─────────────────────────────────────────────────────────
    TARGET_LAPS     = 3     # Number of full laps required
    SECTIONS_PER_LAP = 8    # 4 straight + 4 curve sections per lap
    TURN_ANGLE_THRESHOLD = 75.0   # Degrees of yaw change to count a 90° turn

    # ── Communication ────────────────────────────────────────────────────────
    # Find Arduino port on Raspberry Pi with: ls /dev/tty*
    # Typical values: /dev/ttyUSB0 or /dev/ttyACM0
    ARDUINO_PORT = "/dev/ttyUSB0"
    BAUD_RATE    = 115200

    # ── Safety ───────────────────────────────────────────────────────────────
    # If no valid sensor data is received for this many milliseconds, stop.
    COMM_TIMEOUT_MS = 500

# ============================================================
# RANGOS HSV DE COLOR  (formato OpenCV: H 0-179, S 0-255, V 0-255)
# Calibrados con other/hsv_calibrator.py
# Perfil: NORMAL | Luz: [ANOTA TU CONDICION, ej. artificial taller]
# Fecha: [ANOTA LA FECHA]
# ============================================================
import numpy as np

# VERDE — un solo rango (calibrado y verificado)
GREEN_HSV_LOWER = np.array([35,  70,  50])
GREEN_HSV_UPPER = np.array([85, 255, 255])

# ROJO — DOBLE rango (vive en los dos extremos del Hue). PROVISIONAL: calibrar.
RED_HSV_LOWER_1 = np.array([0,   70, 34])    # rango bajo (H ~0-10)
RED_HSV_UPPER_1 = np.array([10,  255, 255])
RED_HSV_LOWER_2 = np.array([170, 70, 34])    # rango alto (H ~170-179)
RED_HSV_UPPER_2 = np.array([179, 255, 255])
