"""
pid_controller.py — WRO 2026 Future Engineers — CHUISA ARCITEP
============================================================
Standard PID controller with anti-windup.
Used for steering correction (wall-following and pillar avoidance).

Tuning guide (in order):
  1. Set Ki=0, Kd=0. Increase Kp until vehicle oscillates noticeably.
  2. Reduce Kp by 50%.
  3. Increase Kd gradually to dampen oscillations (typically 0.05–0.3).
  4. Add small Ki (0.001–0.05) to eliminate persistent steady-state offset.
  5. Document final values and test results in Engineering Journal.
"""

import time


class PIDController:
    """
    PID controller with anti-windup and output clamping.

    Args:
        kp, ki, kd: PID gains
        output_min, output_max: Output range (typically -1.0 to 1.0 for steering)
    """

    def __init__(
        self,
        kp: float,
        ki: float,
        kd: float,
        output_min: float = -1.0,
        output_max: float = 1.0,
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.output_min = output_min
        self.output_max = output_max

        self._integral   = 0.0
        self._prev_error = 0.0
        self._prev_time  = time.time()

    def compute(self, error: float) -> float:
        """
        Compute PID output for the given error.

        Args:
            error: Difference between desired and actual value.
                   Positive error → output steers to reduce error.

        Returns:
            Control output clamped to [output_min, output_max].
        """
        now = time.time()
        dt  = now - self._prev_time
        dt  = max(dt, 1e-6)  # Avoid division by zero

        # Integral with anti-windup (clamp to prevent runaway)
        self._integral += error * dt
        integral_limit  = 100.0  # Tune if steady-state correction is too slow/fast
        self._integral  = max(-integral_limit, min(integral_limit, self._integral))

        # Derivative (rate of change of error)
        derivative = (error - self._prev_error) / dt

        output = (
            self.kp * error
            + self.ki * self._integral
            + self.kd * derivative
        )
        output = max(self.output_min, min(self.output_max, output))

        self._prev_error = error
        self._prev_time  = now
        return output

    def reset(self):
        """Reset internal state. Call when switching control modes."""
        self._integral   = 0.0
        self._prev_error = 0.0
        self._prev_time  = time.time()
