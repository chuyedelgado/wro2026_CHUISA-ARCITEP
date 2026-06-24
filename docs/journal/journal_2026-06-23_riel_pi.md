# Journal 2026-06-23 — Riel de la Pi (Mini560 5V) VALIDADO ✅

## Objetivo
Alimentar la Raspberry Pi 5 desde la batería con el buck **Mini560 (5V fijo)** y
**validar el riel bajo carga**. Es el componente más caro del robot → máxima cautela:
"la Pi no se conecta hasta que el multímetro confirme ~5V limpios".

## Hardware y decisión de ingeniería
- **Mini560** (DORHEA): buck step-down de **salida FIJA 5V / 5A**. Entrada ~7–20V
  (3S entra sin problema).
- **Por qué buck FIJO y no ajustable:** el potenciómetro de un buck ajustable puede
  **derivar con la vibración** y subir el voltaje → riesgo de matar la Pi. **Fijo = seguro.**
- Alimentado desde la **Batería A (lógica)**, LiPo 3S GOLDBAT (medida **11.52V**),
  separada de la batería del motor para aislar a la Pi de los picos del motor.

## Pinout del Mini560 (verificado en placa)
- **Entrada:** `IN+` / `IN−` (lado de origen de la flecha impresa).
- **Salida:** `OUT+` / `OUT−`.
- La **flecha** impresa indica el sentido del flujo (entra → sale).

## Cableado a la Pi
| Mini560 | Pi (header 40 pines) |
|---|---|
| OUT+ (5V) | **Pin 4** (+5V) |
| OUT− (GND) | **Pin 14** (GND) |

> El pin 6 ya estaba ocupado por el GND del UART (Bloque 4); los 8 pines GND del
> header son comunes, así que se usó el pin 14. Alimentar por GPIO **salta la
> protección de entrada** de la Pi → polaridad y pin verificados (continuidad) antes
> de energizar.

## Mediciones (reales)
- **Salida en vacío** (sin la Pi conectada): **5.145V**.
- **Bajo carga** (`stress-ng --cpu 4 --timeout 60s`): **5.122–5.123V**
  (caída de apenas **~8 mV** respecto al reposo).
- Tras el estrés: **5.130V**.
- **`vcgencmd get_throttled` = `0x0`** → la Pi no detectó bajo voltaje ni throttling. ✅

## Conclusión
Riel **Mini560 → Pi validado y sólido**: se mantiene **≥4.9V con holgura** bajo carga
máxima de CPU, sin throttling. La caída mínima (~8 mV) confirma una fuente firme con
mucha reserva. La decisión del buck fijo 5V queda respaldada con datos.

## Pendiente / opcional
- Optimización opcional: `usb_max_current_enable=1` en `/boot/firmware/config.txt`
  (habilita corriente USB completa; el Mini560 es de 5A). No crítico: la cámara es CSI,
  no USB.
- Corriente real de la Pi (media/pico) → por medir para el presupuesto de potencia.
