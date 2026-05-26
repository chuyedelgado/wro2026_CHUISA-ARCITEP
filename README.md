# WRO 2026 Future Engineers — Equipo CHUISA ARCITEP

> Documentación del trabajo desarrollado por el equipo **CHUISA ARCITEP** (Panamá) para la categoría **Future Engineers** de la World Robot Olympiad temporada 2026.

[![Status](https://img.shields.io/badge/status-Active%20Development-green)]()
[![Phase](https://img.shields.io/badge/phase-Hardware%20Ordered-blue)]()
[![Country](https://img.shields.io/badge/country-Panama-red)]()
[![Competition](https://img.shields.io/badge/competition-July%202026-orange)]()

---

## 📋 Estado actual del proyecto

| Hito | Estado | Fecha |
|------|--------|-------|
| Estructura de repositorio | ✅ Completado | 24 mayo 2026 |
| Estrategia validada (dos prototipos) | ✅ Completado | 24 mayo 2026 |
| Selección de componentes (24 iteraciones) | ✅ Completado | 25 mayo 2026 |
| Compra de hardware ($1,075.68) | ✅ Completado | 25 mayo 2026 |
| Engineering Journal v2 | ✅ Completado | 25 mayo 2026 |
| Bill of Materials | ✅ Completado | 25 mayo 2026 |
| Llegada de hardware | 🔄 En tránsito | Jun 1-25, 2026 |
| Setup Prototipo 1 | ⏳ Pendiente | Jun 5-12, 2026 |
| Desarrollo software visión | ⏳ Pendiente | Jun 7-20, 2026 |
| CAD chasis Prototipo 2 | ⏳ Pendiente | Jun 10-25, 2026 |
| Integración final | ⏳ Pendiente | Jul 1-10, 2026 |
| Regional Panamá | 🎯 Objetivo | Jul 2026 |

---

## 🎯 Visión del proyecto

CHUISA ARCITEP desarrolla un vehículo autónomo de auto-conducción para la categoría Future Engineers de WRO 2026. Nuestra estrategia adopta un enfoque de **dos prototipos paralelos**:

1. **Prototipo 1 (Plataforma de desarrollo):** WLtoys A959-B 1/18 modificado para validar software desde el día 1
2. **Prototipo 2 (Vehículo de competencia):** Chasis custom diseñado en CAD e impreso en 3D para maximizar puntuación en criterios de rúbrica

Esta estrategia balancea velocidad de desarrollo, gestión de riesgos, y calidad del producto final.

---

## 🏗️ Arquitectura del sistema

### Hardware

```
┌─────────────────────────────────────────────────────────────┐
│  Raspberry Pi 5 (4GB) — Cerebro principal                  │
│  - Python 3.11 + OpenCV                                    │
│  - Cámara SainSmart 152° Ultra Wide (IMX708 con filtro IR) │
│  - Procesamiento de visión (HSV) + lógica FSM              │
└─────────────────────────────────────────────────────────────┘
                            ↕ UART 115200 baud
┌─────────────────────────────────────────────────────────────┐
│  Arduino Nano Every — MCU bajo nivel                       │
│  - 2× VL53L1X ToF (distancia lateral)                      │
│  - MPU-6050 IMU (yaw)                                      │
│  - Encoder Hall (motor JGB37-520 530 RPM)                  │
│  - PWM servo + motor                                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Actuadores                                                │
│  - Servo Power HD LF-20MG (20kg·cm)                        │
│  - Motor JGB37-520 12V 530 RPM con encoder Hall            │
│  - Driver Cytron MD10C (10A continuo)                      │
└─────────────────────────────────────────────────────────────┘
```

### Arquitectura de potencia

```
2× LiPo 3S 11.1V 1500mAh (aisladas para reducir ruido)
       ↓
Switch DPST 12V 16A iluminado (corta ambas — Regla 9.10)
       ↓
┌──────────────────┬─────────────────┬──────────────────┐
│  Batería A       │  Batería A      │  Batería B       │
│  PolySwitch 3A   │  PolySwitch 3A  │  Fusible vidrio 8A│
│  Mini560 5V/5A   │  FEICHAO 6V/8A  │  Cytron MD10C    │
│  → Raspberry Pi  │  → Servo        │  → Motor         │
└──────────────────┴─────────────────┴──────────────────┘
```

---

## 📂 Estructura del repositorio

```
wro2026_CHUISA-ARCITEP/
├── README.md                       ← Este archivo
├── models/                         ← Archivos CAD del chasis (futuro)
├── other/                          ← Documentación adicional
│   ├── engineering_journal.md      ← Diario de ingeniería detallado
│   ├── bill_of_materials.md        ← Lista completa de componentes
│   └── WRO2026_CHUISA-ARCITEP_Lista_Componentes.pdf
├── schemes/                        ← Diagramas eléctricos (futuro)
├── src/                            ← Código fuente
│   ├── arduino/
│   │   └── main/
│   │       └── main.ino            ← Sketch Arduino (sensores + actuadores)
│   └── raspberry_pi/
│       ├── main.py                 ← Entry point
│       ├── vision.py               ← Pipeline OpenCV
│       ├── state_machine.py        ← FSM principal
│       ├── pid_controller.py       ← Controladores PID
│       ├── uart_comm.py            ← Comunicación con Arduino
│       └── config.py               ← Configuración global
├── t-photos/                       ← Fotos del equipo
├── v-photos/                       ← Fotos del vehículo (futuro)
└── video/
    └── video.md                    ← Enlace al video oficial (futuro)
```

---

## 🔑 Decisiones clave de ingeniería

Documentamos 24 decisiones revisadas durante el proceso de selección iterativa de componentes. Todas se encuentran detalladas en el [Engineering Journal](other/engineering_journal.md).

**Resumen ejecutivo de decisiones clave:**

- **Estrategia:** Dos prototipos en paralelo (no uno solo)
- **Cámara:** 152° Ultra Wide (no 75° estándar) — máximo FOV
- **Motor:** JGB37-520 530 RPM con encoder Hall (no Pololu 25D — insuficiente velocidad)
- **Driver:** Cytron MD10C (no TB6612FNG — protección térmica)
- **Power:** Dual BEC dedicado (no compartido — imposible servir Pi 5V y servo 6V)
- **Protección:** PolySwitch + fusible vidrio (no ATO — curva muy lenta)
- **Sensores:** ACEIRMC TOF400C (no SparkFun — mismo chip, mejor precio y delivery)

---

## 📊 Cumplimiento de Rúbrica del Apéndice C

| Criterio | Puntos | Cómo lo cubrimos |
|----------|--------|------------------|
| **1. Movilidad y Diseño Mecánico** | 6 | Chasis custom 3D + cálculos de torque/RPM documentados |
| **2. Arquitectura de Potencia y Sensores** | 6 | Diagramas eléctricos + análisis dual-BEC + sensores ToF |
| **3. Software y Estrategia de Obstáculos** | 6 | Arquitectura modular Python + Arduino + FSM documentada |
| **4. Pensamiento Sistémico** | 6 | 24 decisiones de ingeniería documentadas con trade-offs |
| **5. Reproducibilidad del Repositorio** | 6 | Estructura completa + BOM + cálculos + código compilable |
| **TOTAL** | **30** | |

---

## 💻 Stack de software

**Raspberry Pi 5:**
- Raspberry Pi OS (Bookworm 64-bit)
- Python 3.11
- OpenCV 4.x (procesamiento de visión)
- picamera2 (acceso cámara)
- pyserial (UART)
- libcamera (stack oficial de cámara)

**Arduino Nano Every:**
- Arduino IDE 2.x
- C++ con framework Arduino
- Librerías: Wire (I2C), Servo, VL53L1X (Pololu), MPU6050 (Electronic Cats)

---

## 🛠️ Cómo reproducir este proyecto

### Hardware requerido

Ver lista completa en [bill_of_materials.md](other/bill_of_materials.md). Inversión total ~$1,075 USD.

### Setup de software

#### Raspberry Pi 5

```bash
# 1. Flashear Raspberry Pi OS 64-bit en MicroSD usando Raspberry Pi Imager
# 2. Boot y configuración inicial
sudo apt update && sudo apt upgrade -y

# 3. Habilitar interfaces requeridas
sudo raspi-config
# Habilitar: I2C, SPI, Camera, Serial

# 4. Instalar dependencias
sudo apt install -y python3-pip python3-opencv python3-picamera2
pip3 install pyserial numpy

# 5. Clonar repositorio
git clone https://github.com/chuyedelgado/wro2026_CHUISA-ARCITEP.git
cd wro2026_CHUISA-ARCITEP

# 6. Ejecutar
cd src/raspberry_pi
python3 main.py
```

#### Arduino Nano Every

1. Abrir `src/arduino/main/main.ino` en Arduino IDE
2. Instalar librerías requeridas (Wire, Servo, VL53L1X, MPU6050)
3. Seleccionar board: Arduino Nano Every
4. Compilar y subir

---

## 👥 Equipo

| Rol | Nombre |
|-----|--------|
| Líder | Jesús Delgado |
| Miembro | [Nombre 2] |
| Miembro | [Nombre 3] |
| Coach | [Nombre del coach] |

---

## 📅 Cronograma del proyecto

```
Semana 1 (May 24-30) ✅  Estructura repo + Estrategia + Selección + Compras
Semana 2 (May 31-Jun 6) 🔄 Llegada componentes + Setup Pi 5
Semana 3 (Jun 7-13)      Setup Prototipo 1 + Inicio visión
Semana 4 (Jun 14-20)     CAD Chasis Prototipo 2 + Continuar visión
Semana 5 (Jun 21-27)     Impresión 3D + Ensamblaje Prototipo 2
Semana 6 (Jun 28-Jul 4)  Integración + Tuning PID + Pruebas
Semana 7 (Jul 5-11)      Pruebas finales + Documentación pulida
Semana 8 (Jul 12+)       🎯 REGIONAL PANAMÁ
```

---

## 📜 Licencia y reconocimientos

Este proyecto se desarrolla con fines educativos para WRO 2026. El código fuente está disponible bajo licencia MIT. La documentación bajo Creative Commons CC-BY 4.0.

Agradecimientos a la comunidad de WRO por documentación abierta de proyectos previos, y a Anthropic por proveer Claude como herramienta de apoyo técnico durante el proceso de selección iterativa de componentes.

---

## 📧 Contacto

- **GitHub:** [@chuyedelgado](https://github.com/chuyedelgado)
- **Repositorio:** [wro2026_CHUISA-ARCITEP](https://github.com/chuyedelgado/wro2026_CHUISA-ARCITEP)
- **Team:** CHUISA ARCITEP (Panamá)

---

*Última actualización: 25 de mayo de 2026 — Post compras completadas*
