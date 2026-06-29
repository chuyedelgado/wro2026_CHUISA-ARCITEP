# Journal 2026-06-28 — Placa de sensores I2C (perfboard) VALIDADA ✅

## Objetivo
Migrar el **bus de sensores I2C** de protoboard a una **PCB perforada permanente**
(primera placa perforada del equipo) y validarla. Motivo: las conexiones de protoboard
se **aflojan con la vibración** → fallos intermitentes en pista. La versión soldada es
firme y montable.

## Diseño: hub del bus I2C
- Perfboard **4×6 cm**. Conectores: **headers hembra (zócalos)** — fáciles de soldar y
  desmontables. *(Opcional a futuro: endurecer a JST-XH para el robot.)*
- **4 rieles compartidos** (VCC, GND, SDA, SCL) + **4 conectores** (ToF1, ToF2, MPU,
  Arduino) + **2 líneas XSHUT** punto a punto.
- Headers **verticales** → los pines quedan alineados en filas horizontales = los rieles.

## Pinouts usados (módulos reales)
- **ToF VL53L1X:** VIN, GND, SDA, SCL, **SHUT (XSHUT)**. INT no se usa.
- **MPU-6050 (GY-521 / HW-123):** VCC, GND, **SCL, SDA** (orden invertido vs ToF),
  **AD0 → GND** (puente en el módulo) para fijar la dirección **0x68**.

## Corrección de pines (importante)
Los XSHUT estaban en **D2/D3** en el protoboard, pero **el motor ahora usa D2 (DIR) y
D3 (PWM)** → se **mudaron a D7/D8**. Firmware actualizado.

## Mapa de conexión (placa → Arduino)
| Placa | Arduino |
|---|---|
| VCC | 5V |
| GND | GND |
| SDA | A4 |
| SCL | A5 |
| XSHUT1 (ToF1) | **D7** |
| XSHUT2 (ToF2) | **D8** |

## Método de armado (notas de técnica)
- **Rieles:** alambre **sólido** (patitas de resistencia) acostado a lo largo de cada
  fila, soldado a las 4 gotas. Desnudo (todos los pines de la fila comparten señal).
- **XSHUT:** cable **aislado** (solo extremos pelados), soldado punto a punto
  (ToF → Arduino), ruteado por la zona vacía para no tocar los pines del medio.
- Cada etapa verificada con **continuidad** antes de seguir.

## Validación
1. **Continuidad:** cada riel conduce de extremo a extremo; los 4 rieles **aislados
   entre sí**; cada XSHUT conecta sus dos extremos y está aislado de los rieles y
   entre sí. ✅
2. **Escáner I2C:** detectó los **3 dispositivos**:
   - `0x29` — ToF (dirección base)
   - `0x2A` — ToF (re-direccionado vía XSHUT)
   - `0x68` — MPU-6050
   → **Total: 3.** ✅

## Estado
**Placa de sensores I2C COMPLETA y validada.** Primer subsistema migrado de protoboard
a circuito permanente.

## Pendiente
- Validación actual = banco (jumpers Dupont temporales). Cables finales a la medida tras
  el **montaje mecánico**: ToF en los bordes mirando afuera (altura de muro), MPU sobre
  **foam EVA** lejos del motor (EMI/vibración).
- Siguiente migración: **placa de distribución de potencia** (perfboard 7×9).
