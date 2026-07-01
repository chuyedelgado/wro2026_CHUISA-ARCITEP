# Journal 2026-06-30 — Firmware del Arduino (controlador de bajo nivel) COMPLETO ✅

**Autor:** Jesús (Hardware Lead). Construido por módulos, probando cada uno antes de seguir.

## Objetivo
Escribir el **firmware real** del Arduino Nano Every que **coincida con el hardware real**,
reemplazando la plantilla vieja del repo (que tenía TB6612FNG, 3 ToF, `Serial` USB, sin
checksum — nada de eso es nuestro hardware).

## Rol en la arquitectura
El Arduino es el **ejecutor de bajo nivel**: no decide (eso lo hace la Pi), **ejecuta y
reporta**. Garantiza los tiempos duros (ISR del encoder, PWM estable, failsafe) que Python
en la Pi no asegura. La Pi manda *intenciones*; el Arduino las ejecuta con seguridad propia.

## Módulos (todos validados en banco)
| # | Módulo | Qué hace |
|---|---|---|
| 1 | Cimientos | Mapa de pines real |
| 2 | `setup()` seguro | Motor parado + servo centro + 2 seriales al arrancar |
| 3 | Sensores I2C | 2× ToF (Pololu VL53L1X) + MPU (MPU6050_light) vía XSHUT |
| 4 | Lectura sin bloqueo | Distancias + yaw sin congelar el loop |
| 5 | Actuadores | `applySteering()` y `applySpeed()` con límites |
| 6 | Encoder | ISR con dirección (odometría con signo) |
| 7 | UART | Protocolo con checksum XOR + failsafe |
| 8 | Botón/LED + FSM | Máquina de estados IDLE→READY→RUN |

## Mapa de pines real
```
D0/D1  UART ↔ Pi (Serial1)     D2  Cytron DIR      D3  Cytron PWM
D4     Encoder A               D5  Encoder B
D7     XSHUT1 (ToF1→0x2A)      D8  XSHUT2 (ToF2→0x29)
D9     Servo señal
A0     Botón (INPUT_PULLUP)    A1  LED de estado
A4/A5  I2C (SDA/SCL) → ToF 0x29, 0x2A + MPU 0x68
```

## Protocolo UART (Serial1, 115200)
- **Pi → Arduino:** `S<steer>,<speed>*<checksum>\n`  (steer/speed: −100..+100)
- **Arduino → Pi:** `T<d1>,<d2>,<yaw>,<enc>*<checksum>\n`  (~50 Hz)
- **Checksum:** XOR de los caracteres del contenido. Mensaje corrupto → se descarta.
- **Parsing robusto:** descarta si falta `*`, si el checksum no cuadra, si no empieza en
  `S`, o si falta la `,`. **Un mensaje corrupto nunca mueve el robot.**
- **Failsafe:** sin comando válido en **200 ms** → motor 0, servo centro. Reacciona al
  **silencio** (no depende de que la Pi avise). 200 ms = 10 comandos perdidos a 50 Hz.

## Máquina de estados (reglas 9.11 y 9.14)
```
IDLE (arranque + calibración) → READY (espera botón) → RUN (opera)
```
- **IDLE/READY:** el motor está **FORZADO a 0** aunque la Pi mande comandos → el robot
  no se mueve hasta pulsar el botón (cumple standby 9.11).
- **READY:** LED **parpadea** (sin `delay`, con `(millis()/300)%2`). Botón con antirrebote.
- **RUN:** botón pulsado → obedece a la Pi (con failsafe). LED **fijo**.

## Decisiones de ingeniería clave (para el juez)
- **`Serial1` vs `Serial`:** la Pi está cableada a D0/D1 = `Serial1`; `Serial` es el USB
  (solo depuración). En el Nano Every son puertos separados.
- **Lectura ToF sin bloqueo:** `read()` por defecto espera hasta 50 ms → congelaría el
  loop; se usa `dataReady()` + `read(false)` para mantener el lazo rápido y parejo.
- **`volatile` en `encoderPulsos`:** la variable cambia dentro de una interrupción.
- **Encoder de 2 canales (cuadratura):** un canal cuenta, el segundo da la **dirección**
  (signo). Esencial para el parking en reversa (debe restar).
- **`constrain()` en actuadores:** el firmware se protege solo aunque la Pi mande un valor
  fuera de rango.
- **Failsafe por silencio:** la seguridad no depende de que la Pi "avise" que falló.

## Validación (banco, robot elevado)
- 3 sensores inicializan y leen (ToF reaccionan a la mano; yaw cambia al girar). ✅
- Servo dobla a ambos lados; motor gira en ambos sentidos. ✅
- **Deadband del motor detectado:** `M20` solo zumba, `M50` gira → hay un PWM mínimo de
  arranque (medir el valor exacto). Dato para el control de velocidad.
- Encoder: adelante **suma**, atrás **resta**. ✅
- Telemetría `T...*...` llega a la Pi; valores cambian con mano/rueda. ✅
- Comandos de la Pi mueven el robot (envío continuo a 50 Hz). ✅
- **Failsafe:** al cortar la comunicación, el motor **para solo** (~200 ms). ✅
- **FSM:** en READY ignora comandos (motor quieto, LED parpadea); al botón → RUN (obedece,
  LED fijo). ✅

## Estado
**Firmware COMPLETO y validado en banco.** Reemplaza la plantilla del repo en
`src/arduino/main/main.ino`. Ahora el código coincide con el hardware real.

## Pendiente
- **Calibrar valores reales:** centro y límites del servo, y el **PWM mínimo de arranque**
  (deadband hallado hoy).
- Validar el **checksum de la telemetría** del lado de la Pi (María).
- **Lógica autónoma** (visión, PID wall-following, FSM de alto nivel) → vive en la **Pi**,
  tarea de María. Este firmware es la **base** sobre la que ella construye.
- Soldar el **botón/LED definitivos** en el montaje final (ahora en cables de prueba).
