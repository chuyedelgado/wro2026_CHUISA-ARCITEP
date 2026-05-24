/**
 * main.ino — WRO 2026 Future Engineers — CHUISA ARCITEP
 * ====================================================
 * Arduino Nano: Low-level controller.
 *
 * Responsibilities:
 *   1. Handle start button (Rule 9.11): wait in standby, signal Pi when pressed
 *   2. Read sensors: 2× VL53L1X Time-of-Flight (I2C), MPU-6050 IMU (I2C)
 *   3. Count encoder pulses (interrupt-driven)
 *   4. Control DC motor via TB6612FNG (PWM + direction pins)
 *   5. Control steering servo (PWM)
 *   6. Send sensor data to Raspberry Pi via UART at ~50Hz
 *   7. Receive steering/speed commands from Pi via UART
 *
 * Communication Protocol (UART 115200 baud):
 *   Receive:  "S<steering>,<speed>\n"
 *             steering: -100 (full left) to +100 (full right)
 *             speed:    -100 (full reverse) to +100 (full forward)
 *   Send:     "T<tof_l>,<tof_f>,<tof_r>,<yaw>,<enc>\n"
 *             "READY\n"  — setup complete
 *             "START\n"  — start button pressed
 *
 * Competition rules enforced:
 *   Rule 9.10: ONE power switch (hardware, not this code)
 *   Rule 9.11: ONE start button, vehicle waits in standby
 *   Rule 11.10: No wireless — WiFi/BT not used (Nano has none)
 *
 * Libraries required (install via Arduino Library Manager):
 *   - "SparkFun VL53L1X" by SparkFun Electronics
 *   - "MPU6050" by Electronic Cats (or Jeff Rowberg's i2cdevlib)
 *   - "Servo" (built-in)
 */

#include <Wire.h>
#include <Servo.h>
#include <SparkFun_VL53L1X.h>
#include <MPU6050.h>

// ── Pin Definitions ──────────────────────────────────────────────────────────
// Start button — Rule 9.11: the ONE permitted start button
const uint8_t PIN_START_BTN   = 2;   // INT0 — interrupt-capable

// Steering servo
const uint8_t PIN_SERVO        = 9;

// TB6612FNG motor driver
const uint8_t PIN_MOTOR_IN1    = 5;   // Direction A
const uint8_t PIN_MOTOR_IN2    = 6;   // Direction B
const uint8_t PIN_MOTOR_PWM    = 3;   // Speed (PWM)
const uint8_t PIN_STBY         = 4;   // Standby (active HIGH = enabled)

// Encoder (channel A on interrupt pin)
const uint8_t PIN_ENCODER_A    = 7;   // INT1 alternative — use PCINT if needed

// VL53L1X XSHUT pins (used to assign unique I2C addresses at boot)
const uint8_t PIN_TOF_XSHUT_L  = 10;
const uint8_t PIN_TOF_XSHUT_F  = 11;
// Right ToF: always-on, uses default address 0x29

// ── Constants ────────────────────────────────────────────────────────────────
const int SERVO_CENTER_US = 1500;     // Pulse width for straight-ahead (microseconds)
const int SERVO_MAX_US    = 1900;     // Max right turn
const int SERVO_MIN_US    = 1100;     // Max left turn
const int MOTOR_MAX_PWM   = 200;      // Max PWM (out of 255) — limit top speed
const int SEND_INTERVAL_MS = 20;      // Send sensor data every 20ms (~50Hz)

// VL53L1X I2C addresses (must be unique)
const uint8_t TOF_ADDR_RIGHT = 0x29;  // Default address (always-on)
const uint8_t TOF_ADDR_LEFT  = 0x30;  // Reassigned at startup
const uint8_t TOF_ADDR_FRONT = 0x31;  // Reassigned at startup

// ── Objects ───────────────────────────────────────────────────────────────────
Servo         steeringServo;
SFEVL53L1X    tofLeft,  tofFront, tofRight;
MPU6050       imu;

// ── Volatile State ────────────────────────────────────────────────────────────
volatile long     encoderPulses = 0;
volatile bool     startPressed  = false;

