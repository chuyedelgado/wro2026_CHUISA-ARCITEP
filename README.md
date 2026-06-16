# WRO 2026 Future Engineers — Team CHUISA ARCITEP

Autonomous self-driving car for the **WRO 2026 Future Engineers** category.
Regional: **Panama — July 16, 2026**.

> Working document. This README reflects the engineering work of the student team and is
> updated continuously. Sections marked **[pending]** depend on hardware still in transit
> (chassis, batteries, encoders) or on tests that require the assembled robot; they will be
> completed before the documentation freeze. **No fabricated data is included** — every figure
> comes from a real measurement, and what has not been measured is explicitly marked.
>
> _Language note: per WRO rule 7 this README is written in English; to be confirmed with WRO
> Panama whether Spanish is acceptable for the regional._

---

## 1. The Team

**Team CHUISA ARCITEP**, representing the **Academia de Robótica CITEP (ARCITEP)**, Panama.

| Member | Age | Role |
|---|---|---|
| Jesús Delgado | 20 | Hardware & Electronics Lead — power architecture, wiring, sensor integration, mechanical assembly |
| María I. Acosta | 21 | Software & Data Lead — computer vision, control logic / FSM, documentation |
| Carlos Delgado | 21 | Coach — organizational support |

Per WRO rule 3.3, **all construction and programming is performed by the students**; the coach
provides organizational support only and does not build or program. The students can explain every
design decision and implementation detail, as judges may interview the team (rules 3.8–3.9).

---

## 2. The Challenge

The Future Engineers self-driving car must complete two challenges autonomously on a 3×3 m track
bounded by 100 mm black walls:

- **Open Challenge:** 3 laps following the corridor (width 600 or 1000 mm per section, randomized)
  without touching the outer wall, then stop in the start section.
- **Obstacle Challenge:** 3 laps (corridor always 1000 mm) reacting to traffic signs —
  **a RED pillar is passed on its RIGHT, a GREEN pillar on its LEFT** — without displacing them,
  plus a parallel-parking maneuver between two magenta delimiters.

Driving direction (CW/CCW) is decided by the first colored line crossed (orange/blue) and is
**not** provided as data — the robot must infer it (rules 9.8–9.9).

---

## 3. Hardware Overview

| Subsystem | Component | Notes |
|---|---|---|
| Compute (brain) | Raspberry Pi 5 (4 GB) | Vision + high-level FSM + decisions |
| Real-time control | Arduino Nano Every (ATmega4809, 5 V) | PWM, encoder ISR, sensor I2C, failsafe |
| Camera | SainSmart Camera Module 3 (Sony IMX708, 152° FOV) | Classical HSV vision |
| Distance | 2× VL53L1X ToF (Pololu lib) | Wall distance for PID; I2C |
| Orientation | MPU-6050 IMU | Yaw for 90° turns and lap counting |
| Chassis | WLtoys A959-B 1/18 (≈250×180×90 mm) | Factory Ackermann steering **[pending arrival]** |
| Traction motor | JGB37-520, 12 V, 530 RPM, Hall encoder | Single driven axle **[encoder pending]** |
| Steering servo | Power HD LF-20MG (~20 kg·cm) | Ackermann actuator |
| Power | 2× LiPo 3S 1500 mAh (isolated) | Logic battery + motor battery **[pending arrival]** |
| Regulation | Mini560 fixed 5 V (Pi) · UBEC 5/6 V (servo) | Separate rails |
| Motor driver | Cytron MD10C | PWM + DIR |
| Protection | PolySwitch RXEF300 (logic) · glass fuse (motor) · DPST switch | Single switch cuts both batteries (rule 9.10) |

---

## 4. Mobility & Mechanical Design

**Chassis decision — modified RC car vs. custom build.** We chose to modify a **WLtoys A959-B**
(1/18) rather than design an Ackermann chassis from scratch. Rationale: a proven factory steering
geometry removes mechanical risk and the CAD learning curve within a 5-week timeline. The A959-B
(~180 mm wide) fits the 200 mm width limit with margin; the larger 144001 (1/14) does not.

**Drivetrain.** Single driven axle + one steering actuator (rules 11.3/11.5). The factory 4WD/ESC/
RX and body are removed; our own electronics, the JGB37-520 motor and the LF-20MG servo are installed.

**Speed budget.** With a 65 mm wheel and 530 RPM: theoretical top speed ≈ 530 × π × 0.065 / 60 ≈
**1.8 m/s** — ample for the track with controllable margin. The Hall encoder enables closed-loop
speed control and odometry (finish-line stop and parking).

**[pending]** measured top speed (free-run and on track); final weight (≤1500 g target); final
dimensions with camera mounted; mechanical iteration table — all require the assembled robot.

