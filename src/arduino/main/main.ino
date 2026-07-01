// firmware_chuisa.ino — Controlador de bajo nivel. CHUISA ARCITEP, WRO 2026.
// (TÚ completas los valores según nuestro mapa real)

#include <Wire.h>
#include <Servo.h>
#include <VL53L1X.h>          // Pololu
#include <MPU6050_light.h>    // rfetick

// --- Actuadores ---
const uint8_t PIN_SERVO     = 9;
const uint8_t PIN_MOTOR_DIR = 2;   // Cytron DIR
const uint8_t PIN_MOTOR_PWM = 3;   // Cytron PWM

// --- Encoder ---
const uint8_t PIN_ENC_A = 4;
const uint8_t PIN_ENC_B = 5;

// --- Sensores (XSHUT de los ToF) ---
const uint8_t PIN_XSHUT1 = 7;
const uint8_t PIN_XSHUT2 = 8;
// I2C: A4 (SDA), A5 (SCL) — fijos por hardware

// --- Botón y LED ---
const uint8_t PIN_BTN = A0;
const uint8_t PIN_LED = A1;

// --- Actuadores: límites (CALIBRAR los reales luego) ---
const int SERVO_CENTER  = 1600;  // centro
const int SERVO_LEFT    = 1400;  // steer -100  (conservador por ahora)
const int SERVO_RIGHT   = 1800;  // steer +100  (conservador por ahora)
const int MOTOR_MAX_PWM = 150;   // tope de PWM (de 255) — arranca bajo, sube con cuidado

Servo steeringServo;
VL53L1X tof1, tof2;           // tof1 → 0x2A,  tof2 → 0x29
MPU6050 mpu(Wire);            // 0x68

// --- Lecturas de sensores ---
int   distancia1 = 0;   // mm, ToF1 (0x2A)
int   distancia2 = 0;   // mm, ToF2 (0x29)
float yaw        = 0.0; // grados, del MPU

volatile long encoderPulsos = 0;   // con signo: + adelante, - atrás

// --- Comandos recibidos de la Pi ---
int  cmdSteer = 0;                 // último steer válido
int  cmdSpeed = 0;                 // último speed válido
unsigned long ultimoComandoMs = 0; // cuándo llegó el último comando válido
const unsigned long FAILSAFE_MS = 200;  // tu decisión: 200 ms

enum Estado { IDLE, READY, RUN };
Estado estado = IDLE;

void initSensors() {
  Wire.begin();
  Wire.setClock(400000);

  // --- Secuencia XSHUT (tu técnica validada) ---
  pinMode(PIN_XSHUT1, OUTPUT);
  pinMode(PIN_XSHUT2, OUTPUT);
  digitalWrite(PIN_XSHUT1, LOW);
  digitalWrite(PIN_XSHUT2, LOW);
  delay(10);

  // ToF1 → encender y renombrar a 0x2A
  pinMode(PIN_XSHUT1, INPUT);
  delay(10);
  if (tof1.init()) {
    tof1.setAddress(0x2A);
    tof1.setDistanceMode(VL53L1X::Short);   // modo corto: mejor precisión <1.3m
    tof1.setMeasurementTimingBudget(50000); // 50ms
    tof1.startContinuous(50);
    Serial.println("ToF1 OK (0x2A)");
  } else {
    Serial.println("ERROR: ToF1 no responde");
  }

  // ToF2 → encender, queda en 0x29
  pinMode(PIN_XSHUT2, INPUT);
  delay(10);
  if (tof2.init()) {
    tof2.setDistanceMode(VL53L1X::Short);
    tof2.setMeasurementTimingBudget(50000);
    tof2.startContinuous(50);
    Serial.println("ToF2 OK (0x29)");
  } else {
    Serial.println("ERROR: ToF2 no responde");
  }

  // MPU-6050 (0x68)
  byte status = mpu.begin();
  if (status == 0) {
    Serial.println("MPU OK - calibrando, NO MOVER...");
    delay(1000);
    mpu.calcOffsets();   // calibra bias con el robot QUIETO
    Serial.println("MPU calibrado");
  } else {
    Serial.print("ERROR: MPU status ");
    Serial.println(status);
  }
}

void readSensors() {
  // ToF: leer solo si hay dato nuevo (sin bloquear)
  if (tof1.dataReady()) distancia1 = tof1.read(false);
  if (tof2.dataReady()) distancia2 = tof2.read(false);

  // MPU: hay que actualizarlo cada vuelta para que integre el yaw
  mpu.update();
  yaw = mpu.getAngleZ();
}

void applySteering(int steer) {
  // steer: -100 (izq) .. +100 (der)
  steer = constrain(steer, -100, 100);           // seguridad: nunca fuera de rango
  int us = map(steer, -100, 100, SERVO_LEFT, SERVO_RIGHT);
  steeringServo.writeMicroseconds(us);
}

void applySpeed(int speed) {
  // speed: -100 (reversa) .. +100 (adelante), 0 = parar
  speed = constrain(speed, -100, 100);
  if (speed == 0) {                              // parada explícita
    analogWrite(PIN_MOTOR_PWM, 0);
    return;
  }
  digitalWrite(PIN_MOTOR_DIR, speed > 0 ? LOW : HIGH);  // LOW = adelante (según tu prueba)
  int pwm = map(abs(speed), 0, 100, 0, MOTOR_MAX_PWM);
  analogWrite(PIN_MOTOR_PWM, pwm);
}

