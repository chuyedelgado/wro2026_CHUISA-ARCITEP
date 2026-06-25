# Journal 2026-06-24 — Riel del motor (Cytron MD10C + JGB37) VALIDADO ✅

## Objetivo
Poner en marcha el **tercer y último riel de potencia**: Batería B → fusible →
Cytron MD10C → motor JGB37-520, en **lazo abierto y PWM bajo**. Primer giro del
tren motriz.

## Hardware
- **Motor JGB37-520** (12V, 530 RPM nominal, encoder Hall) — caracterizado antes
  (11 PPR en el eje del motor, reducción 18.8:1).
- **Driver Cytron MD10C R3** (13A continuos / 30A pico, interfaz PWM+DIR).
- **Batería B** (LiPo 3S GOLDBAT), **separada de la Batería A** (lógica) → aísla los
  picos del motor de la Pi.
- **Fusible de vidrio 5A** en el riel del motor (portafusibles en serie en el +).

## Pinout del Cytron MD10C (verificado en placa)
- Bornera verde (arriba→abajo): `POWER+`, `POWER−`, `MOTOR A`, `MOTOR B`.
- Control (`INPUT`): `DIR`, `PWM`, `GND`.
- Tabla de verdad: `PWM=0` → parado; `PWM=1, DIR=0` → un sentido;
  `PWM=1, DIR=1` → el otro.

## Cableado
| Conexión | Detalle |
|---|---|
| Potencia | Batería B (+) → **fusible 5A** → POWER+ ; Batería B (−) → POWER− |
| Motor | MOTOR A → motor **rojo** ; MOTOR B → motor **blanco** |
| Control | Arduino **D3** (PWM) → PWM ; Arduino **D2** (DIR) → DIR ; Arduino GND → Cytron GND (**tierra común**) |

> El encoder sigue en D4/D5, alimentado por el 5V del Arduino.

## Prueba (lazo abierto, PWM limitado a 40%)
- El motor gira **suave en ambos sentidos**. **Nada se calienta** (Cytron, fusible). Sin olor.

## Corriente medida (multímetro en serie, vía portafusibles)
| Condición | Corriente |
|---|---|
| 20% PWM (vacío) | ~107–108 mA |
| 40% PWM (vacío) | ~150 mA |
| Frenando un poco las ruedas | pico ~195 mA |

> La medición a 40% (**150 mA**) coincide **exactamente** con la hoja del JGB37
> (0.15A en vacío) → motor sano y dentro de especificación.

## Fusible — decisión con datos
- Hoja: marcha 0.15A, **stall 2.4A**. Fusible de **5A** → ~2× por encima del stall:
  no salta en operación ni en bloqueos breves, pero protege ante un corto real.
  **5A confirmado como adecuado.**

## Estado del árbol de potencia (3 rieles validados con datos reales)
| Riel | Resultado |
|---|---|
| Servo (UBEC 6V) | salida **6.22V** ✅ |
| Pi (Mini560 5V) | **5.122V** bajo carga, `throttled=0x0` ✅ |
| Motor (Cytron) | gira ambos sentidos, **~0.15A** marcha, fusible 5A ✅ |

## Pendiente
- Integrar el **switch DPST** como único encendido que corta **ambas baterías**
  (regla 9.10) → unifica y deja legal el árbol de potencia.
- Corriente de arranque/stall real bajo carga de pista (cuando esté montado el robot).
