/*
 * telemetria_test.ino — Equipo CHUISA ARCITEP (WRO 2026 Future Engineers)
 *
 * PAPEL EN LA MISIÓN:
 *   Une los Bloques 3 (sensores) y 4 (UART): el Arduino lee sus sensores y los
 *   reporta a la Raspberry Pi en tiempo real (el "sistema nervioso" del robot).
 *
 *   Lee 2x ToF VL53L1X + MPU-6050 y los envia por Serial1 con el formato:
 *       T<tof_izq>,<tof_der>,<yaw>*<checksum>
 *   El checksum (XOR) permite a la Pi descartar mensajes corruptos.
 *
 * ALCANCE ACTUAL vs ARQUITECTURA:
 *   La arquitectura define la telemetria completa T<tof_l>,<tof_f>,<tof_r>,<yaw>,<enc>.
 *   Hoy se envia lo que EXISTE: 2 ToF + yaw. Faltan por integrar (cuando existan):
 *     - 3er ToF (frontal)         -> deteccion de esquina/parada
 *     - encoder (motor JGB37)     -> odometria (meta y parking)
 *
 * CONEXIONES: bus I2C en A4/A5 (compartido); XSHUT en D2 (#1) y D3 (#2).
 *             UART hacia la Pi por Serial1 (TX1 via divisor de voltaje -> Pi RX).
 * LIBRERIAS: VL53L1X (Pololu), MPU6050_light (rfetick).
 */

#include <Wire.h>
#include <VL53L1X.h>
#include <MPU6050_light.h>

#define XSHUT_1 2
#define XSHUT_2 3

VL53L1X tofIzq, tofDer;     // asignacion izq/der provisional hasta el montaje fisico
MPU6050 mpu(Wire);

unsigned long ultimoEnvio = 0;
const unsigned long PERIODO_MS = 100;   // 10 telemetrias/seg (legible para validar)

byte calcularChecksum(String s) {
  byte cs = 0;
  for (unsigned int i = 0; i < s.length(); i++) cs ^= s[i];
  return cs;
}

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);
  Wire.begin();
  Wire.setClock(400000);

  // --- 2 ToF con re-direccionamiento XSHUT (#1 -> 0x2A, #2 -> 0x29) ---
  pinMode(XSHUT_1, OUTPUT); pinMode(XSHUT_2, OUTPUT);
  digitalWrite(XSHUT_1, LOW); digitalWrite(XSHUT_2, LOW);
  delay(10);
  pinMode(XSHUT_1, INPUT); delay(10);
  if (!tofIzq.init()) { Serial.println("ERROR ToF #1"); while (1) {} }
  tofIzq.setAddress(0x2A);
  tofIzq.setDistanceMode(VL53L1X::Long);
  tofIzq.setMeasurementTimingBudget(50000);
  tofIzq.startContinuous(50);
  pinMode(XSHUT_2, INPUT); delay(10);
  if (!tofDer.init()) { Serial.println("ERROR ToF #2"); while (1) {} }
  tofDer.setDistanceMode(VL53L1X::Long);
  tofDer.setMeasurementTimingBudget(50000);
  tofDer.startContinuous(50);

  // --- MPU (sensor QUIETO al arrancar para calibrar el bias) ---
  if (mpu.begin() != 0) { Serial.println("ERROR MPU"); while (1) {} }
  Serial.println("Calibrando MPU... NO MUEVAS nada (2 s).");
  delay(1000);
  mpu.calcOffsets();
  Serial.println("Enviando telemetria a la Pi...");
}

void loop() {
  mpu.update();   // actualizar el yaw con frecuencia

  if (millis() - ultimoEnvio >= PERIODO_MS) {
    int dIzq = tofIzq.read();
    int dDer = tofDer.read();
    float yaw = mpu.getAngleZ();

    String cuerpo = "T" + String(dIzq) + "," + String(dDer) + "," + String(yaw, 1);
    byte cs = calcularChecksum(cuerpo);
    Serial1.print(cuerpo); Serial1.print("*"); Serial1.println(cs);

    // eco por USB para depuracion
    Serial.print("TX -> "); Serial.print(cuerpo); Serial.print("*"); Serial.println(cs);
    ultimoEnvio = millis();
  }
}