---

## 5. Power System

**Dual isolated-battery architecture.** Battery A powers the logic (Pi + servo), Battery B powers
the motor. Isolating the motor rail eliminates Pi brownouts caused by motor current spikes **without
a capacitor bank** — a simpler, more robust design.

**Pi regulator — Mini560 fixed 5 V (not adjustable).** An adjustable buck's potentiometer can drift
under vibration and over-volt the Pi. A fixed 5 V/5 A converter is the safe choice.
Validation criterion: ≥4.9 V under full Pi load **[pending: measure under load]**.

**Servo regulator — separate UBEC.** The Pi needs exactly 5 V; the servo performs better at 6 V, so
a shared rail creates a voltage conflict. The UBEC is set to 5 V for bench tests; its output is
**measured with a multimeter before connecting the servo**.

**Protection & switching.** PolySwitch RXEF300 (auto-resetting) on the logic rail; fast glass fuse on
the motor rail; a single DPST DC-rated switch cuts both batteries with one action (rule 9.10).

**[pending]** measured currents: Pi (avg/peak), servo (avg/stall @6 V), motor (run/stall) → glass-fuse
rating; wiring diagram in `schemes/`.

---

## 6. Sensors & Vision

**Camera + lens calibration (data-driven).** The 152° lens distorts strongly. The standard pinhole
calibration gave a reprojection error of **2.39 px** with residual edge curvature; switching to the
**fisheye model** reduced it to **0.61 px**. We use the fisheye calibration
(`config/camera_calibration_fisheye.npz`). This is documented as an engineering decision: the lens
exceeds the pinhole model.

**Classical HSV vision — chosen over ML.** The track is the best case for classical CV: colors are
specified in the rules (RGB exact), objects are solid geometric shapes, background is controlled.
HSV gives stable 30 fps, is debuggable (the mask is visible and tunable in seconds — essential for
in-pit recalibration), and avoids the cost/opacity of training a model. An AI camera (Sony IMX500)
is a documented **post-regional** line of work only (see `other/decisions/`).

- Green: single Hue range (H 35–85, S 70–255, V 50–255, bench lighting).
- Red: **dual** range (Hue wraps near 0 and near 179).
- Robustness plan: robust mode (widened S/V), light matrix testing, and **in-situ recalibration during
  practice** (legal per rule 9.9). See `docs/` calibration methodology.

**ToF distance sensors (2× VL53L1X).** Both share factory address 0x29, so we use the **XSHUT
re-addressing** technique: power both off, bring up sensor #1 and reassign it to **0x2A**, then bring
up sensor #2 (stays **0x29**). Measured accuracy: **±3 mm at 100 mm** (criterion ±5 mm — met).
Minimum measurable distance ~20 mm (a sensor characteristic, irrelevant since the wall-following
setpoint is ~250–300 mm). **[pending]** accuracy check at 250 mm and 500 mm.

**IMU (MPU-6050, 0x68).** Yaw for 90° turns and lap counting (12 corners = 3 laps). Bias calibrated at
rest on startup. Measured gyro drift: **~0.5° per minute** — negligible versus turn magnitudes and
lap durations.

**Thermal.** Pi 5 with Active Cooler reached **~59.6 °C** under a 5-minute CPU stress test (criterion
<60 °C). **[pending]** re-measure under vision load.

---

## 7. Software & Obstacle Strategy

**Two-controller architecture.** The Pi handles vision and high-level strategy; the Arduino guarantees
microsecond timing (encoder ISR, stable PWM, failsafe) that Python cannot. The Pi sends *intentions*;
the Arduino executes them with its own safety logic.

**High-level FSM (Pi):**
`INIT → WAIT_BUTTON → DETECT_DIR → DRIVE(open|obstacle) ⇄ TURN_90 → LAP_COUNT → (3 laps) → STOP/PARK`,
with transversal `ESTOP` (failsafe) and `RECOVERY` (wrong-side-of-pillar correction). **[pending: FSM
diagram in `schemes/`.]**

**Vision pipeline (320×240 @30 fps):** capture → fisheye undistort → BGR→HSV → ROI → color masks
(red dual-range, green, orange, blue, magenta) → erode/dilate → contour filtering → centroid + bbox.

**UART protocol (Pi ↔ Arduino), implemented and verified:**
- Pi → Arduino: `S<steer>,<speed>*<checksum>`
- Arduino → Pi telemetry: `T<tof_left>,<tof_right>,<yaw>*<checksum>` _(full spec adds front ToF and
  encoder once integrated)_
