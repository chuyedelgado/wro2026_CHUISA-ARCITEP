/*
 * sensores_i2c_test.ino — Equipo CHUISA ARCITEP (WRO 2026 Future Engineers)
 *
 * PAPEL EN LA MISIÓN:
 *   Lee a la vez los tres sensores I2C del robot:
 *     - 2x ToF VL53L1X  -> distancia a las paredes (entrada del PID de wall-following)
 *     - 1x MPU-6050      -> yaw (giros de 90 grados y conteo de vueltas)
 *
 * RETO RESUELTO (re-direccionamiento XSHUT):
 *   Los dos ToF salen de fabrica en la MISMA direccion 0x29 y chocarian en el bus.
 *   Se encienden de a uno via XSHUT y se renombra el primero:
 *     ToF #1 -> 0x2A   |   ToF #2 -> 0x29 (de fabrica)
 *
 * CONEXIONES:
 *   Bus I2C: A4 (SDA), A5 (SCL)  -- compartido por los 3 sensores
 *   XSHUT:   D2 (ToF #1), D3 (ToF #2)
 *   MPU en 0x68 (AD0 sin conectar)
 *
 * LIBRERIAS: VL53L1X (Pololu), MPU6050_light (rfetick)
 *
 * NOTA: la asignacion izquierda/derecha de los ToF es PROVISIONAL
 *       hasta el montaje fisico en el chasis.
 */

#include <Wire.h>
#include <VL53L1X.h>
#include <MPU6050_light.h>

#define XSHUT_1  2          // ToF #1 -> D2
#define XSHUT_2  3          // ToF #2 -> D3
#define ADDR_TOF1  0x2A     // direccion nueva del ToF #1
// El ToF #2 queda en su 0x29 de fabrica.

VL53L1X tofIzq;             // ToF #1 (provisional: izquierda)
VL53L1X tofDer;             // ToF #2 (provisional: derecha)
MPU6050 mpu(Wire);

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Wire.setClock(400000);   // I2C a 400 kHz

  // --- 1) Apagar AMBOS ToF (XSHUT en bajo = apagado) ---
  pinMode(XSHUT_1, OUTPUT);
  pinMode(XSHUT_2, OUTPUT);
  digitalWrite(XSHUT_1, LOW);
  digitalWrite(XSHUT_2, LOW);
  delay(10);

  // --- 2) Encender SOLO el ToF #1 y renombrarlo a 0x2A ---
  pinMode(XSHUT_1, INPUT);          // soltar XSHUT = encender (pull-up interno)
  delay(10);
  if (!tofIzq.init()) { Serial.println("ERROR: ToF #1 no responde"); while (1) {} }
  tofIzq.setAddress(ADDR_TOF1);
  tofIzq.setDistanceMode(VL53L1X::Long);
  tofIzq.setMeasurementTimingBudget(50000);
  tofIzq.startContinuous(50);

  // --- 3) Encender el ToF #2 (queda en 0x29) ---
  pinMode(XSHUT_2, INPUT);
  delay(10);
  if (!tofDer.init()) { Serial.println("ERROR: ToF #2 no responde"); while (1) {} }
  tofDer.setDistanceMode(VL53L1X::Long);
  tofDer.setMeasurementTimingBudget(50000);
  tofDer.startContinuous(50);

  // --- 4) Iniciar y calibrar el MPU (sensor QUIETO al arrancar) ---
  byte st = mpu.begin();
  if (st != 0) { Serial.println("ERROR: MPU no responde"); while (1) {} }
  Serial.println("Calibrando MPU... NO MUEVAS nada (2 s).");
  delay(1000);
  mpu.calcOffsets();

  Serial.println("Sistema sensorial completo activo.\n");
}

void loop() {
  mpu.update();

  static unsigned long ultimo = 0;
  if (millis() - ultimo > 200) {     // imprime ~5 veces por segundo
    Serial.print("ToF Izq: "); Serial.print(tofIzq.read()); Serial.print(" mm");
    Serial.print("  |  ToF Der: "); Serial.print(tofDer.read()); Serial.print(" mm");
    Serial.print("  |  Yaw: "); Serial.print(mpu.getAngleZ(), 1); Serial.println(" grados");
    ultimo = millis();
  }
}