// Calcula el XOR de todos los caracteres de un texto → un byte
byte calcularChecksum(const char* datos, int longitud) {
  byte chk = 0;
  for (int i = 0; i < longitud; i++) {
    chk ^= datos[i];     // ^= es "XOR y guarda"
  }
  return chk;
}

void onEncoderPulse() {
  // Se dispara en cada flanco de subida del canal A.
  // Miramos B para saber la dirección:
  if (digitalRead(PIN_ENC_B) == LOW) encoderPulsos--;   // un sentido
  else                                encoderPulsos++;   // el otro
}

void enviarTelemetria() {
  // 1. Armar el contenido en un buffer de texto
  char buffer[48];
  int n = snprintf(buffer, sizeof(buffer), "T%d,%d,%d,%ld",
                   distancia1, distancia2, (int)yaw, encoderPulsos);

  // 2. Calcular el checksum de ese contenido
  byte chk = calcularChecksum(buffer, n);

  // 3. Enviar por Serial1 (a la Pi): contenido * checksum \n
  Serial1.print(buffer);
  Serial1.print('*');
  Serial1.println(chk);   // println agrega el \n final
}

void recibirComandos() {
  // Formato esperado: "S<steer>,<speed>*<checksum>\n"
  if (!Serial1.available()) return;

  char buffer[48];
  int n = Serial1.readBytesUntil('\n', buffer, sizeof(buffer) - 1);
  if (n <= 0) return;
  buffer[n] = '\0';                 // cierra el texto

  // 1. Separar contenido y checksum en el '*'
  char* asterisco = strchr(buffer, '*');
  if (asterisco == NULL) return;    // mal formado: sin checksum
  *asterisco = '\0';                // corta el buffer en el '*'
  byte chkRecibido = atoi(asterisco + 1);

  // 2. Verificar el checksum
  byte chkCalculado = calcularChecksum(buffer, strlen(buffer));
  if (chkCalculado != chkRecibido) return;   // corrupto → descartar

  // 3. Parsear "S<steer>,<speed>"
  if (buffer[0] != 'S') return;
  char* coma = strchr(buffer, ',');
  if (coma == NULL) return;
  *coma = '\0';

  cmdSteer = atoi(buffer + 1);      // desde después de la 'S'
  cmdSpeed = atoi(coma + 1);        // desde después de la ','
  ultimoComandoMs = millis();       // ¡llegó un comando VÁLIDO!
}

void aplicarComandosConFailsafe() {
  if (millis() - ultimoComandoMs > FAILSAFE_MS) {
    // La Pi se calló → PARAR por seguridad
    applySpeed(0);
    applySteering(0);
  } else {
    // Comunicación viva → ejecutar el último comando válido
    applySteering(cmdSteer);
    applySpeed(cmdSpeed);
  }
}

bool botonPulsado() {
  if (digitalRead(PIN_BTN) == HIGH) return false;  // en reposo, nada
  delay(20);                                        // espera el rebote (solo en READY, robot quieto)
  return (digitalRead(PIN_BTN) == LOW);             // ¿sigue pulsado? → válido
}

void actualizarLED() {
  if (estado == RUN) {
    digitalWrite(PIN_LED, HIGH);              // RUN → fijo
  } else {
    digitalWrite(PIN_LED, (millis() / 300) % 2);  // READY → parpadeo cada 300ms
  }
}

void setup() {
  // 1. Dos puertos serie
  Serial.begin(115200);    // USB (depuración hacia la PC)
  Serial1.begin(115200);   // UART hacia la Pi (D0/D1) — el del divisor

  // 2. Pines de salida del motor
  pinMode(PIN_MOTOR_DIR, OUTPUT);
  pinMode(PIN_MOTOR_PWM, OUTPUT);
  analogWrite(PIN_MOTOR_PWM, 0);     // motor PARADO (seguro)

  // 3. Servo al centro
  steeringServo.attach(PIN_SERVO);
  steeringServo.writeMicroseconds(1500);   // centro (ajustaremos el real luego)

  // 4. Botón y LED
  pinMode(PIN_BTN, INPUT_PULLUP);    // botón: ALTO en reposo, BAJO al pulsar
  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, LOW);

  // 5. Aviso de que arrancó (por USB, para que TÚ lo veas)
  Serial.println("Firmware iniciado - estado seguro");

  initSensors();
  pinMode(PIN_ENC_A, INPUT_PULLUP);
  pinMode(PIN_ENC_B, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_ENC_A), onEncoderPulse, RISING);
  estado = READY;
  Serial.println("Estado: READY - esperando boton");

}

void loop() {
  actualizarLED();

  // Bloque de control a ~50 Hz
  static unsigned long t = 0;
  if (millis() - t >= 20) {
    t = millis();

    readSensors();
    recibirComandos();      // siempre: drena el buffer y actualiza comandos
    enviarTelemetria();     // la Pi siempre recibe datos

    if (estado == READY) {
      applySpeed(0);        // motor FORZADO a 0 (no se mueve aunque la Pi mande)
      applySteering(0);
      if (botonPulsado()) {
        estado = RUN;
        Serial.println("Estado: RUN - arrancando");
        Serial1.println("START");   // avisa a la Pi (opcional)
      }
    }
    else if (estado == RUN) {
      aplicarComandosConFailsafe();   // ahora sí obedece (con failsafe)
    }
  }
}