// ── Regular State ─────────────────────────────────────────────────────────────
int   cmdSteering     = 0;    // -100 to +100, from Pi
int   cmdSpeed        = 0;    // -100 to +100, from Pi
int   distLeft        = 9999;
int   distFront       = 9999;
int   distRight       = 9999;
float yawDegrees      = 0.0f;
float gyroZBias       = 0.0f;
unsigned long lastIMUMicros  = 0;
unsigned long lastSendMillis = 0;


// ── Setup ────────────────────────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);
  Wire.begin();
  Wire.setClock(400000UL);  // 400kHz I2C

  // Pin modes
  pinMode(PIN_START_BTN,  INPUT_PULLUP);
  pinMode(PIN_MOTOR_IN1,  OUTPUT);
  pinMode(PIN_MOTOR_IN2,  OUTPUT);
  pinMode(PIN_MOTOR_PWM,  OUTPUT);
  pinMode(PIN_STBY,       OUTPUT);
  pinMode(PIN_TOF_XSHUT_L, OUTPUT);
  pinMode(PIN_TOF_XSHUT_F, OUTPUT);

  // Motor driver: standby mode until start
  digitalWrite(PIN_STBY, LOW);
  analogWrite(PIN_MOTOR_PWM, 0);

  // Steering servo: center position
  steeringServo.attach(PIN_SERVO);
  steeringServo.writeMicroseconds(SERVO_CENTER_US);

  // Initialize ToF sensors with unique I2C addresses
  setupToFSensors();

  // Initialize IMU and calibrate gyro bias
  setupIMU();

  // Encoder interrupt
  attachInterrupt(digitalPinToInterrupt(PIN_ENCODER_A), onEncoderPulse, RISING);

  // Start button interrupt
  attachInterrupt(digitalPinToInterrupt(PIN_START_BTN), onStartButton, FALLING);

  Serial.println("READY");

  // ── STANDBY: Wait for start button (Rule 9.11) ────────────────────────────
  // Vehicle is in standby state. No movement. Servo at center. Motor stopped.
  while (!startPressed) {
    delay(10);  // Low-power wait
  }

  // Arm motor driver
  digitalWrite(PIN_STBY, HIGH);
  Serial.println("START");   // Signal Pi that we are starting

  lastIMUMicros  = micros();
  lastSendMillis = millis();
}


// ── Main Loop ────────────────────────────────────────────────────────────────
void loop() {
  // 1. Parse incoming commands from Pi
  parseSerial();

  // 2. Read sensors
  readToFSensors();
  updateIMU();

  // 3. Apply actuator commands
  applySteering(cmdSteering);
  applySpeed(cmdSpeed);

  // 4. Send sensor packet to Pi at SEND_INTERVAL_MS
  unsigned long now = millis();
  if (now - lastSendMillis >= SEND_INTERVAL_MS) {
    Serial.print("T");
    Serial.print(distLeft);   Serial.print(",");
    Serial.print(distFront);  Serial.print(",");
    Serial.print(distRight);  Serial.print(",");
    Serial.print(yawDegrees, 2); Serial.print(",");
    Serial.println(encoderPulses);
    lastSendMillis = now;
  }
}


// ── Actuator Control ─────────────────────────────────────────────────────────

void applySteering(int value) {
  // value: -100 (full left) to +100 (full right)
  int pulseWidth = map(value, -100, 100, SERVO_MIN_US, SERVO_MAX_US);
  pulseWidth     = constrain(pulseWidth, SERVO_MIN_US, SERVO_MAX_US);
  steeringServo.writeMicroseconds(pulseWidth);
}

void applySpeed(int value) {
  // value: -100 to +100
  if (value == 0) {
    analogWrite(PIN_MOTOR_PWM, 0);
    return;
  }
  if (value > 0) {
    digitalWrite(PIN_MOTOR_IN1, HIGH);
    digitalWrite(PIN_MOTOR_IN2, LOW);
  } else {
    digitalWrite(PIN_MOTOR_IN1, LOW);
    digitalWrite(PIN_MOTOR_IN2, HIGH);
  }
  int pwm = map(abs(value), 0, 100, 0, MOTOR_MAX_PWM);
  analogWrite(PIN_MOTOR_PWM, constrain(pwm, 0, MOTOR_MAX_PWM));
}


