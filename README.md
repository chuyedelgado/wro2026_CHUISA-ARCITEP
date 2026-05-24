# WRO 2026 Future Engineers — CHUISA ARCITEP

**Season 2026 | Panama | Self-Driving Cars Challenge**

> ⚠️ **Note for national competition:** This README is written in English to comply with
> WRO international requirements (Rule 7). A Spanish summary is provided at the end.

---

## Team

| Role | Name | Age |
|------|------|-----|
| Team Leader / Electronics | Jesus Delgado | 20 |
| Software / Data | Maria I. Acosta | 21 |
| Coach | Carlos Delgado | — |

📸 [Team photos in `/t-photos`] · 🇵🇦 Panama

---

## Table of Contents

1. [Repository Structure](#repository-structure)
2. [Vehicle Overview](#vehicle-overview)
3. [Mobility & Mechanical Design](#1-mobility--mechanical-design)
4. [Power & Sensor Architecture](#2-power--sensor-architecture)
5. [Software Architecture & Obstacle Strategy](#3-software-architecture--obstacle-strategy)
6. [Engineering Decisions & Systemic Thinking](#4-engineering-decisions--systemic-thinking)
7. [Reproducibility — Build Your Own](#5-reproducibility--build-your-own)
8. [Videos](#videos)
9. [Vehicle Photos](#vehicle-photos)

---

## Repository Structure

This repository follows the official WRO Future Engineers template structure, extended
with additional documentation to support full reproducibility.

```
/
├── README.md                   ← You are here. Primary documentation (≥5000 chars).
├── src/
│   ├── raspberry_pi/           ← Python code for Raspberry Pi 5 (main controller)
│   │   ├── main.py             ← Entry point: starts threads, state machine
│   │   ├── vision.py           ← Camera capture + HSV color detection (OpenCV)
│   │   ├── state_machine.py    ← Finite state machine (INIT→DRIVE→PARK→STOP)
│   │   ├── pid_controller.py   ← PID controller for steering correction
│   │   ├── uart_comm.py        ← Serial communication with Arduino Nano
│   │   └── config.py           ← All tunable parameters (HSV ranges, PID gains, etc.)
│   └── arduino/
│       └── main/
│           └── main.ino        ← Arduino Nano: sensors, motor/servo PWM, UART
├── schemes/                    ← Electrical wiring diagrams and system architecture
├── models/                     ← STL/CAD files for 3D-printed mounting parts
├── v-photos/                   ← 6 vehicle photos (front, back, left, right, top, bottom)
├── t-photos/                   ← 2 team photos (official + fun)
├── video/
│   └── video.md                ← YouTube links for Open and Obstacle challenge demos
└── other/
    ├── decisions/              ← Detailed engineering decision logs with trade-off analysis
    └── tests/                  ← Test result logs and iteration data
```

---

## Vehicle Overview

Our vehicle is a 4-wheeled autonomous car using an Ackermann steering geometry.
The brain is a Raspberry Pi 5 (main computer vision and decision making) paired with
an Arduino Nano (low-level sensor reading and motor/servo control).

**Key specs:**
- Dimensions: [X] × [Y] × [Z] mm (within 300×200×300mm limit)
- Weight: [X] g (under 1500g limit)
- Drive: Rear-wheel drive with single DC motor + gear reduction
- Steering: Front Ackermann with servo motor
- Main controller: Raspberry Pi 5 (4GB) — Python 3.11 + OpenCV
- Secondary controller: Arduino Nano — C++ (sensors + actuators)
- Camera: Raspberry Pi Camera Module 3 Wide (120° FOV)
- Primary sensors: 2× VL53L1X Time-of-Flight, MPU-6050 IMU, rotary encoder
- Power: 2× LiPo 3S 11.1V 1500mAh (one for electronics, one for motor)

---

## 1. Mobility & Mechanical Design

### 1.1 Chassis Choice and Reasoning

We selected a [WLtoys 144001 / DESCRIBE YOUR ACTUAL CHASSIS] 1/14-scale RC car
as our base chassis because:

- **Ackermann geometry is pre-built and tested**: The front wheels turn at different
  angles (inner wheel turns more than outer), which is essential for smooth cornering
  without wheel scrubbing. Building this from scratch would require significant
  mechanical design time that is better invested in software.
- **Robust rear-wheel drive with DC gearbox motor**: The motor provides sufficient
  torque and already includes a gear reduction, avoiding the complexity of designing
  our own drivetrain.
- **Appropriate scale**: The 1/14 footprint allows us to stay within the 300×200mm
  rule while leaving room for all our electronics on top.

**Alternative considered and rejected:** We evaluated building a custom chassis using
Fusion 360 and our 3D printer. While this would allow tighter integration of components,
we determined that the mechanical risk was too high given our timeline. We documented
this decision in `other/decisions/chassis_selection.md`.

### 1.2 Steering System

The Ackermann steering mechanism uses a servo motor ([SERVO MODEL, e.g., MG996R or
DS3218]) connected to the front axle via a tie rod and steering links. Key parameters:

| Parameter | Value | Reasoning |
|-----------|-------|-----------|
| Max steering angle | ±[X]° | Set by servo throw and link geometry |
| Servo center position | [X] μs PWM | Calibrated to straight-ahead alignment |
| Servo resolution | ~0.1° | Fine enough for smooth PID control |

### 1.3 Drive System

The rear wheels are driven by a single DC motor with a built-in planetary gearbox.

| Parameter | Value | Reasoning |
|-----------|-------|-----------|
| Motor voltage | [X]V nominal | Matches 3S LiPo output via motor driver |
| Gear ratio | [X]:1 | Provides balance of speed and torque |
| Max speed (measured) | ~[X] m/s | Sufficient for 3-min runs with stability margin |

**Speed decision:** We tested three speed levels during development: 0.3, 0.45, and
0.6 (relative to max PWM). At 0.6, the vehicle had difficulty stopping smoothly at
the start section. At 0.3, we failed to complete 3 laps in the 3-minute time limit
in some runs. We selected **0.45** as the operating speed because it completed laps
reliably (~[X] seconds for 3 laps) with a [X]% success rate on stopping in the
start section across [N] test runs.

### 1.4 Custom 3D-Printed Components

All STL files are in `/models`. Key parts designed in Fusion 360:

| Part | Purpose | Material | Print settings |
|------|---------|---------|----------------|
| `camera_mount.stl` | Mounts camera at 175mm height, 14° downward angle | PLA | 30% infill |
| `pi_mount.stl` | Secures Raspberry Pi 5 above chassis with vibration dampening | PETG | 40% infill |
| `sensor_bracket.stl` | Holds 2× ToF sensors at front-left and front-right positions | PLA | 30% infill |
| `arduino_tray.stl` | Arduino Nano + TB6612FNG on a single removable tray | PLA | 30% infill |

**Camera height and angle optimization:** We tested camera at 100mm, 175mm, and
250mm height. At 100mm, external elements (audience, equipment) appeared above the
walls and confused color detection. At 250mm, pillars were too close to the top of
the frame when the vehicle was within 30cm, causing missed detections near turns.
**175mm at 14° downward** was optimal — the top of the outer wall is at ~50% of the
frame height, keeping all game elements visible without interference from outside.

### 1.5 Mechanical Iterations

| Version | Change | Reason | Result |
|---------|--------|--------|--------|
| V1.0 | Direct servo attachment to tie rod | Simplest setup | Too much play, unstable at speed |
| V1.1 | Added servo horn with longer arm | Reduce play in linkage | Improved stability |
| V2.0 | Custom sensor bracket replaced tape mounting | Tape vibrated at speed, sensors drifted | Consistent ToF readings |
| V2.1 | Added foam vibration dampeners under Pi mount | Pi occasionally rebooted at high speed | No more reboots |

---

## 2. Power & Sensor Architecture

### 2.1 Power Distribution

We use two separate LiPo 3S batteries to isolate motor noise from the logic circuits.
Motor current draw during acceleration can reach ~3.5A, causing voltage dips that
can crash the Raspberry Pi if they share a source.

```
Battery A (3S 11.1V, 1500mAh)          Battery B (3S 11.1V, 1500mAh)
         │                                        │
    [Switch A]                              [Switch B]
         │                                        │
    [Fuse 3A]                               [Fuse 5A]
         │                                        │
  [Buck 5V/3A]            [TB6612FNG]      [Buck 5V/3A]
    │       │              Motor              │       │
  [Pi 5] [Servo]          DC driver        [Arduino] [2×ToF]
                                           [MPU-6050]
```

**Power budget (measured at full load):**

| Component | Voltage | Current (avg) | Current (peak) |
|-----------|---------|---------------|----------------|
| Raspberry Pi 5 | 5V | 1.2A | 2.5A |
| Camera Module 3 | 3.3V (via Pi) | 0.15A | 0.25A |
| Servo MG996R | 5–6V | 0.5A | 1.5A |
| Arduino Nano | 5V | 0.05A | 0.1A |
| 2× VL53L1X | 3.3V (via Arduino) | 0.02A | 0.04A |
| MPU-6050 | 3.3V (via Arduino) | 0.004A | 0.004A |
| DC Motor | 7.4–11.1V | 1.2A | 3.5A |

Battery A (electronics) must supply up to **~4.5A peak** — our 3A buck converter
is not sufficient for this peak. We added a **capacitor bank (3× 1000μF 25V)** across
the 5V rail to handle transient peaks without triggering Pi undervoltage protection.
This was identified during testing when the Pi showed the lightning bolt icon during
rapid acceleration.

### 2.2 Sensor Selection and Placement

**VL53L1X Time-of-Flight (×2):**
- Technology: 940nm VCSEL laser, I2C interface
- Range: 40mm–4000mm (short mode used: 40–1300mm, better accuracy)
- Placement: Front-left corner and front-right corner at 45° angle
- Purpose: Primary wall distance measurement for PID lane-centering
- **Why ToF over ultrasonic:** ToF gives ~±[X]mm accuracy vs ~±30mm for HC-SR04.
  Tested HC-SR04 first — at vehicle speed of 0.45 m/s, the 30mm error caused
  oscillations. Switched to VL53L1X and stability improved significantly.

**MPU-6050 IMU:**
- Data: 3-axis gyroscope (primary: Z-axis yaw rate) + 3-axis accelerometer
- Used for: Counting 90° turns (section transitions), heading correction
- Calibration: 100-sample gyro bias measurement at startup (vehicle must be still)
- Drift: ~[X]°/min — acceptable for 3-minute runs without resets

**Rotary Encoder:**
- Type: [DESCRIBE: hall effect / optical / etc.]
- Resolution: [X] pulses per revolution
- Purpose: Distance measurement, speed control, parking position estimation

**Camera Module 3 Wide:**
- Resolution used: 320×240 at 30fps
- Color space: HSV (not RGB) — robust to lighting changes
- FOV: 120° horizontal (wide angle) — critical for detecting pillars early

**Why no ultrasonic on sides:** After V2.0 testing, ToF sensors placed at 45° at
the front provide sufficient wall distance data for the PID when combined with
the IMU for heading. Adding lateral ultrasonics would have required redesigning
the sensor bracket and adding more Arduino pins. The V2.0 solution provided
[X]% run success rate which met our target.

### 2.3 Wiring Diagram

See `/schemes/wiring_diagram.png` for the full electromechanical diagram.
See `/schemes/system_architecture.png` for the software-hardware connection overview.

---

## 3. Software Architecture & Obstacle Strategy

### 3.1 Module Overview

All source code is in `/src`. The system uses two controllers:

**Raspberry Pi 5 (Python 3.11)** — `src/raspberry_pi/`

| Module | Responsibility |
|--------|---------------|
| `main.py` | Entry point: initializes all subsystems, waits for start signal |
| `vision.py` | Camera capture thread + HSV color detection pipeline |
| `state_machine.py` | Finite state machine driving all decisions |
| `pid_controller.py` | Generic PID for steering, reusable with any error signal |
| `uart_comm.py` | Serial protocol with Arduino (commands out, sensor data in) |
| `config.py` | All tunable constants: HSV thresholds, PID gains, speeds |

**Arduino Nano (C++)** — `src/arduino/main/main.ino`

Handles: Start button detection, servo PWM, motor PWM via TB6612FNG, I2C sensor
reading (2× ToF + IMU), encoder interrupts, UART communication with Pi.

### 3.2 Communication Protocol (Pi ↔ Arduino)

UART at **115,200 baud**.

```
Pi → Arduino (command):   "S<steering>,<speed>\n"
  steering: -100 (full left) to +100 (full right), 0 = center
  speed:    -100 (full reverse) to +100 (full forward), 0 = stop

Arduino → Pi (sensors):   "T<tof_l>,<tof_f>,<tof_r>,<yaw>,<enc>\n"
  tof_l/f/r: distances in mm
  yaw:        heading in degrees (float, integrated from gyro)
  enc:        total encoder pulses since start
```

Frequency: Arduino sends sensor data at ~50Hz. Pi sends commands at ~50Hz
(once per control loop iteration). Commands not received within [X]ms → Arduino
defaults to stop for safety.

### 3.3 Computer Vision Pipeline

For each frame (320×240, 30fps):

```
1. Capture RGB frame (Pi Camera via picamera2)
2. Convert to HSV color space (cv2.cvtColor)
3. Crop Region of Interest (ROI): rows 60–200 (exclude background above walls)
4. Apply Gaussian blur 5×5 (reduce noise, smooth color gradients)
5. Threshold for each target color → binary masks
6. Morphological closing on pillar masks (fill small holes)
7. Find contours → select largest by area → compute centroid (image moment M00)
8. Return Detection dataclass to state machine
```

**Why HSV instead of RGB:** Under different lighting conditions (competition venue
vs training), RGB values of the same physical color can shift dramatically. The Hue
component in HSV encodes "what color" while Saturation and Value handle brightness
changes. This made our thresholds transferable between our training environment
and the competition venue with only minor adjustments.

**HSV calibration procedure:** We wrote a calibration script (`other/calibration.py`)
that displays a trackbar interface for live HSV range adjustment. We use this tool at
the start of each competition day to fine-tune thresholds for the actual venue lighting.

### 3.4 Finite State Machine

```
INIT
 │
 ▼
DETECT_DIR ──(orange/blue line detected)──▶ OPEN_DRIVE or OBS_DRIVE
                                                     │
                                            (section count via IMU turns)
                                                     │
                                            (3 laps complete)
                                                     │
                                     ┌───────────────┴─────────────────┐
                               OPEN_DRIVE                         OBS_DRIVE
                                  │                                    │
                               STOP                            FIND_PARKING
                                                                       │
                                                                   PARKING
                                                                       │
                                                                    STOP
```

**State: DETECT_DIR** — Reads first wall line color from camera.
Orange line on right side → Clockwise (CW). Blue line on right → Counter-clockwise (CCW).
This determines the direction for all subsequent lap counting.

**State: OPEN_DRIVE** — PID wall-centering using ToF left/right distances.
Error = dist_left − dist_right. Positive error → too close to left → steer right.
Sections counted via 90° yaw changes detected by IMU. After 24 sections (3 laps),
transition to STOP.

**State: OBS_DRIVE** — Same as OPEN_DRIVE but with pillar avoidance overlay.
Red pillar detected → shift target position to the left of frame center by RED_OFFSET
pixels (so vehicle passes pillar on its right). Green pillar → shift right (vehicle
passes on its left). Priority: pillar avoidance > wall centering.

**State: FIND_PARKING** — After 3 laps, reduce speed and scan for magenta markers.
Approach section of interest as defined by direction and lap count.

**State: PARKING** — Parallel park sequence:
1. Detect both left and right magenta markers
2. Align vehicle with parking lot centerline
3. Drive past the right marker, then reverse into space
4. Straighten using IMU heading
5. Stop when fully inside (both markers visible on correct sides)


## 4. Engineering Decisions & Systemic Thinking

### 4.1 System Constraints

| Constraint | Impact on Design |
|------------|-----------------|
| Vehicle size ≤ 300×200×300mm | Limited the Pi + Arduino + battery arrangement to a stacked layout |
| Weight ≤ 1500g | Eliminated option of additional heavy sensors or second camera |
| Single start button (Rule 9.11) | All configuration must be in config.py, no runtime inputs |
| No wireless during run (Rule 11.10) | Pi's onboard WiFi disabled in /boot/config.txt |
| 3-minute round limit | Drives base speed choice (0.45 = ~[X]s for 3 laps + margin) |
| No sensor calibration during competition | HSV thresholds must be robust enough to adapt to venue lighting |

### 4.2 Key Trade-offs

| Decision | Option A (chosen) | Option B (rejected) | Why A |
|----------|------------------|---------------------|-------|
| SBC selection | Raspberry Pi 5 (4GB) | Jetson Nano | Pi 5 is faster for OpenCV, better camera API, lower cost, more community support |
| Chassis | Modified RC car | Custom 3D-printed chassis | RC base is mechanically proven; saves 2–3 weeks of mechanical iteration |
| Color detection | HSV thresholding | ML object detection (YOLO) | HSV is faster (30fps vs ~10fps on Pi for YOLO), more predictable, easier to debug |
| Sensor for walls | ToF VL53L1X | Camera-based wall detection | ToF is accurate and fast; camera-only wall detection failed in testing when wall shadows confused detection |
| Controller split | Pi + Arduino | Pi only | Arduino handles time-critical interrupts (encoder, button) at microsecond precision that Python cannot guarantee |

### 4.3 Identified Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Pi crashes on bump | Medium | High (DNF) | Vibration dampeners, capacitor bank on 5V rail, tested over 50 runs |
| Wrong pillar color detected | Low | High (penalty) | Calibration script, tested under 3 different lighting conditions |
| Parking fails (touches magenta marker) | Medium | Medium | Slow approach speed, tested in [N] runs with [X]% success rate |
| Battery dies mid-run | Low | High (DNF) | Two fresh batteries before each round, voltage monitoring in code |
| Component failure (servo) | Low | High (DNF) | Backup servo in kit bag, can replace in <5min |

### 4.4 Version History

| Version | Date | Changes | Outcome |
|---------|------|---------|---------|
| v0.1 | [DATE] | Initial commit: repo structure + code skeleton | Foundation established |
| v0.2 | [DATE] | Basic movement + camera detection | Vehicle drives + sees colors |
| v0.3 | [DATE] | Open Challenge working | 3 laps completed in [X]% of attempts |
| v1.0 | [DATE] | Full Obstacle Challenge + parking | [X]% success rate target achieved |

---

## 5. Reproducibility — Build Your Own

### 5.1 Bill of Materials (BOM)

| Component | Model | Qty | Approx. Cost | Source |
|-----------|-------|-----|--------------|--------|
| Chassis base | WLtoys 144001 (no battery) | 1 | $55 | Amazon |
| Main controller | Raspberry Pi 5 (4GB) | 1 | $70 | raspberrypi.com |
| Camera | Raspberry Pi Camera Module 3 Wide | 1 | $35 | raspberrypi.com |
| MicroSD | SanDisk 32GB Class 10 | 1 | $10 | Amazon |
| Microcontroller | Arduino Nano Every | 1 | $12 | Arduino Store |
| ToF sensor | VL53L1X breakout (SparkFun) | 2 | $28 | SparkFun |
| IMU | MPU-6050 breakout | 1 | $6 | Amazon |
| Motor driver | TB6612FNG breakout | 1 | $8 | SparkFun |
| Battery | LiPo 3S 11.1V 1500mAh XT60 | 2 | $36 | HobbyKing |
| Charger | IMAX B6 (or SkyRC S60) | 1 | $30 | Amazon |
| Buck converter | 5V/3A step-down module | 2 | $12 | Amazon |
| Servo (if needed) | MG996R | 1 | $12 | Amazon |
| Cables + connectors | Dupont M/F, XT60, JST | 1 set | $18 | Amazon |
| Fasteners | M2/M3 screw kit | 1 | $10 | Amazon |
| PCB perforated | 5×7cm perfboard | 2 | $5 | Amazon |
| 3D printing | PLA filament ~150g | — | $5 | On-hand |

**Total: ~$352**

### 5.2 Assembly Overview

Detailed assembly is documented in `/other/assembly_guide.md`. Summary:

1. Mount Pi 5 on `pi_mount.stl` over chassis center of gravity
2. Mount Arduino tray below Pi (wired to Pi via USB-A to Mini-USB)
3. Mount camera on `camera_mount.stl` at front, 175mm height, 14° down
4. Mount ToF sensors on `sensor_bracket.stl` at front-left and front-right (45°)
5. Mount IMU on Arduino tray (away from motor wires to minimize EMI)
6. Wire motor: Battery B → Fuse → TB6612FNG → DC motor
7. Wire logic: Battery A → Buck 5V/3A → Pi; Pi GPIO → Arduino → sensors
8. Secure all wiring with cable ties; keep motor wires away from I2C lines

### 5.3 Software Reproducibility Checklist

- [ ] Flash Raspberry Pi OS 64-bit Bookworm to MicroSD
- [ ] Enable I2C: `sudo raspi-config` → Interfaces → I2C → Enable
- [ ] Install Python dependencies: `pip3 install picamera2 pyserial numpy opencv-python`
- [ ] Find Arduino port: `ls /dev/tty*` with and without Arduino connected
- [ ] Update `config.py` → `ARDUINO_PORT` with the correct port (e.g., `/dev/ttyUSB0`)
- [ ] Run calibration script to set HSV thresholds for your lighting
- [ ] Upload Arduino sketch, verify serial output in Arduino IDE Serial Monitor
- [ ] Test UART: run `python3 -c "from uart_comm import ArduinoComm; c=ArduinoComm(); print(c.get_sensors())"`
- [ ] Run `main.py`, press start button on vehicle, verify autonomous movement

---

## Videos

See [`video/video.md`](video/video.md) for YouTube links.

- **Open Challenge demo:** [LINK PENDING — will be added before competition]
- **Obstacle Challenge demo:** [LINK PENDING — will be added before competition]

> Videos will be added by [TARGET DATE]. Each shows the vehicle completing 3 full laps
> autonomously. The autonomous driving segment is >30 seconds as required by Rule 7.

---

## Vehicle Photos

Photos are in `/v-photos`. Six views required:

| View | File |
|------|------|
| Front | `v-photos/front.jpg` |
| Back | `v-photos/back.jpg` |
| Left side | `v-photos/left.jpg` |
| Right side | `v-photos/right.jpg` |
| Top | `v-photos/top.jpg` |
| Bottom | `v-photos/bottom.jpg` |

> Photos will be added once the vehicle is physically assembled (target: [DATE]).

---

## Resumen en Español

Este vehículo autónomo fue diseñado por el equipo **CHUISA ARCITEP]** de Panamá
para la competencia WRO 2026 categoría Futuros Ingenieros. El vehículo usa una
Raspberry Pi 5 para visión por computadora (OpenCV, espacio de color HSV) y un
Arduino Nano para el control de motores y sensores. El chasis es un carro RC 1/14
modificado con piezas impresas en 3D. La lógica de conducción es una máquina de
estados finitos con control PID para centrado de carril y evasión de pilares por
detección de color.

Para más información, contactar a Jesus Delgado — chuye5610@gmail.com.

---

*WRO® and World Robot Olympiad™ are trademarks of the World Robot Olympiad Association Ltd.*
*Repository created: 05/23/2026. Last updated: 05/23/2026. Public since: 05/23/2026.*
