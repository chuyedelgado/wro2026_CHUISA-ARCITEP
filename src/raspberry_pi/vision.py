"""
vision.py — WRO 2026 Future Engineers — [TEAM NAME]
====================================================
Camera capture and computer vision processing module.

Uses OpenCV with HSV color space for detection of:
  - Orange / Blue wall lines → determine driving direction + section transitions
  - Red pillars   → traffic sign: vehicle must pass on the RIGHT
  - Green pillars → traffic sign: vehicle must pass on the LEFT
  - Magenta markers → parking lot delimiters

Architecture:
  VisionSystem runs a dedicated background thread (_capture_loop) that
  continuously captures and processes frames. The state machine reads
  the latest Detection result via get_latest() without blocking.

  This threading approach avoids the state machine waiting for I/O
  on each loop iteration (camera reads are ~10-30ms each).
"""

import cv2
import numpy as np
import threading
import time
from dataclasses import dataclass, field
from typing import Optional, Tuple
from config import Config

# Type alias for a detected object: (centroid_x, centroid_y, area_px)
ObjectDetection = Tuple[int, int, int]


@dataclass
class Detection:
    """
    Processed result from a single camera frame.
    All coordinates are in the cropped ROI space.
    """
    # Driving direction determined from first wall line color seen
    direction: str = "UNKNOWN"          # "CW", "CCW", or "UNKNOWN"

    # Wall line visibility (used for section/turn counting)
    orange_line_visible: bool = False
    blue_line_visible: bool = False

    # Pillar detections: (centroid_x, centroid_y, area) or None
    red_pillar:   Optional[ObjectDetection] = None
    green_pillar: Optional[ObjectDetection] = None

    # Parking markers: (centroid_x, centroid_y) or None
    magenta_left:  Optional[Tuple[int, int]] = None
    magenta_right: Optional[Tuple[int, int]] = None

    # Frame metadata
    frame_width:  int = 0
    frame_height: int = 0
    fps:          float = 0.0
    timestamp:    float = field(default_factory=time.time)

    @property
    def has_obstacle(self) -> bool:
        return self.red_pillar is not None or self.green_pillar is not None

    @property
    def parking_markers_visible(self) -> bool:
        return self.magenta_left is not None and self.magenta_right is not None


