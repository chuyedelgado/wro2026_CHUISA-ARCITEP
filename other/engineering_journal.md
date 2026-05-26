# Engineering Journal — WRO 2026 Future Engineers
## Equipo CHUISA ARCITEP | Panamá | Temporada 2026

---

> **Propósito de este documento:**
> Este journal es la documentación viva del proceso de ingeniería del equipo CHUISA ARCITEP. Está estructurado para cumplir simultáneamente dos funciones:
>
> 1. **Registro cronológico** del proceso de diseño, decisiones e iteraciones
> 2. **Evidencia para los 5 criterios** de la rúbrica del Apéndice C (30 puntos)
>
> Cada decisión técnica documentada incluye: qué se decidió, qué alternativas se consideraron, los cálculos o razonamientos que respaldan la decisión, los resultados de pruebas cuando aplica, y las decisiones que se revisaron durante el proceso iterativo de selección.

---

## ÍNDICE

1. [Resumen del Proyecto](#resumen-del-proyecto)
2. [Estrategia: Dos Prototipos en Paralelo](#estrategia-dos-prototipos-en-paralelo)
3. [Metodología de Selección de Componentes](#metodología-de-selección-de-componentes)
4. [Registro Cronológico](#registro-cronológico)
5. [Decisiones de Hardware Documentadas](#decisiones-de-hardware-documentadas)
6. [Análisis por Criterio de la Rúbrica](#análisis-por-criterio-de-la-rúbrica)
7. [Registro de Pruebas](#registro-de-pruebas)
8. [Apéndices](#apéndices)

---

## RESUMEN DEL PROYECTO

| Campo | Información |
|-------|-------------|
| Nombre del equipo | CHUISA ARCITEP |
| Categoría | WRO 2026 Future Engineers — Self-Driving Cars |
| País / Ciudad | Panamá |
| Grupo de edad | 14-22 años |
| Integrantes | Jesus Delgado, Maria I. Acosta |
| Coach | Carlos Delgado |
| Repositorio GitHub | https://github.com/chuyedelgado/wro2026_CHUISA-ARCITEP |
| Competencia objetivo principal | Regional Panamá — Julio 2026 |
| Objetivo aspiracional | Clasificación a final internacional |
| Presupuesto final ejecutado | $1,075.68 USD |

**Stack tecnológico final (post-análisis iterativo y compras completadas):**

- **Chasis Prototipo 1:** WLtoys A959-B 1/18 RC car (Amazon, $123.91)
- **Chasis Prototipo 2:** Custom 3D printed Ackermann con CAD propio
- **Cerebro principal:** Raspberry Pi 5 (4GB RAM) — Python 3.11 + OpenCV
- **Microcontrolador:** Arduino Nano Every — C++
- **Cámara:** SainSmart Pi Camera Module 3, 152° Ultra Wide IMX708 con filtro IR
- **Servo de dirección:** Power HD ALIENTAC LF-20MG (20 kg·cm, 0.16s/60°, metal gear)
- **Motor de tracción:** JGB37-520 12V 530 RPM con encoder Hall (eBay)
- **Driver de motor:** Cytron MD10C single channel (10A continuo, 30A pico)
- **Sensores:** 2× ACEIRMC TOF400C VL53L1X + MPU-6050 + encoder Hall integrado
- **Alimentación:**
  - 2× LiPo 3S 11.1V 1500mAh (GOLDBAT 100C)
  - Mini560 Buck 5V/5A dedicado para Raspberry Pi
  - FEICHAO UBEC 5V/6V 8A configurado a 6V para servo
- **Protección:** PolySwitch RXEF300 (lógica) + fusible vidrio 8A (motor) + capacitores de desacoplo
- **Encendido:** Twidec DPST 12V 16A iluminado (cumple Regla 9.10)
- **Botón de inicio:** Arcade button 24mm con LED 5V (cumple Regla 9.11)

---

## ESTRATEGIA: DOS PROTOTIPOS EN PARALELO

### Decisión estratégica fundacional

Después de evaluar opciones de chasis para el proyecto, decidimos adoptar una **estrategia de desarrollo paralelo** con dos prototipos en lugar de comprometernos con uno solo. Esta es la decisión arquitectónica más importante del proyecto y afecta todo el cronograma, presupuesto y asignación de recursos del equipo.

### Las dos opciones que se descartaron

**Opción descartada A — Solo prototipo RC modificado:**
Ventajas: rápido, mecánica probada, bajo riesgo. Desventajas: limitaciones físicas en la documentación (no podemos justificar decisiones de diseño que no tomamos nosotros), menor puntuación esperada en Criterio 1 de la rúbrica (Movilidad y Diseño Mecánico).

**Opción descartada B — Solo prototipo custom 3D:**
Ventajas: máxima personalización, máximo puntaje potencial en documentación. Desventajas: con 6-8 semanas hasta la regional, el cronograma es ajustado para construir mecánica + electrónica + software de cero. Riesgo alto de llegar sin un vehículo funcional.

### La opción elegida: dos prototipos en paralelo

**Prototipo 1 — Base RC WLtoys A959-B 1/18 modificada:**
- **Propósito:** Plataforma de desarrollo de software desde la semana 1
- **Ventaja crítica:** Permite que el equipo desarrolle visión, máquina de estados, PID, comunicación UART en hardware real desde el día 1
- **Tiempo estimado a funcionar:** 1-2 semanas después de recibir hardware
- **Función secundaria:** Vehículo de backup en caso de falla del Prototipo 2

**Prototipo 2 — Chasis custom diseñado en CAD e impreso en 3D:**
- **Propósito:** Vehículo principal de competencia
- **Ventaja crítica:** Cada decisión de diseño es nuestra → maximiza puntuación en Criterios 1, 2 y 4 de la rúbrica
- **Tiempo estimado:** 4-6 semanas de diseño + impresión + ensamblaje + integración
- **Filosofía:** Cuando esté listo, trasplantamos la electrónica + código ya probados en Prototipo 1

### Trade-offs reconocidos de esta estrategia

| Trade-off | Cómo lo manejamos |
|-----------|-------------------|
| Costo extra de electrónica duplicada (~$150) | Justificado: permite trabajo en paralelo sin desmontar/remontar electrónica |
| Riesgo de que el equipo se "acomode" en el Prototipo 1 | Disciplina explícita: el Prototipo 1 NO se pule, NO se invierte tiempo extra en él |
| Cronograma agresivo | El código modular del repositorio funciona idénticamente en ambos prototipos |
| Mayor complejidad de gestión | Compensada con mejor cobertura de riesgos y mayor puntuación de documentación |

---

## METODOLOGÍA DE SELECCIÓN DE COMPONENTES

La selección de componentes para este proyecto se realizó usando una metodología iterativa específica que el equipo desarrolló:

### Proceso de 4 etapas

**Etapa 1 — Generación de hipótesis inicial:**
El líder del equipo genera una lista inicial de componentes con justificaciones técnicas basadas en el análisis del reto, los presupuestos de potencia, las restricciones de espacio, y las capacidades necesarias.

**Etapa 2 — Validación cruzada con múltiples sistemas de IA:**
La lista inicial se presenta de forma anónima (sin contexto compartido) a múltiples modelos de IA especializados para obtener segundas opiniones técnicas independientes. Esto evita el sesgo de confirmación de una sola fuente.

**Etapa 3 — Resolución de discrepancias:**
Cuando las recomendaciones difieren, se realiza análisis técnico adicional (cálculos de torque, RPM, corriente, etc.) para determinar la opción técnicamente superior.

**Etapa 4 — Verificación en plataformas de compra:**
Antes de comprar cualquier componente, se verifica el listado específico contra los criterios técnicos definidos (modelo, voltaje, RPM, FOV, pin XSHUT, etc.). Esta etapa identificó múltiples errores en componentes inicialmente seleccionados (ver Apéndice D).

### Resultado de la metodología

El proceso resultó en **24 decisiones revisadas y corregidas** antes de la compra final. Cada una documentada con la razón técnica del cambio. Esto es evidencia directa de proceso iterativo de ingeniería.

---

## REGISTRO CRONOLÓGICO

### Semana 1 — Mayo 23-30, 2026 | FUNDACIONES Y SELECCIÓN

#### Día 1 — Creación del repositorio (24 de mayo)

Creamos el repositorio público en GitHub. Primer commit realizado cumpliendo Regla 7.

Contenido del primer commit:
- Estructura completa de carpetas según template oficial WRO
- README.md inicial con secciones para los 5 criterios
- Esqueleto de código Python (1,116 líneas) y Arduino (328 líneas)
- Template del Engineering Journal

#### Días 2-7 — Análisis y compra de componentes (24-30 mayo)

Múltiples iteraciones de análisis técnico siguiendo la metodología descrita. Cada componente mayor pasó por el ciclo de 4 etapas, con varios componentes requiriendo 2-3 iteraciones para llegar a la decisión final.

**24 decisiones revisadas documentadas en Apéndice D.**

#### Hitos completados esta semana:
- [x] Repositorio GitHub público creado
- [x] Primer commit realizado (24 de mayo de 2026)
- [x] Estrategia de dos prototipos validada y documentada
- [x] Lista final de componentes consolidada después de 24 iteraciones
- [x] Engineering Journal v2 actualizado
- [x] **Componentes ordenados** (Amazon $850.48 + Pi Hut UK $129.40 + eBay $95.80 = $1,075.68)
- [x] Bill of Materials generado

### Semana 2 — Mayo 31 - Junio 6 | LLEGADA DE COMPONENTES Y SETUP

[A completar conforme avance]

### Semana 3 — Junio 7-13 | SETUP DE PROTOTIPO 1 + INICIO DE VISIÓN

[A completar]

### Semana 4 — Junio 14-20 | CAD CHASIS PROTOTIPO 2

[A completar]

### Semanas 5-8 | INTEGRACIÓN Y AFINAMIENTO

[Se completa según avanza]

---

## DECISIONES DE HARDWARE DOCUMENTADAS

### 4.1 Selección del Chasis

#### Prototipo 1 — WLtoys A959-B 1/18

**Decisión:** Usar el WLtoys A959-B 1/18 como base del Prototipo 1.

**Compra ejecutada:** Amazon US, $123.91 (incluye carro RTR completo con batería 7.4V 1400mAh, cargador balanceado, transmisor 2.4GHz y cross wrench).

**Alternativas evaluadas:**

| Opción | Pros | Contras | Veredicto |
|--------|------|---------|-----------|
| WLtoys 144001 (1/14) | Más espacio para electrónica, popular | Motor 540-class sobredimensionado, sin encoder | Descartado |
| **WLtoys A959-B (1/18)** | **Motor 390-class controlable, ~230×165mm cómodo** | Menos espacio interno | **✓ Elegido** |
| LaTrax Rally 1/18 | Calidad superior | $130-150 — costoso | Descartado |

**Razonamiento técnico:** El motor 540-class del WLtoys 144001 entrega ~35 km/h con LiPo 3S. Para WRO necesitamos ~2 m/s = 7.2 km/h. Operaríamos al 10-15% del throttle, donde los ESC tienen control granular pobre. El motor 390-class del A959-B opera en rango cómodo a estas velocidades.

**Nota sobre la compra:** Inicialmente consideramos eBay desde China (~$50-60), pero el tiempo de envío de 3-4 semanas era inaceptable. Pagar el premium de Amazon US fue la decisión correcta — delivery garantizado vs riesgo de quedar sin Prototipo 1.

#### Prototipo 2 — Chasis custom 3D printed

**Decisión:** Diseñar el chasis desde cero en Fusion 360 con geometría Ackermann custom.

**Dimensiones objetivo:**

| Parámetro | Valor objetivo | Justificación |
|-----------|---------------|---------------|
| Wheelbase | 140-160mm | Balance maniobrabilidad/estabilidad, ajustado para ruedas 65mm |
| Track width | 140-160mm | Margen sobre límite de 200mm |
| Footprint total | ≤200×280mm | Margen sobre límite WRO |
| Altura total | ≤180mm | Dentro del límite de 300mm con margen amplio |
| Centro de gravedad | Lo más bajo posible | Reduce transferencia de peso en curvas |

---

### 4.2 Sistema de Dirección — Servo

**Decisión final:** Power HD ALIENTAC LF-20MG (2 unidades, Amazon $49.98)

**Cálculo del torque requerido:**

Para el peor caso de fricción estática con ruedas ShareGoo 65×27mm:
- Masa total estimada: ~1,300g
- Distribución frontal: ~45% → 585g sobre eje delantero → 290g por rueda
- Coeficiente de fricción goma/tapete vinilo: μ ≈ 1.0
- Radio efectivo del par de scrub (ancho 27mm): ≈ 6mm

Par de scrub estático por rueda:
T = μ × N × r = 1.0 × 2.85 N × 0.006 m = 0.017 N·m ≈ 1.7 kg·cm

Para ambas ruedas con factor de seguridad 3×:
**Torque mínimo del servo requerido: ~10-12 kg·cm**

**Comparativa de alternativas:**

| Servo | Torque | Material | Velocidad | Precio | Veredicto |
|-------|--------|----------|-----------|--------|-----------|
| SG90 | 1.8 kg·cm | Plástico | 0.12s/60° | $3 | ❌ Demasiado débil |
| MG996R | 13 kg·cm | Metal + plástico interior | 0.17s/60° | $8 | ❌ Disco maestro plástico falla |
| DS3218MG | 20 kg·cm | Metal completo | 0.16s/60° | $15 | ⚠️ Selección inicial |
| **Power HD LF-20MG** | **20 kg·cm** | **Metal completo** | **0.16s/60°** | **$25** | **✓ Elegido** |

**Configuración eléctrica:** El LF-20MG se alimenta vía FEICHAO UBEC configurado a 6V. Puede demandar picos de ~2A bajo carga.

**Cantidad final:** 2 unidades (1 principal Prototipo 2 + 1 repuesto). Decidimos NO modificar el servo del Prototipo 1 ya que es solo plataforma de desarrollo desechable.

---

### 4.3 Sistema de Tracción — Motor

**Decisión final:** JGB37-520 12V 530 RPM con encoder Hall y bracket (2 unidades, eBay $95.80)

**Cálculo de RPM objetivo:**

Velocidad pico necesaria: 1.5-2 m/s para aceleración tras curvas.

Con rueda de 65mm (ShareGoo):
- Circunferencia: π × 0.065 = 0.204 m
- RPM en rueda a 2 m/s: 588 RPM

Considerando pérdidas (25% bajo carga + 8% por voltaje nominal 11.1V vs 12V spec):
**RPM no-load objetivo del motor (a 12V): 750-1000 RPM**

**Análisis de variantes disponibles del JGB37-520 en eBay:**

| Variante (RPM) | Vel. pico no-load | Vel. op 60% PWM | Veredicto |
|---|---|---|---|
| 178 RPM | 0.61 m/s | 0.36 m/s | ❌ Demasiado lento |
| 333 RPM | 1.13 m/s | 0.68 m/s | ⚠️ Marginal |
| **530 RPM** | **1.80 m/s** | **1.08 m/s** | **✓ Elegido** |
| 800 RPM | 2.72 m/s | 1.63 m/s | ⚠️ Difícil de controlar |
| 1000 RPM | 3.40 m/s | 2.04 m/s | ❌ Demasiado rápido |

**Por qué JGB37-520 sobre alternativas:**

| Alternativa | Pros | Contras |
|-------------|------|---------|
| Pololu 25D 12V 200RPM + encoder | Calidad superior | Top speed 0.68 m/s — insuficiente |
| Pololu 37D Premium HP 64CPR | Construcción superior | $45 vs $24 — no justificable |
| N20 micro gear motor | Pequeño | Torque insuficiente |
| Servo de rotación continua | Simple | Pierde encoder de calidad |

**Stall current del JGB37-520: ~2.5A** — esto determinó el dimensionamiento del driver Cytron MD10C.

**Cantidad final:** 2 unidades (1 principal + 1 repuesto crítico).

---

### 4.4 Sistema de Tracción Trasera — Live Axle vs Diferencial

**Decisión final:** Eje rígido (live axle) en v1.0 del Prototipo 2 con **mount modular** para upgrade futuro a diferencial.

**Trade-off analizado:**

Un diferencial permite que las ruedas traseras giren a diferentes velocidades en curva, eliminando el "scrub" (arrastre). Con ruedas 65×27mm relativamente anchas, el scrub es más pronunciado.

| Argumento | Análisis |
|-----------|----------|
| ¿El scrub afecta tiempo de ronda? | No significativamente |
| ¿El scrub afecta precisión de trayectoria? | Sí, pero compensable en software |
| ¿Equipos ganadores WRO usan diff? | Mayormente NO |
| ¿Tenemos tiempo para diseñar diff? | No con seguridad en 6-8 semanas |
| Trade-off de oportunidad | 1 semana CAD diff = 1 semana menos visión/control |

**Diseño previsor:** El mount del eje trasero se diseña con **interfaz modular** (4 tornillos M3 en patrón estándar) para permitir upgrade futuro a housing de diferencial sin rediseñar el chasis completo.

- v1.0 (Regional Panamá): Live axle, simple y robusto
- v2.0 (si clasificamos a internacional): Drop-in diferencial

---

### 4.5 Ruedas y Llantas

**Decisión final:** ShareGoo OD 65mm rubber tires con plastic wheel rims, hex 12mm (1 set de 4, Amazon $12.99)

**Especificaciones:**
- Diámetro exterior: 65mm
- Ancho: 27mm
- Hex hub: 12mm
- Material llanta: Goma con inserto de espuma
- Patrón: On-road racing/touring

**Por qué 65mm:**

| Diámetro | Pros | Contras |
|----------|------|---------|
| 50mm | CG más bajo | Más RPM motor para misma velocidad |
| **60-65mm** | **Sweet spot WRO** | — |
| 85mm+ | Mayor torque al piso | CG alto, scrub severo |

**Por qué racing sobre rally:**
Las llantas racing/touring están diseñadas para superficies lisas (tapete vinilo WRO). Las rally tienen tacos pronunciados que generan vibración y contacto inconsistente en superficie lisa.

**Sistema hex 12mm sobre alternativas:**
- Hex 12mm RC estándar: acoplamiento positivo, intercambiable, requiere adaptador 5→12mm
- Bore directo 5mm con set screw: el set screw deforma el eje y se afloja
- Adaptador custom impreso: menor consistencia, falla bajo torque

**Detalle de montaje:**
Las llantas vienen separadas de los rines y requieren pegado con super-glue líquido. Para esto compramos WOUSEDO super glue ($5.92) + MaxTite isopropyl alcohol ($7.95).

---

### 4.6 Rodamientos y Hardware Mecánico

#### Eje de 5mm — verificación de flexión

**Análisis:**
| Diámetro | Análisis |
|---|---|
| 3mm | Insuficiente rigidez |
| 4mm | Límite de rigidez |
| **5mm** | **Sweet spot** |
| 6mm+ | Sobredimensionado |

**Cálculo de flexión (acero 5mm, luz 40mm, carga lateral 5N):**

I = π·d⁴ / 64 = 30.7 mm⁴
δ = F·L³ / (48·E·I) = 0.001 mm

**Flexión despreciable. 5mm es ampliamente suficiente.**

#### Rodamientos MR105ZZ

**Componente:** KABOBEARING MR105ZZ 10pcs ($7.49)

Configuración: 2 por nudillo delantero + 2 por extremo del eje trasero = 10 totales (4 usados + 6 repuestos).

Sellado ZZ (metálico) sobre RS (goma): menor fricción rotacional, suficiente exclusión de polvo.

#### Bushings de kingpin SF-1 bronce

**Componente:** PRECISCRY SF-1 Composite Copper Bushing 3×5×6mm, 10pcs ($10.27)

En los pivotes de las ruedas delanteras usamos bushings de bronce sinterizado en lugar de rodamientos de bolas. Razón: los kingpins rotan a baja frecuencia (~Hz) con ángulo limitado (~±30°). Para esta aplicación, bushings son la elección de ingeniería correcta — más simples, más livianos, sin desgaste apreciable.

**Implicaciones CAD:**
- Diámetro interno del agujero: 5mm con tolerancia +0.05/-0.0mm (press fit ligero)
- Profundidad: Mínimo 6mm
- Pared mínima alrededor: 2.5mm de plástico

#### Acople motor-eje AOWEITAL Plum Coupling

**Componente:** AOWEITAL D25×L30 Plum Coupling 5mm to 6mm (2 unidades, $23.98)

Plum/Jaw coupling con elastómero de poliuretano. Bore 6mm (motor) → 5mm (eje trasero).

Beneficios sobre diaphragm coupling:
- Absorbe vibración del motor
- Tolera desalineamiento ligero (±0.1mm)
- Ideal para chasis 3D impreso con tolerancias ±0.2-0.3mm

#### Tornillería y consumibles

| Componente | Función |
|---|---|
| Fgruh 1760pcs M2/M3/M4/M5 Kit ($21.99) | Tornillería general |
| Loctite 243 Blue Threadlocker ($14.97) | Fijación de tornillos críticos |
| MOHERO Hex Hubs 5→12mm 4pcs ($10.99) | Adaptador eje 5mm a wheel hex 12mm |
| YijiaLink Servo Horns 25T Aluminio ($8.99) | Brazos del servo en aluminio |
| Mriuuod M3×150mm Threaded Rod 10pcs ($7.69) | Tie rods de dirección |
| ShareGoo M3 Ball Joints 10pcs ($11.89) | Articulaciones de tie rods, bola metal |
| uxcell Shaft Lock Collars 5mm 10pcs ($9.79) | Fijación axial en eje |
| MECCANIXITY Stainless Rods 5×300mm 6pcs ($12.39) | Ejes traseros y delanteros |

---

### 4.7 Arquitectura de Cómputo

**Decisión:** Arquitectura distribuida con dos controladores:
- **Raspberry Pi 5 (4GB):** Cerebro principal (visión, lógica, estado)
- **Arduino Nano Every:** Microcontrolador de bajo nivel (sensores, PWM, interrupciones)

**Comunicación:** UART a 115,200 baud entre ambos.

**Hardware comprado:**
- Raspberry Pi 5 (4GB) + PSU 27W + cable Micro-HDMI (bundle Pi Hut UK, $129.40)
- Arduino Nano Every 3-pack (Amazon, $38.00)
- Pi 5 Active Cooler oficial ($9.99)
- ARCTIC MX-4 thermal paste ($5.49)
- SanDisk Ultra 32GB MicroSD Class 10 ($20.33)
- SMALLRIG Micro-HDMI 35cm cable backup ($7.99)

#### Por qué no Pi 5 sola

Python no garantiza tiempos de respuesta de microsegundos para interrupciones del encoder. Pérdida de pulsos cuando OpenCV consume CPU.

**Solución:** Arduino maneja interrupciones time-critical (encoder, botón) en hardware con jitter sub-microsegundo. Pi se enfoca en procesamiento de imagen y decisiones de alto nivel.

#### Refrigeración crítica

La Pi 5 corriendo OpenCV alcanza 80-85°C → throttling. El Active Cooler oficial mantiene <60°C bajo carga continua. Inversión de $10 que previene pérdida de FPS durante competencia.

---

### 4.8 Arquitectura de Potencia

#### Dos baterías LiPo separadas

**Componente:** GOLDBAT 1500mAh 3S 11.1V 100C 2-pack ($23.99)

**Razón:** Aislar el ruido eléctrico del motor de los circuitos de lógica.

```
Batería A (3S 11.1V 1500mAh)              Batería B (3S 11.1V 1500mAh)
        │                                          │
    [Switch DPST 12V 16A iluminado] ←─── Corta ambas (Regla 9.10)
        │                                          │
    [PolySwitch 3A hold]                  [Fusible vidrio 8A]
        │                                          │
  [Mini560 5V/5A]      [FEICHAO UBEC 6V/8A]   [Cytron MD10C]
        │                       │                  │
   [Raspberry Pi 5]        [Power HD LF-20MG]   [Motor JGB37-520]

       [Arduino Nano Every — alimentado vía 5V del bus de la Pi]
       [VL53L1X × 2, MPU-6050 — alimentados vía 3.3V del Arduino]
```

#### BECs separados para Pi y servo (decisión crítica)

**Error inicial corregido:** En la primera iteración propusimos un solo BEC compartido. Imposible servir Pi (5V exactos, max 5.5V) y servo (6-7V para torque nominal) con un BEC.

**Solución:**

| Carga | BEC dedicado | Voltaje | Corriente | Componente |
|-------|--------------|---------|-----------|------------|
| Raspberry Pi 5 | Mini560 Step-Down | 5.0V regulado (fijo) | 5A continuo | DORHEA 10-pack ($12.99) |
| Servo Power HD LF-20MG | FEICHAO UBEC | 6.0V regulado | 8A pico | 2 unidades ($37.96) |

**Por qué Mini560 fijo sobre regulador ajustable:**
- Reguladores ajustables tienen potenciómetro que puede descalibrarse por vibración
- Pi 5 muere instantáneamente si recibe >5.5V
- $4 de diferencia no compensan riesgo de quemar Pi 5 ($75)
- 10 unidades por $12.99 vs 3 unidades Pololu por $89.85 — mejor precio + más repuestos

#### Capacitores correctamente dimensionados

**Componentes:**
- BOJACK 0.1μF Ceramic 50pcs ($6.99) — desacoplo HF
- Rubycon 100μF/16V 15pcs ($5.99) — desacoplo medio
- Rubycon 470μF/16V 15pcs ($5.99) — desacoplo bulk

**Cálculo (escenario hipotético si compartieran rail):**
ΔV permitida = 0.25V
Pico motor: 5A × 20ms = 100mC
C = 100mC / 0.25V = **400,000 μF** (absurdo)

**Conclusión:** Solo aplica si compartieran rail. Con baterías aisladas solo necesitamos desacoplo local:
- 2× 470μF/16V en rail 5V Arduino
- 1× 100μF/16V cerca de cada VL53L1X
- 20× 0.1μF cerámico (uno por cada IC)

#### Diodo Schottky eliminado

**Propuesta inicial:** Diodo Schottky 1N5822 para protección polaridad inversa.

**Análisis posterior:** Pi se alimenta por USB-C (protección integrada), BECs son regulados (protección interna), Cytron tiene diodos integrados, baterías no conectan directo a Pi, XT60 es físicamente irreversible.

**Conclusión:** Diodo introduce caída de 0.4V (8% del rail 5V) sin función útil. **Eliminado.**

---

### 4.9 Sistema de Encendido y Arranque

#### Switch DPST (Regla 9.10)

**Componente:** Twidec DPST 12V 16A Rocker Switch Illuminated 2-pack ($8.99)

**Por qué DPST sobre SPST:**

| Topología | Análisis |
|---|---|
| SPST cortando solo lógica | Pi cae, pero motor queda armado (riesgo en transporte) |
| **DPST cortando ambas baterías** | **Apaga todo, satisface la regla** |
| XT60 desconectable | Solución RC estándar, puede no satisfacer al juez |

**Por qué panel mount sobre inline:**
- Factor de forma más profesional
- Switch integrado en chasis vs cables colgando
- Más fácil identificar para jueces
- Mejor resistencia mecánica

#### Botón de inicio (Regla 9.11)

**Componente:** EG STARTS Arcade Button 24mm LED 5V 5pcs ($11.99)

**Detalle crítico:** Arcade buttons por defecto traen LEDs de 12V. Buscamos específicamente **LED 5V** para alimentar desde pin GPIO del Arduino con resistor 220Ω.

**Función dual del LED:** Indicador visual al juez del estado del sistema. Detalle de UX evaluado positivamente.

---

### 4.10 Sistema de Protección Eléctrica

**Error inicial corregido:** Inicialmente propusimos fusibles automotrices ATO 5A/10A.

**Problema:** Curva de fusión ATO es muy lenta (diseñada para shorts de 100+ A en alternador de auto). Un short en nuestro robot dando 8-10A puede no abrir un ATO de 10A nunca.

**Solución correcta:**

| Aplicación | Componente | Compra | Por qué |
|------------|------------|--------|---------|
| Rail lógica | PolySwitch RXEF300 (3A hold) | 10-pack $7.53 | Auto-resetable, trip rápido en sobrecarga |
| Rail motor | Fusible vidrio 5×20mm 8A fast-blow + portafusible | BOJACK kit $11.99 | Curva rápida apropiada |

**Costo:** $19.52 vs $30+ ATO. Más liviano, más apropiado técnicamente, auto-resetable en desarrollo.

---

### 4.11 Selección de Sensores

#### Cámara SainSmart 152° Ultra Wide

**Componente:** SainSmart Camera Module 3, 12MP IMX708, 152° (D) Ultra Wide ($44.99)

**Especificaciones:**
- Sensor IMX708 12MP (idéntico al oficial Raspberry Pi)
- FOV: **152° diagonal**
- Filtro IR integrado (crítico para HSV preciso)
- Autofocus por detección de fase
- HDR mode hasta 3MP
- Compatible con Pi 5 (incluye cable correcto)

**Por qué 152° sobre 75° o 120°:**

| FOV | Análisis | Veredicto |
|-----|----------|-----------|
| 75° estándar | Detecta pilares muy tarde | ❌ |
| 120° Wide | Buen balance | ⚠️ Aceptable |
| **152° Ultra Wide** | **Detección temprana, mejor en esquinas** | **✓** |

**Trade-off:** El FOV 152° introduce distorsión de barril, compensable con calibración OpenCV (`cv2.calibrateCamera()` + `cv2.undistort()`). ~30 min de calibración + ~5ms por frame.

**Decisiones revisadas durante la selección:**
1. Pi Camera Module 3 estándar SC0872 (75°) — Rechazada
2. Pi Camera Module 3 NoIR Wide SC0875 — Rechazada (NoIR distorsiona HSV)
3. Arducam 120° con filtro IR — Aceptable pero descartada
4. **SainSmart 152° Ultra Wide con filtro IR — Elegida**

#### Sensores ToF: 2× ACEIRMC TOF400C VL53L1X

**Componente:** ACEIRMC TOF400C VL53L1X 4-pack ($21.89)

**Por qué ToF sobre alternativas:**

| Sensor | Precisión | Velocidad | Veredicto |
|--------|-----------|-----------|-----------|
| HC-SR04 ultrasónico | ±30mm | 60ms/lectura | ❌ Oscilaciones a 0.45 m/s |
| **VL53L1X ToF** | **±1mm** | **20ms/lectura** | **✓** |
| Sharp IR | ±10mm | Variable | Ruido del sensor, no lineal |

**Configuración:** 2 unidades en esquinas frontales, modo "short" (40-1300mm).

**Asignación I2C:** VL53L1X comparten dirección por defecto (0x29). Asignamos direcciones únicas usando pines SHUT (verificado visualmente en breakout — 6 pines incluyendo SHUT).

**Por qué ACEIRMC sobre SparkFun:**

| Marca | Precio (4 unidades) | Delivery |
|---|---|---|
| SparkFun VL53L1X | $114 | Jun 15-25 |
| **ACEIRMC TOF400C** | **$21.89** | **Jun 1** |

Mismo chip ST Microelectronics. ACEIRMC: $35 más barato, delivery 2 semanas más rápido, más repuestos. 4 unidades = 2 usadas + 2 repuestos.

#### IMU MPU-6050

**Componente:** HiLetgo GY-521 MPU-6050 3-pack ($11.79)

**Función:** Giroscopio eje Z para medir yaw (heading). Uso principal: detección de giros de 90° → conteo de secciones.

**Aislamiento físico:** Montaje sobre foam EVA 3mm (MEARCOOH $9.96) para aislar de vibraciones del motor.

**Cantidad:** 3 unidades (1 por prototipo + 1 repuesto).

---

## ANÁLISIS POR CRITERIO DE LA RÚBRICA

### Criterio 1: Movilidad y Diseño Mecánico

**Decisiones documentadas:**
- Chasis: dos prototipos, WLtoys A959-B vs custom 3D (4.1)
- Servo: Power HD LF-20MG con cálculo torque (4.2)
- Motor: JGB37-520 530 RPM con cálculo RPM (4.3)
- Live axle vs diferencial (4.4)
- Ruedas 65mm racing (4.5)
- Hardware mecánico (4.6): eje 5mm, MR105ZZ, SF-1 bronce, plum coupling

**Evidencia de iteración:** 24 cambios documentados en Apéndice D.

### Criterio 2: Arquitectura de Potencia y Sensores

**Decisiones documentadas:**
- Potencia (4.8): dos baterías, dual BEC dedicado, capacitores correctos
- Protección (4.10): PolySwitch + fusible vidrio
- Diodo Schottky eliminado (over-engineering identificado)
- Sensores (4.11): ToF sobre ultrasónico, IMU aislado, cámara 152° Wide

**Presupuesto de potencia:** Tabla detallada en Apéndice B.

### Criterio 3: Arquitectura de Software

**Implementación inicial en repositorio:**
- Arquitectura modular: 6 módulos Python + sketch Arduino
- FSM con 7 estados documentados
- PID reutilizables (wall-following + pillar avoidance)
- Protocolo UART definido

**Por desarrollar:**
- Calibración OpenCV para corrección distorsión cámara 152°
- Algoritmo HSV con valores calibrados
- Lógica evasión pilares (offset por color)
- Estacionamiento paralelo
- Métricas de pruebas

### Criterio 4: Pensamiento Sistémico

**Evidencia:**

1. Estrategia dos prototipos — gestión riesgo a nivel proyecto
2. Mount modular eje trasero — diseño para evolución (v1 → v2)
3. Aislamiento baterías — comprensión ruido eléctrico motor
4. Sensores ToF + IMU separados — sensor correcto para cada problema
5. Arquitectura Pi + Arduino — comprensión limitaciones Python tiempo real
6. Metodología iterativa con IA múltiple — proceso documentado y replicable

**Trade-offs documentados:** Cada decisión en sección 4 incluye tabla comparativa. 24 decisiones revisadas en Apéndice D.

### Criterio 5: Reproducibilidad y Calidad del Repositorio

**Estado del repositorio:**
- Estructura completa según template oficial WRO
- README.md de 24,442+ caracteres (>5,000 requerido)
- Código: 1,116+ líneas Python + 328+ líneas Arduino
- Documentación instalación paso a paso
- Bill of Materials completo con sources y precios

**Compromiso:**
- Público desde creación (24 mayo 2026)
- Permanecerá público ≥12 meses post-competencia
- Commits con mensajes significativos

---

## REGISTRO DE PRUEBAS

*(Esta sección se completa a medida que se ejecutan las pruebas)*

### Pruebas de chasis

#### Prototipo 1 — WLtoys A959-B
| Fecha | Prueba | Resultado | Notas |
|-------|--------|-----------|-------|
| [FECHA] | Movimiento básico con comandos manuales | [PENDIENTE] | |
| [FECHA] | Velocidad máxima medida | [PENDIENTE] | |

#### Prototipo 2 — Custom 3D
| Fecha | Prueba | Resultado | Notas |
|-------|--------|-----------|-------|
| [FECHA] | Movimiento básico | [PENDIENTE] | |

### Pruebas de visión
| Fecha | Condición luz | Detección rojo | Detección verde | Detección líneas | Notas |
|-------|---------------|----------------|-----------------|-------------------|-------|
| [FECHA] | Natural día | [%] | [%] | [%] | |
| [FECHA] | Artificial fluorescente | [%] | [%] | [%] | |

### Tuning de PID
| Versión | Kp | Ki | Kd | Tasa éxito 3 vueltas | Notas |
|---------|----|----|----|--------------------|-------|
| v1.0 | [TBD] | [TBD] | [TBD] | [%] | |

### Pruebas Open Challenge
| Fecha | Pista (ancho) | Dirección | Intentos | 3 vueltas OK | Tiempo prom | Notas |
|-------|--------------|-----------|----------|--------------|-------------|-------|
| [FECHA] | [mm] | CW/CCW | [N] | [X/N] | [s] | |

### Pruebas Obstacle Challenge
| Fecha | Config. pilares | Intentos | 3 vueltas OK | Sin mover señales | Parking OK | Notas |
|-------|----------------|----------|--------------|-------------------|------------|-------|
| [FECHA] | [DESCRIBE] | [N] | [X/N] | [X/N] | [X/N] | |

---

## APÉNDICES

### Apéndice A: Lista completa de componentes comprados

Ver documento dedicado: `bill_of_materials.md` (en `/other/`).

**Resumen ejecutivo:**
- **Amazon US:** 51 items, $850.48 — Pago realizado, entrega Jun 1-16
- **Pi Hut UK:** 3 items (Pi 5 bundle), $129.40 — Pago realizado
- **eBay (WHCD01):** 2 motores JGB37-520, $95.80 — Pago realizado
- **TOTAL EJECUTADO:** $1,075.68 USD

### Apéndice B: Cálculos técnicos clave

**B.1 Torque servo:** Mínimo 10-12 kg·cm (ruedas 65×27mm), seleccionado 20 kg·cm (margen 2×).

**B.2 RPM motor:** Objetivo 750-1000 no-load, seleccionado 530 RPM (1.8 m/s pico, 1.08 m/s operación 60% PWM).

**B.3 Flexión eje:** Eje 5mm con flexión 0.001mm bajo carga típica — despreciable.

**B.4 Capacitores:** 400,000μF teóricos si compartieran rail, pero con baterías aisladas solo desacoplo local (~1,000μF).

**B.5 Presupuesto de potencia:**

| Subsistema | Corriente promedio | Corriente pico | Fuente |
|---|---|---|---|
| Raspberry Pi 5 (idle) | 0.6A | 1.2A | Batería A → Mini560 5V |
| Raspberry Pi 5 (OpenCV) | 1.2A | 2.0A | Batería A → Mini560 5V |
| Pi Camera | 0.25A | 0.3A | Bus 5V Pi |
| Arduino Nano Every | 0.05A | 0.1A | Bus 5V Pi |
| 2× VL53L1X | 0.04A | 0.08A | Bus 3.3V Arduino |
| MPU-6050 | 0.005A | 0.01A | Bus 3.3V Arduino |
| Servo LF-20MG | 0.1A | 2.0A | Batería B → FEICHAO 6V |
| Motor JGB37-520 | 1.5A | 5.0A | Batería B directo |
| **TOTAL Batería A** | **~1.5A** | **~2.5A** | LiPo 1500mAh = ~60 min |
| **TOTAL Batería B** | **~1.6A** | **~7.0A** | LiPo 1500mAh = ~55 min |

### Apéndice C: Cumplimiento de Reglas WRO

| Regla | Requisito | Cumplimiento |
|---|---|---|
| Regla 7 | Primer commit ≥2 meses antes de competencia | ✅ 24 mayo 2026 |
| Regla 7 | README.md ≥5,000 caracteres | ✅ 24,442+ caracteres |
| Regla 7 | Carpetas requeridas | ✅ Estructura completa |
| Regla 9.8 | Dimensiones ≤300×200×300mm | ✅ Diseño objetivo 280×200×180mm |
| Regla 9.10 | Un interruptor de encendido | ✅ DPST Twidec corta ambas baterías |
| Regla 9.11 | Un botón de inicio | ✅ Arcade button con LED |
| Regla 9.X | Sin dispositivos comerciales propietarios | ✅ Solo componentes COTS estándar |

### Apéndice D: Decisiones revisadas durante el análisis

Lista exhaustiva de 24 decisiones iniciales que cambiamos tras análisis técnico adicional. Evidencia del proceso iterativo de ingeniería:

| # | Decisión inicial | Decisión final | Razón del cambio |
|---|-----------------|----------------|------------------|
| 1 | Chasis WLtoys 144001 | WLtoys A959-B | Motor 144001 sobredimensionado |
| 2 | Servo DS3218MG | Power HD LF-20MG | Calidad superior, mejor documentación |
| 3 | Motor Pololu 25D 200RPM | JGB37-520 12V 530 RPM | Pololu insuficiente (0.68 m/s vs 2 m/s) |
| 4 | Driver TB6612FNG | Cytron MD10C | TB6612 entra en protección térmica con stall JGB37 |
| 5 | BEC único compartido | Dual BEC (Mini560 + FEICHAO) | Imposible servir Pi (5V) y servo (6-7V) con un BEC |
| 6 | Fusibles ATO automotrices | PolySwitch + fusible vidrio | Curva ATO demasiado lenta |
| 7 | Banco 5× 1000μF | Desacoplo local específico | Cálculo mostró banco inadecuado |
| 8 | Diodo Schottky 1N5822 | Eliminado | Caída innecesaria, sin función protectora real |
| 9 | Pi Camera Module 3 estándar 75° | SainSmart 152° Ultra Wide | FOV insuficiente |
| 10 | Pi Camera Module 3 NoIR Wide | Versión con filtro IR | NoIR rompe pipeline HSV |
| 11 | Arducam 120° | SainSmart 152° | Mayor FOV, mejor rating, mismo precio |
| 12 | SparkFun VL53L1X 2-pack | ACEIRMC TOF400C 4-pack | $35 más barato, delivery 2 sem más rápido |
| 13 | Switch SPST | Switch DPST | SPST no cumple Regla 9.10 estrictamente |
| 14 | Switch DPST inline | Switch DPST panel mount | Más profesional, más visible |
| 15 | Ruedas hobbysoul 130mm | ShareGoo 65mm | "60mm" original era ancho, no diámetro |
| 16 | Ruedas patrón Rally | Ruedas patrón Racing | Racing óptimo para tapete liso WRO |
| 17 | Acople Sinoblu diaphragm | AOWEITAL Plum/Jaw | Plum absorbe vibración, tolera desalineamiento |
| 18 | Pololu D24V50F5 (3 × $30) | Mini560 (10 × $1.30) | Misma función, mejor precio, más repuestos |
| 19 | 3 servos LF-20MG | 2 servos LF-20MG | No modificar servo Prototipo 1 (desechable) |
| 20 | Hose Clamps Qibaok | Eliminado | Sin aplicación clara |
| 21 | WLtoys A979-B Monster Truck | WLtoys A959-B Buggy | A979 tiene CG alto y geometría inadecuada |
| 22 | A959-B desde eBay China | A959-B desde Amazon US | Delivery garantizado vs riesgo 3-4 semanas |
| 23 | JGB37-520 con CCM6N PWM bundle | JGB37-520 con encoder Hall | Bundle no tenía encoder |
| 24 | JGB37-520 12V176 (176 RPM) | JGB37-520 12V530 (530 RPM) | 176 RPM da solo 0.6 m/s |

**Total: 24 decisiones reversadas o refinadas durante el proceso iterativo.**

---

*Documento mantenido por: Equipo CHUISA ARCITEP*
*Última actualización: 25 de mayo de 2026 — Post compras completadas*
*Repositorio: https://github.com/chuyedelgado/wro2026_CHUISA-ARCITEP*