- XOR checksum (corrupt messages discarded); **failsafe** stops the motor and centers steering if no
  valid command arrives within 500 ms. Verified: **10 minutes of traffic with zero checksum errors**.
- Voltage safety: the Arduino TX (5 V) reaches the Pi RX through a 1 kΩ/2.2 kΩ divider; **measured
  3.294 V** (safe for the 3.3 V Pi) before powering the Pi.

**Pillar handling (Obstacle):** HSV detection + inter-frame tracking + distance by apparent size →
dynamic setpoint offset. **RED → pass on the RIGHT; GREEN → pass on the LEFT.** A unit test
(`test_pillar_sides.py`) guards this rule. **[pending: PID wall-following tuning table and test
metrics, once the robot drives.]**

---

## 8. Systems Thinking — Key Decisions ("X not Y because…")

| Decision | Chosen | Alternative | Why (data-driven) |
|---|---|---|---|
| Platform | A959-B + 3D parts | Custom Ackermann | Mechanical risk & CAD curve vs. 5 weeks |
| Compute | Pi 5 + Nano Every | Pi only | Hard real-time timing on the MCU |
| Vision | Classical HSV | ML / AI camera | 30 fps, debuggable, colors are normed; IMX500 also cuts FOV 152°→76° |
| Lens model | Fisheye | Pinhole | 0.61 px vs 2.39 px reprojection (measured) |
| Power | Dual isolated battery | Single + cap bank | Isolates motor spikes; simpler |
| Pi BEC | Fixed 5 V Mini560 | Adjustable buck | Pot drift under vibration risks the Pi |
| Level shift | Resistor divider | Level-shifter module | Sufficient & available; shifter is a future refinement |

**Risks & mitigations:** logistics of late hardware (chassis/batteries) → Phase 1-A bench work done
first; lighting vs. HSV → robust mode + in-situ recalibration; parking tight margin (robot ~180 mm in
200 mm bay) → decision point on full vs. partial parking; wrong pillar side → unit test.

---

## 9. Code Structure

```
src/raspberry_pi/   main.py · vision.py · state_machine.py · pid_controller.py
                    uart_comm.py · config.py   (ALL constants live here)
src/arduino/        sensor reading, PWM, encoder ISR, low-level FSM, UART, watchdog
other/              calibration & test tools (HSV calibrator, I2C scanner, camera calibration)
other/decisions/    engineering decision records
docs/journal/       dated engineering log
config/             camera_calibration_fisheye.npz
```
Convention: **no magic constants outside `config.py`**; each constant documented with how/when it was
measured.

---

## 10. How to Build, Compile & Run

**Raspberry Pi (vision + strategy):**
1. Flash Raspberry Pi OS Bookworm (64-bit); enable I2C and the serial port (`raspi-config`).
2. Third-party camera: add `dtoverlay=imx708` to `/boot/firmware/config.txt`; verify with
   `rpicam-hello --list-cameras`.
3. Install: `sudo apt install -y python3-opencv python3-picamera2` and `pip3 install pyserial --break-system-packages`.
4. Run: `python3 src/raspberry_pi/main.py`.

**Arduino (real-time control):**
1. Arduino IDE + "Arduino megaAVR Boards"; board: Arduino Nano Every.
2. Libraries: `VL53L1X` (Pololu), `MPU6050_light` (rfetick).
3. Upload `src/arduino/main/main.ino`.

---

## 11. Reproducibility & GitHub

- Public repository, maintained ≥12 months post-competition.
- Folder structure follows the official WRO-FE template.
- Daily commits with meaningful messages (`feat:`, `fix:`, `docs:`, `test:`); release tag
  `v1.0-regional` at the documentation freeze.
- Zero fabricated data: every figure traces to a dated measurement; pending items are explicitly marked.

---

## 12. Current Status (verified vs. pending)

| Item | Status |
|---|---|
| Pi 5 OS, headless SSH, thermal (~59.6 °C) | ✅ verified |
| Camera + fisheye calibration (0.61 px) | ✅ verified |
| HSV detection (green + red) | ✅ verified |
| 3 sensors on one I2C bus (2 ToF + IMU) | ✅ verified |
| ToF ±3 mm @100 mm · gyro drift ~0.5°/min | ✅ measured |
| UART protocol (checksum + failsafe, 10 min no error) | ✅ verified |
| Arduino → Pi telemetry (2 ToF + yaw) | ✅ verified |
| Steering servo characterization | ⏳ pending (battery → UBEC) |
| Chassis assembly, motor + encoder integration | ⏳ pending (hardware in transit) |
| PID tuning table, FSM diagram, success metrics | ⏳ pending (requires driving robot) |
| Vehicle & team photos, challenge videos, CAD/STL | ⏳ pending (requires assembled robot) |

