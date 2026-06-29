# Journal 2026-06-29 — UART migrado a placa permanente (enlace validado) ✅

## Objetivo
Migrar la conexión **UART Pi ↔ Arduino** (con su divisor de voltaje) de protoboard a un
**mini-perfboard permanente**, y validar el enlace físico. Era **lo último** que quedaba
en protoboard.

## El divisor (nivelador 5V → 3.3V)
El Arduino (Nano Every) es de **5V** y la Pi de **3.3V**. La línea Arduino-TX → Pi-RX
pasa por un divisor que baja 5V a ~3.3V seguros:
```
Arduino TX (D1) ──[ R1 = 1k ]──┬──[ R2 = 2.2k ]── GND
                              NODO ─────────────► Pi RX (pin 10)
```
- Armado en mini-perfboard (3×7cm), soldado, con 3 conectores: TX-in (A), nodo (B), GND (C).
- **Medición del nodo (TX en ALTO): 3.299V** ✅ — casi idéntico a los 3.294V del protoboard.
  Dentro del rango seguro de la Pi.

## Mapa de conexión UART
| Línea | Conexión |
|---|---|
| Arduino TX (D1) → divisor → **Pi RX (pin 10)** | con divisor (5V→3.3V) |
| **Pi TX (pin 8)** → Arduino **D0** | directo (3.3V lo lee el Nano como ALTO) |
| GND común | divisor C ↔ Pi pin 6 ↔ Arduino GND |
> El UART del Nano Every es **Serial1** (D0/D1), no `Serial` (que es el USB).

## Validación (prueba de eco del enlace físico)
- Arduino con sketch de eco (repite en Serial1); Pi envía y compara.
- **Resultado: 2735 mensajes enviados, 0 errores** en 60 s. **Enlace físico limpio.** ✅

## Aprendizaje clave (diagnóstico del día)
- Lecturas raras iniciales (3.75V, luego nada) eran **lecturas fantasma de un pin
  flotando**: el divisor solo entrega voltaje real cuando el Arduino **mantiene D1 en
  ALTO por programa**. **"Conectado/energizado" ≠ "D1 en ALTO"** — el estado del pin lo
  fija el sketch cargado. Las resistencias siempre estuvieron bien.
- El multímetro (EMTOP) **auto-detecta**: muestra voltios si hay voltaje, ohmios si no.
  Mostrar resistencia cuando el circuito está sin energía es normal, no un defecto.

## Estado
**UART migrado y enlace físico validado.** Con esto, **toda la electrónica está fuera del
protoboard** (placa de sensores, distribución de potencia, switch, UART). Protoboard libre.

## Pendiente
- **Validación completa de protocolo** (10 min con mensajes `S`/`T` + **checksum** +
  **failsafe**) → requiere el **firmware real** (de María), que aún hay que terminar para
  que coincida con el hardware real (Cytron MD10C, 2 ToF en 0x29/0x2A + MPU 0x68, pines
  reales, Serial1, checksum XOR, failsafe ~200ms).
- ⚠️ **El `main.ino` del repo sigue siendo PLANTILLA** (TB6612FNG, 3 ToF, `Serial` USB,
  sin checksum). Corregirlo **antes del congelamiento del 2 jul** — los jueces leen el código.
- Soldar botón de inicio (A0) + LED (A1) al final del montaje.
