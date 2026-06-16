/*
 * uart_protocolo_test.ino — Equipo CHUISA ARCITEP (WRO 2026 Future Engineers)
 *
 * PAPEL EN LA MISIÓN:
 *   Recibe comandos de la Raspberry Pi por UART (Serial1 = pines TX1/RX0) con
 *   formato  S<steer>,<speed>*<checksum>  y los valida con checksum XOR.
 *   Implementa el FAILSAFE: si no llega un comando valido en TIMEOUT_MS,
 *   detiene el motor y centra la direccion (no sigue a ciegas).
 *
 *   Es la semilla de la parte de comunicacion del firmware final (main.ino).
 *
 * CANAL: Serial1 (pines fisicos) hacia la Pi, independiente del USB de depuracion.
 * SEGURIDAD: el TX1 (5V) va a la Pi a traves de un divisor de voltaje (1k/2.2k -> 3.3V).
 */

unsigned long ultimoComandoValido = 0;
const unsigned long TIMEOUT_MS = 500;   // failsafe (coincide con config.py COMM_TIMEOUT_MS)

int steer = 0;     // -100 (izq) .. +100 (der), 0 = centro
int speed = 0;     // -100 .. +100, 0 = stop
bool enFailsafe = false;

// Checksum: XOR de todos los caracteres del texto
byte calcularChecksum(String s) {
  byte cs = 0;
  for (unsigned int i = 0; i < s.length(); i++) cs ^= s[i];
  return cs;
}

void setup() {
  Serial.begin(115200);     // USB, depuracion
  Serial1.begin(115200);    // hacia la Pi (pines fisicos)
  ultimoComandoValido = millis();
}

void loop() {
  // --- Recepcion con verificacion de checksum ---
  if (Serial1.available()) {
    String linea = Serial1.readStringUntil('\n');
    linea.trim();
    int posAst = linea.indexOf('*');
    if (linea.startsWith("S") && posAst > 0) {
      String cuerpo = linea.substring(0, posAst);          // "S0,50"
      byte csRecibido = (byte) linea.substring(posAst + 1).toInt();
      if (csRecibido == calcularChecksum(cuerpo)) {
        int posComa = cuerpo.indexOf(',');
        steer = cuerpo.substring(1, posComa).toInt();
        speed = cuerpo.substring(posComa + 1).toInt();
        ultimoComandoValido = millis();
        if (enFailsafe) {                  // volvio la comunicacion
          Serial.println(">> Comunicacion restaurada");
          enFailsafe = false;
        }
        Serial.print("VALIDO -> steer="); Serial.print(steer);
        Serial.print(" speed="); Serial.println(speed);
      } else {
        Serial.print("DESCARTADO (checksum): "); Serial.println(linea);
      }
    }
  }

  // --- Failsafe: entra UNA sola vez al perder la comunicacion ---
  if (millis() - ultimoComandoValido > TIMEOUT_MS && !enFailsafe) {
    steer = 0;
    speed = 0;
    enFailsafe = true;
    Serial.println("!! FAILSAFE ACTIVADO: motor a 0, direccion centrada");
  }

  // NOTA: aqui (firmware final) steer/speed se aplicarian al servo y al motor.
}
