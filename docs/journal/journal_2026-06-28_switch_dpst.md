# Journal 2026-06-28 — Switch DPST + PolySwitch: árbol de potencia CERRADO ✅

## Objetivo
Integrar el **único interruptor de encendido (DPST)** que corta **ambas baterías** con
una sola acción (**regla 9.10**), y añadir el **PolySwitch** (protección auto-reseteable)
al riel lógico. Esto **unifica y cierra** el árbol de potencia.

## Switch usado (dato real)
- **KCD4**, rocker **DPST** (4 terminales en 2×2 = 2 polos). Rating impreso:
  **16A 250VAC / 20A 125VAC**.
- **Nota AC vs DC:** está marcado solo en AC, pero a **12V** y con un margen de 16–20A
  es **adecuado** (el arco de DC que preocupa en switches AC es problema a voltajes
  altos, no a 12V). Práctica de operación: **apagar con el robot detenido**.
- ⚠️ *Doc pendiente:* el BOM original listaba un Twidec KCD2-201N; **actualizar a este
  KCD4** para mantener "cero datos inventados".

## Mapeo de terminales (verificado con continuidad)
- **Polo 1 = TL–BL** (pita en ON, abierto en OFF).
- **Polo 2 = TR–BR** (pita en ON, abierto en OFF).
- Los dos polos **aislados entre sí**. ✅

## Cableado (soldado, cada espada aislada con termorretráctil)
```
POLO 1 — LÓGICA (Batería A):
   Batería A (+) → TL
   BL → PolySwitch → (Mini560 IN+  y  UBEC IN+)
   Batería A (−) → (Mini560 IN−  y  UBEC IN−)        [no pasa por el switch]

POLO 2 — MOTOR (Batería B):
   Batería B (+) → TR
   BR → fusible 5A → Cytron POWER+
   Batería B (−) → Cytron POWER−                      [no pasa por el switch]
```
> Solo los **+** pasan por el switch; las tierras (−) son comunes y no se cortan.

## PolySwitch (RXEF300) — protección del riel lógico
- PPTC auto-reseteable: hold **3A**, trip **~6A**. No polarizado, en serie en el + lógico.
- **Por qué aquí:** ante un pico/corto transitorio en pista, corta y **se resetea solo**
  al enfriarse → el robot no queda muerto en la pista (a diferencia de un fusible que
  habría que cambiar a mano). Decisión: **auto-reset en lógica**, **fusible de vidrio
  (corte duro) en el motor** — cada protección en su sitio.

## Validación (prueba del único interruptor)
| Switch | Mini560 (Pi) | UBEC (servo) | Motor |
|---|---|---|---|
| **OFF** | 0V | 0V | no responde |
| **ON** | ~5V | ~6V | responde |
| **OFF** | 0V | 0V | no responde |

→ **Un solo interruptor enciende/apaga ambas baterías. Regla 9.10 cumplida.** ✅

## Estado: ÁRBOL DE POTENCIA COMPLETO
Los 3 rieles + el único switch DPST + PolySwitch (lógica) + fusible (motor),
todo montado y validado:
- Servo (UBEC 6V): 6.22V ✅
- Pi (Mini560 5V): 5.122V bajo carga, throttled 0x0 ✅
- Motor (Cytron): gira ambos sentidos, ~0.15A marcha, fusible 5A ✅
- Encendido único (DPST): corta/activa ambas baterías ✅

## Pendiente
- Actualizar BOM/README con el switch real (KCD4) antes del congelamiento del 2 jul.
- Montaje mecánico de la electrónica y del servo de dirección (LF-20MG) en el chasis.