class VisionSystem:
    """
    Manages camera and processes frames in a background thread.

    Usage:
        vision = VisionSystem(config)
        vision.start()
        ...
        d = vision.get_latest()
        if d and d.red_pillar:
            cx, cy, area = d.red_pillar
        ...
        vision.stop()
    """

    def __init__(self, config: Config):
        self.config = config
        self._camera = None
        self._latest: Optional[Detection] = None
        self._lock = threading.Lock()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._frame_count = 0
        self._fps_start = time.time()
        self._current_fps = 0.0

        self._init_camera()

    # ── Public API ────────────────────────────────────────────────────────────

    def start(self):
        """Start the background capture + processing thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(
            target=self._capture_loop, daemon=True, name="vision-thread"
        )
        self._thread.start()
        print("[VISION] Camera thread started.")

    def stop(self):
        """Stop the background thread and release camera."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=3.0)
        if self._camera:
            self._camera.stop()
        print("[VISION] Camera stopped.")

    def get_latest(self) -> Optional[Detection]:
        """
        Thread-safe access to the most recent detection result.
        Returns None if no frame has been processed yet.
        """
        with self._lock:
            return self._latest

    def get_debug_frame(self) -> Optional[np.ndarray]:
        """
        Returns an annotated frame for debugging/visualization.
        Not used in competition — only for development.
        """
        with self._lock:
            d = self._latest
        if d is None:
            return None
        # [TODO: draw bounding boxes, centroid markers, state info on frame]
        return None

    # ── Camera Init ───────────────────────────────────────────────────────────

    def _init_camera(self):
        """Initialize Raspberry Pi Camera Module 3 via picamera2."""
        try:
            from picamera2 import Picamera2
            self._camera = Picamera2()
            cam_config = self._camera.create_preview_configuration(
                main={
                    "size": (self.config.FRAME_WIDTH, self.config.FRAME_HEIGHT),
                    "format": "RGB888"
                }
            )
            self._camera.configure(cam_config)
            self._camera.start()
            time.sleep(0.5)  # Let camera exposure stabilize
            print(f"[VISION] Pi Camera initialized: "
                  f"{self.config.FRAME_WIDTH}×{self.config.FRAME_HEIGHT} @ {self.config.TARGET_FPS}fps")
        except ImportError:
            # Fallback for development on non-Pi machine
            print("[VISION] WARNING: picamera2 not found. Using OpenCV VideoCapture.")
            self._camera = cv2.VideoCapture(0)
            self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.FRAME_WIDTH)
            self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.FRAME_HEIGHT)

    def _capture_frame(self) -> Optional[np.ndarray]:
        """Capture one frame from camera (handles both picamera2 and cv2)."""
        try:
            from picamera2 import Picamera2
            if isinstance(self._camera, Picamera2):
                return self._camera.capture_array()
        except ImportError:
            pass
        if self._camera:
            ret, frame = self._camera.read()
            return frame if ret else None
        return None

    # ── Capture Loop ─────────────────────────────────────────────────────────

    def _capture_loop(self):
        """Main loop: capture frame → process → store result. Runs in thread."""
        while self._running:
            frame = self._capture_frame()
            if frame is None:
                time.sleep(0.01)
                continue

            detection = self._process_frame(frame)

            # Track FPS
            self._frame_count += 1
            elapsed = time.time() - self._fps_start
            if elapsed >= 1.0:
                self._current_fps = self._frame_count / elapsed
                self._frame_count = 0
                self._fps_start = time.time()
            detection.fps = self._current_fps

            with self._lock:
                self._latest = detection

    # ── Processing Pipeline ───────────────────────────────────────────────────

    def _process_frame(self, frame: np.ndarray) -> Detection:
        """
        Full processing pipeline for one frame.
        Steps: crop ROI → convert HSV → detect each color → return Detection.
        """
        cfg = self.config

        # Convert RGB→HSV (picamera2 returns RGB, OpenCV expects BGR or HSV)
        # If using cv2.VideoCapture (BGR input), use cv2.COLOR_BGR2HSV instead
        hsv_full = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        # Crop to Region of Interest (removes sky/background above walls)
        roi = hsv_full[cfg.ROI_TOP:cfg.ROI_BOTTOM, :]

        # Apply light denoise to reduce sensor noise
        roi_blur = cv2.GaussianBlur(roi, (5, 5), 0)

        h, w = frame.shape[:2]

        # Detect each game element
        red   = self._detect_red_pillar(roi_blur)
        green = self._detect_green_pillar(roi_blur)
        m_l, m_r = self._detect_magenta(roi_blur, w)
        orange = self._detect_orange_line(roi_blur)
        blue   = self._detect_blue_line(roi_blur)
        direction = self._determine_direction(roi_blur, w)

        return Detection(
            direction=direction,
            orange_line_visible=orange,
            blue_line_visible=blue,
            red_pillar=red,
            green_pillar=green,
            magenta_left=m_l,
            magenta_right=m_r,
            frame_width=w,
            frame_height=h,
        )

    # ── Individual Detectors ──────────────────────────────────────────────────

    def _detect_red_pillar(self, roi: np.ndarray) -> Optional[ObjectDetection]:
        """
        Red wraps around H=0/180 in OpenCV HSV → need two masks combined.
        Red pillar = traffic sign to pass on the RIGHT.
        """
        cfg = self.config
        mask1 = cv2.inRange(roi, cfg.HSV_RED_LOW1, cfg.HSV_RED_HIGH1)
        mask2 = cv2.inRange(roi, cfg.HSV_RED_LOW2, cfg.HSV_RED_HIGH2)
        mask = cv2.bitwise_or(mask1, mask2)
        # Closing: fill holes inside the mask (dilation then erosion)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        return self._largest_contour(mask, cfg.PILLAR_MIN_AREA)

    def _detect_green_pillar(self, roi: np.ndarray) -> Optional[ObjectDetection]:
        """
        Green pillar = traffic sign to pass on the LEFT.
        """
        cfg = self.config
        mask = cv2.inRange(roi, cfg.HSV_GREEN_LOW, cfg.HSV_GREEN_HIGH)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        return self._largest_contour(mask, cfg.PILLAR_MIN_AREA)

    def _detect_magenta(
        self, roi: np.ndarray, frame_width: int
    ) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
        """
        Detect left and right magenta parking delimiters.
        Split frame into left and right halves for separation.
        Returns (left_centroid, right_centroid), each is (x, y) or None.
        """
        cfg = self.config
        mask = cv2.inRange(roi, cfg.HSV_MAGENTA_LOW, cfg.HSV_MAGENTA_HIGH)
        mid = frame_width // 2

        mask_left  = mask.copy(); mask_left[:,  mid:] = 0
        mask_right = mask.copy(); mask_right[:, :mid] = 0

        det_left  = self._largest_contour(mask_left,  cfg.MAGENTA_MIN_AREA)
        det_right = self._largest_contour(mask_right, cfg.MAGENTA_MIN_AREA)

        l = (det_left[0],  det_left[1])  if det_left  else None
        r = (det_right[0], det_right[1]) if det_right else None
        return l, r

    def _detect_orange_line(self, roi: np.ndarray) -> bool:
        """
        Detect orange wall-direction line.
        Returns True if enough orange pixels are present in ROI.
        """
        cfg = self.config
        mask = cv2.inRange(roi, cfg.HSV_ORANGE_LOW, cfg.HSV_ORANGE_HIGH)
        return int(cv2.countNonZero(mask)) > cfg.LINE_MIN_PIXELS

    def _detect_blue_line(self, roi: np.ndarray) -> bool:
        """
        Detect blue wall-direction line.
        """
        cfg = self.config
        mask = cv2.inRange(roi, cfg.HSV_BLUE_LOW, cfg.HSV_BLUE_HIGH)
        return int(cv2.countNonZero(mask)) > cfg.LINE_MIN_PIXELS

    def _determine_direction(self, roi: np.ndarray, frame_width: int) -> str:
        """
        Determine CW vs CCW driving direction.
        Logic: measure which side (left or right half of frame) has more
        orange/blue line pixels. Orange dominant on right → CW. Blue → CCW.
        TODO: refine based on actual field testing.
        """
        cfg = self.config
        mid = frame_width // 2

        orange_mask = cv2.inRange(roi, cfg.HSV_ORANGE_LOW, cfg.HSV_ORANGE_HIGH)
        blue_mask   = cv2.inRange(roi, cfg.HSV_BLUE_LOW, cfg.HSV_BLUE_HIGH)

        orange_right = cv2.countNonZero(orange_mask[:, mid:])
        blue_right   = cv2.countNonZero(blue_mask[:,   mid:])

        if orange_right > cfg.LINE_MIN_PIXELS:
            return "CW"
        elif blue_right > cfg.LINE_MIN_PIXELS:
            return "CCW"
        return "UNKNOWN"

    # ── Utility ───────────────────────────────────────────────────────────────

    def _largest_contour(
        self, mask: np.ndarray, min_area: int
    ) -> Optional[ObjectDetection]:
        """
        Find the largest contour in a binary mask.
        Returns (centroid_x, centroid_y, area) or None if below min_area.
        """
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if not contours:
            return None

        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)

        if area < min_area:
            return None

        # Compute centroid using image moments
        M = cv2.moments(largest)
        if M["m00"] == 0:
            return None

        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return (cx, cy, int(area))
