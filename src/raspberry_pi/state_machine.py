"""
state_machine.py — WRO 2026 Future Engineers — CHUISA ARCITEP
===========================================================
Finite State Machine for autonomous driving.

States:
    INIT         System initialization and self-check
    DETECT_DIR   Identify CW vs CCW driving direction from wall lines
    OPEN_DRIVE   Open Challenge: 3 laps, wall-following, stop at start section
    OBS_DRIVE    Obstacle Challenge: 3 laps with pillar avoidance
    FIND_PARKING Locate magenta parking markers after completing 3 laps
    PARKING      Execute parallel parking maneuver
    STOP         End of run (all control outputs zeroed)

Transitions are triggered by:
    - Vision detections (colors, pillar positions)
    - Section/lap counter (IMU yaw changes)
    - Timer guards (prevent infinite loops in edge cases)
"""

import time
from enum import Enum, auto
from typing import Optional

from vision import VisionSystem, Detection
from uart_comm import ArduinoComm
from pid_controller import PIDController
from config import Config


class State(Enum):
    INIT         = auto()
    DETECT_DIR   = auto()
    OPEN_DRIVE   = auto()
    OBS_DRIVE    = auto()
    FIND_PARKING = auto()
    PARKING      = auto()
    STOP         = auto()


class StateMachine:
    """
    Main autonomous driving logic.

    Example usage:
        sm = StateMachine(config, vision, comm)
        sm.run()   # blocks until STOP state
    """

    CONTROL_HZ    = 50      # Control loop frequency (Hz)
    CONTROL_DT    = 1.0 / CONTROL_HZ
    TARGET_LAPS   = 3

    def __init__(self, config: Config, vision: VisionSystem, comm: ArduinoComm):
        self.config = config
        self.vision = vision
        self.comm   = comm

        # PID for wall-centering (error = dist_left - dist_right)
        self.pid_wall = PIDController(
            kp=config.PID_KP, ki=config.PID_KI, kd=config.PID_KD,
            output_min=-1.0, output_max=1.0
        )
        # PID for pillar avoidance (error = pillar_cx - target_cx)
        self.pid_pillar = PIDController(
            kp=0.010, ki=0.0, kd=0.002,
            output_min=-1.0, output_max=1.0
        )

        # State variables
        self.state          = State.INIT
        self.prev_state     = None
        self.direction      = None          # "CW" or "CCW"
        self.section_count  = 0            # Total sections traversed
        self.lap_count      = 0            # Full laps completed
        self.last_turn_yaw  = 0.0          # IMU yaw at last counted turn
        self.state_start_t  = time.time()  # When current state was entered

        self._log(f"StateMachine initialized. Challenge: {config.CHALLENGE}")

    # ── Public ────────────────────────────────────────────────────────────────

    def run(self):
        """
        Main control loop. Blocks until STOP state is reached.
        Called once after the start button is pressed.
        """
        self.vision.start()
        self._transition(State.DETECT_DIR)

        while self.state != State.STOP:
            loop_start = time.time()

            detection = self.vision.get_latest()
            sensors   = self.comm.get_sensors()

            if detection is not None and sensors is not None:
                self._update(detection, sensors)
            else:
                self._log("WARNING: No detection or sensor data available.")

            # Maintain control loop frequency
            elapsed = time.time() - loop_start
            sleep_t = self.CONTROL_DT - elapsed
            if sleep_t > 0:
                time.sleep(sleep_t)

        self.vision.stop()
        self.comm.stop_vehicle()
        self._log("Run complete. Vehicle stopped.")

    # ── Core State Logic ─────────────────────────────────────────────────────

    def _update(self, d: Detection, sensors: dict):
        """Dispatch to the correct handler for the current state."""
        if self.state == State.DETECT_DIR:
            self._state_detect_dir(d)
        elif self.state == State.OPEN_DRIVE:
            self._state_open_drive(d, sensors)
        elif self.state == State.OBS_DRIVE:
            self._state_obs_drive(d, sensors)
        elif self.state == State.FIND_PARKING:
            self._state_find_parking(d, sensors)
        elif self.state == State.PARKING:
            self._state_parking(d, sensors)

    def _state_detect_dir(self, d: Detection):
        """
        Detect driving direction by observing the first wall line color.
        Guard: if direction not found after 3 seconds, default to CW.
        """
        if d.direction != "UNKNOWN":
            self.direction = d.direction
            self._log(f"Direction detected: {self.direction}")
            target = State.OPEN_DRIVE if self.config.CHALLENGE == "OPEN" else State.OBS_DRIVE
            self._transition(target)
        elif self._state_elapsed() > 3.0:
            self._log("Direction not detected after 3s. Defaulting to CW.")
            self.direction = "CW"
            target = State.OPEN_DRIVE if self.config.CHALLENGE == "OPEN" else State.OBS_DRIVE
            self._transition(target)

    def _state_open_drive(self, d: Detection, sensors: dict):
        """
        Open Challenge: follow walls via PID, count 3 laps, stop at start section.
        """
        self._wall_follow(sensors)
        self._update_lap_counter(sensors)

        if self.lap_count >= self.TARGET_LAPS:
            self._transition(State.STOP)

    def _state_obs_drive(self, d: Detection, sensors: dict):
        """
        Obstacle Challenge: wall-follow with pillar avoidance overlay.
        After 3 laps, find and enter parking.
        """
        # Determine steering: pillar avoidance overrides wall-following
        if d.red_pillar:
            self._avoid_pillar(d, color="RED")
        elif d.green_pillar:
            self._avoid_pillar(d, color="GREEN")
        else:
            self._wall_follow(sensors)

        self.comm.set_speed(self.config.BASE_SPEED)
        self._update_lap_counter(sensors)

        if self.lap_count >= self.TARGET_LAPS:
            self._transition(State.FIND_PARKING)

    def _state_find_parking(self, d: Detection, sensors: dict):
        """
        After 3 laps, slow down and scan for magenta parking markers.
        Drive slowly forward until both markers are visible.
        """
        self.comm.set_speed(self.config.PARKING_APPROACH_SPEED)
        # Keep roughly centered while searching
        self._wall_follow(sensors, scale=0.5)

        if d.parking_markers_visible:
            self._transition(State.PARKING)

        # Guard: if we searched too long, attempt parking anyway
        if self._state_elapsed() > 10.0:
            self._log("WARNING: Parking markers not found after 10s. Attempting anyway.")
            self._transition(State.PARKING)

    def _state_parking(self, d: Detection, sensors: dict):
        """
        Execute parallel parking sequence.
        The parking lot width is always 20cm (Rule, Section 5).
        The parking lot length is 1.5× vehicle length.

        Sequence:
            1. Align: center vehicle in front of parking lot opening
            2. Overshoot: drive past the right magenta marker
            3. Reverse: turn wheel and reverse into space
            4. Straighten: use IMU to align parallel with wall
            5. Stop: complete when vehicle projection is inside lot
        TODO: Implement and test full sequence. Currently placeholder.
        """
        self.comm.set_speed(0)
        # [TODO: implement full parking sequence with state sub-machine]
        # For now: stop and declare done (partial score)
        self._transition(State.STOP)

    # ── Control Helpers ───────────────────────────────────────────────────────

    def _wall_follow(self, sensors: dict, scale: float = 1.0):
        """
        PID-based wall centering using ToF distances.
        Error = left_distance - right_distance.
        Positive error → too close to left wall → steer right (positive output).
        """
        left  = sensors.get("tof_left",  500)
        right = sensors.get("tof_right", 500)

        # Clamp sensor values to valid range (VL53L1X short mode: 40–1300mm)
        left  = max(40, min(1300, left))
        right = max(40, min(1300, right))

        error   = left - right
        output  = self.pid_wall.compute(error) * scale
        self.comm.set_steering(output)

    def _avoid_pillar(self, d: Detection, color: str):
        """
        Pillar avoidance: shift target x-position in frame so vehicle
        passes on the correct side without triggering a wrong-side penalty.

        RED   → pass on RIGHT → steer left → target_x = center - RED_OFFSET
        GREEN → pass on LEFT  → steer right → target_x = center + GREEN_OFFSET
        """
        cfg = self.config
        frame_center = d.frame_width // 2

        if color == "RED" and d.red_pillar:
            cx = d.red_pillar[0]
            target_x = frame_center - cfg.RED_OFFSET
        elif color == "GREEN" and d.green_pillar:
            cx = d.green_pillar[0]
            target_x = frame_center + cfg.GREEN_OFFSET
        else:
            return

        # Error: positive → pillar is to the right of target → steer right
        error  = cx - target_x
        output = self.pid_pillar.compute(error)
        self.comm.set_steering(-output)  # Invert: steer away from pillar

    def _update_lap_counter(self, sensors: dict):
        """
        Count sections and laps using IMU yaw angle.
        A 90° yaw change (±threshold) indicates crossing a section boundary.
        """
        cfg     = self.config
        current_yaw = sensors.get("yaw", 0.0)
        delta   = abs(current_yaw - self.last_turn_yaw)

        if delta >= cfg.TURN_ANGLE_THRESHOLD:
            self.section_count += 1
            self.last_turn_yaw  = current_yaw

            if self.section_count % cfg.SECTIONS_PER_LAP == 0:
                self.lap_count += 1
                self._log(f"Lap {self.lap_count}/{self.TARGET_LAPS} complete. "
                          f"Sections: {self.section_count}")

    # ── Utilities ─────────────────────────────────────────────────────────────

    def _transition(self, new_state: State):
        """Transition to new state, log the change, reset PID and state timer."""
        if new_state == self.state:
            return
        self._log(f"STATE: {self.state.name} → {new_state.name} | "
                  f"laps={self.lap_count} sections={self.section_count}")
        self.prev_state  = self.state
        self.state       = new_state
        self.state_start_t = time.time()
        self.pid_wall.reset()
        self.pid_pillar.reset()

    def _state_elapsed(self) -> float:
        """Seconds elapsed since entering the current state."""
        return time.time() - self.state_start_t

    def _log(self, msg: str):
        print(f"[SM {time.strftime('%H:%M:%S')}] {msg}")