// ── Serial Parsing ────────────────────────────────────────────────────────────

void parseSerial() {
  // Expected format: "S<steering>,<speed>\n"
  if (Serial.available() == 0) return;

  String line = Serial.readStringUntil('\n');
  line.trim();

  if (!line.startsWith("S")) return;

  int commaIdx = line.indexOf(',');
  if (commaIdx < 2) return;

  int s = line.substring(1, commaIdx).toInt();
  int v = line.substring(commaIdx + 1).toInt();

  cmdSteering = constrain(s, -100, 100);
  cmdSpeed    = constrain(v, -100, 100);
}


// ── Sensor Setup ─────────────────────────────────────────────────────────────

void setupToFSensors() {
  // Shut all sensors off via XSHUT, then bring up one at a time
  // to assign unique I2C addresses before enabling the next.
  // Right sensor has no XSHUT pin — it's always on at default 0x29.
  // Technique: shut L and F down first, then address R.

  digitalWrite(PIN_TOF_XSHUT_L, LOW);
  digitalWrite(PIN_TOF_XSHUT_F, LOW);
  delay(10);

  // Init RIGHT sensor (already at 0x29)
  if (!tofRight.begin()) {
    Serial.println("ERR: ToF Right init failed");
  }
  tofRight.setDistanceModeShort();
  tofRight.startRanging();

  // Init LEFT sensor
  digitalWrite(PIN_TOF_XSHUT_L, HIGH);
  delay(10);
  if (!tofLeft.begin()) {
    Serial.println("ERR: ToF Left init failed");
  }
  tofLeft.setI2CAddress(TOF_ADDR_LEFT);
  tofLeft.setDistanceModeShort();
  tofLeft.startRanging();

  // Init FRONT sensor
  digitalWrite(PIN_TOF_XSHUT_F, HIGH);
  delay(10);
  if (!tofFront.begin()) {
    Serial.println("ERR: ToF Front init failed");
  }
  tofFront.setI2CAddress(TOF_ADDR_FRONT);
  tofFront.setDistanceModeShort();
  tofFront.startRanging();
}

void setupIMU() {
  imu.initialize();
  if (!imu.testConnection()) {
    Serial.println("ERR: IMU connection failed");
    return;
  }
  // Calibrate gyro Z bias: collect 100 samples at rest
  long sum = 0;
  for (int i = 0; i < 100; i++) {
    sum += imu.getRotationZ();
    delay(3);
  }
  gyroZBias = (float)sum / 100.0f;
  lastIMUMicros = micros();
  Serial.print("IMU bias: ");
  Serial.println(gyroZBias);
}


// ── Sensor Reading ────────────────────────────────────────────────────────────

void readToFSensors() {
  // Non-blocking read — only update if new data is ready
  if (tofLeft.checkForDataReady()) {
    int d = tofLeft.getDistance();
    tofLeft.clearInterrupt();
    if (d > 0) distLeft = d;
  }
  if (tofFront.checkForDataReady()) {
    int d = tofFront.getDistance();
    tofFront.clearInterrupt();
    if (d > 0) distFront = d;
  }
  if (tofRight.checkForDataReady()) {
    int d = tofRight.getDistance();
    tofRight.clearInterrupt();
    if (d > 0) distRight = d;
  }
}

void updateIMU() {
  unsigned long now = micros();
  float dt = (float)(now - lastIMUMicros) / 1e6f;
  lastIMUMicros = now;

  // Gyro Z raw → degrees/sec (sensitivity: 131 LSB/°/s at ±250°/s range)
  float gyroZ_dps = ((float)imu.getRotationZ() - gyroZBias) / 131.0f;

  // Integrate to get heading (yaw)
  yawDegrees += gyroZ_dps * dt;
}


// ── Interrupt Handlers ────────────────────────────────────────────────────────

void onEncoderPulse() {
  encoderPulses++;
}

void onStartButton() {
  // Debounce: ignore if pressed recently
  static unsigned long lastPressMs = 0;
  unsigned long now = millis();
  if (now - lastPressMs > 200) {
    startPressed  = true;
    lastPressMs   = now;
  }
}
