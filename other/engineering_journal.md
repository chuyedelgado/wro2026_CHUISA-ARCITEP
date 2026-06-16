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

## 2026-06-10 — Semana 1 (Fase 1-A: plataforma viva sin chasis ni batería)

### Bloque 1 — Raspberry Pi 5 ✅ COMPLETADO

**Hardware**
- Raspberry Pi 5 (4 GB) + Active Cooler oficial.
- Active Cooler montado con sus almohadillas térmicas pre-aplicadas. NO se añadió pasta MX-4 (se reserva como repuesto para un eventual reasentado del cooler).
- microSD SanDisk Ultra 32 GB UHS-I.

**Sistema operativo y acceso**
- Raspberry Pi OS Bookworm 64-bit, flasheado con Raspberry Pi Imager.
- Sistema actualizado (`sudo apt update` + `sudo apt full-upgrade`).
- Acceso headless por SSH: **OK y confiable** (verificado tras apagar y volver a encender).
- Bus I2C habilitado vía `raspi-config` (preparado para los sensores del Bloque 3).
- Repositorio del equipo clonado en la Pi.

**Mediciones térmicas (datos reales medidos)**

| Métrica | Condición | Valor |
|---|---|---|
| Temp. máx CPU | `stress-ng --cpu 4 --timeout 300s` (5 min, 4 núcleos, temp. ambiente de banco) | **59.6 °C** |
| Temp. idle (reposo) | — | `[por registrar]` |
| `vcgencmd get_throttled` | — | `[por registrar]` — reportado sin errores; confirmar y anotar el valor exacto (se espera `0x0`) |

**Observación de ingeniería**
59.6 °C bajo carga de CPU queda por debajo del umbral objetivo (<60 °C) pero con margen estrecho (~0.4 °C). Consideraciones:
1. Esta prueba estresa solo la CPU. La carga real de operación es de **visión** (cámara + OpenCV + procesador de imagen), de comportamiento térmico distinto → medir de nuevo en el Bloque 2.
2. Riesgo a vigilar: temperatura ambiente del recinto de competencia (Panamá). Un salón caluroso reduce el margen.

**Acciones pendientes derivadas**
- [ ] Registrar temp. idle y valor de `get_throttled`.
- [ ] Repetir la medición térmica bajo carga de visión (Bloque 2) y comparar contra 59.6 °C.

---

### Bloque 2 — Cámara 152° + pipeline HSV ✅ COMPLETADO (visión S1)
- Cámara SainSmart Camera Module 3 (IMX708, 152°) conectada a la Pi 5.
- **Aprendizaje clave (punto de falla resuelto):** la cámara es de tercero (no oficial). Requirió (a) el cable correcto de 22 pines para el conector de la Pi 5, y (b) declarar el sensor a mano en `/boot/firmware/config.txt` con `dtoverlay=imx708` (la auto-detección sola no la reconoció). Tras esto: `rpicam-hello --list-cameras` detecta el `imx708`.
- Pipeline en Python operativo (picamera2 + OpenCV); captura a 320×240.
- **Calibración del lente (decisión basada en datos):** modelo estándar (pinhole) → error de reproyección **2.39 px** con distorsión residual en las orillas. Cambio al **modelo fisheye** → error **0.61 px**. Se elige fisheye (`config/camera_calibration_fisheye.npz`). El lente de 152° excede el modelo pinhole; el fisheye es el correcto.
- **Calibración HSV:** verde (un rango) y rojo (doble rango por wrap del Hue) calibrados con `other/hsv_calibrator.py` y guardados en `src/raspberry_pi/config.py`.
- **Hallazgo de robustez:** la detección por color varía con la posición en el encuadre (viñeteo del lente, recorte del undistort en bordes, exposición). Mitigaciones aplicadas: bloquear exposición/AWB en el calibrador, ampliar S y V (manteniendo H estrecho), y plan de modo robusto + recalibración in-situ.

### Próximo: Bloque 3 — Sensores I2C (2× VL53L1X ToF + MPU-6050)


### Semana 3 — Junio 7-13 | SETUP DE PROTOTIPO 1 + INICIO DE VISIÓN

[A completar]
#### Bloque 2 — Conexión, verificación y calibración inicial de cámara IMX708

Durante esta semana se inició el bloque de visión artificial del proyecto. El objetivo principal fue conectar la cámara SainSmart Pi Camera Module 3 con sensor IMX708 y lente ultra wide de 152°, verificar que la Raspberry Pi 5 la detectara correctamente, probar la captura desde Python y comenzar la calibración del sistema de visión que se utilizará para detectar pilares rojos y verdes.

Este bloque es crítico porque la cámara será el sensor principal para identificar colores, posición relativa de pilares, líneas de pista y referencias visuales necesarias para la navegación autónoma. La configuración debía quedar funcionando antes de avanzar a la lógica de detección, evasión y control.

##### Objetivos del bloque

* Verificar físicamente la conexión de la cámara a la Raspberry Pi 5.
* Diagnosticar el error inicial de detección de cámara.
* Confirmar el reconocimiento del sensor IMX708 por el sistema.
* Realizar una captura de prueba con herramientas del sistema.
* Probar la cámara desde Python usando `picamera2`.
* Calibrar la distorsión del lente ultra wide de 152°.
* Comparar calibración estándar contra calibración fisheye.
* Crear rangos HSV iniciales para detección de verde y rojo.
* Documentar el procedimiento de recalibración in-situ para competencia.

---

##### 2A. Conexión y diagnóstico inicial de la cámara

La cámara fue conectada a la Raspberry Pi 5 mediante cable plano de 22 pines. Al ejecutar el primer comando de verificación:

```bash
rpicam-hello --list-cameras
```

el sistema respondió:

```text
No cameras available!
```

Este resultado indicaba que la Raspberry Pi no estaba detectando físicamente la cámara. Se revisaron tres posibles causas:

1. Cable mal orientado o mal insertado.
2. Incompatibilidad entre el cable y el conector de la cámara.
3. Configuración incorrecta del sistema para una cámara de tercero.

Se confirmó que el cable utilizado era de 22 pines en ambos extremos y que sí correspondía al hardware disponible, ya que el cable de 15 pines no encajaba físicamente en esta versión de cámara. Por lo tanto, el problema no era el tipo de cable.

Luego se verificó el archivo de configuración del sistema:

```bash
grep camera /boot/firmware/config.txt
```

El sistema devolvió:

```text
camera_auto_detect=1
```

Esto indicaba que la auto-detección estaba activada, pero no estaba logrando inicializar correctamente el módulo de cámara.

##### Decisión técnica tomada

Se decidió desactivar la auto-detección y declarar manualmente el sensor IMX708 en `/boot/firmware/config.txt`.

Configuración aplicada:

```text
camera_auto_detect=0
dtoverlay=imx708
```

Después de guardar los cambios y reiniciar la Raspberry Pi, se repitió la prueba:

```bash
rpicam-hello --list-cameras
```

Resultado:

```text
Available cameras
-----------------
0 : imx708 [4608x2592 10-bit RGGB] (/base/axi/pcie@1000120000/rp1/i2c@80000/imx708@1a)
    Modes: 'SRGGB10_CSI2P' : 1536x864 [120.13 fps - (768, 432)/3072x1728 crop]
                             2304x1296 [56.03 fps - (0, 0)/4608x2592 crop]
                             4608x2592 [14.35 fps - (0, 0)/4608x2592 crop]
```

Este resultado confirmó que la Raspberry Pi reconoció correctamente el sensor IMX708.

##### Aprendizaje del diagnóstico

El problema no era una falla de hardware ni un cable dañado. La causa fue que esta cámara de tercero requería declarar explícitamente el sensor mediante `dtoverlay=imx708`. Esta corrección se documenta porque representa un punto de falla real del sistema y una solución reproducible para el equipo.

---

##### 2B. Captura de imagen y prueba desde Python

Después de confirmar que el sistema operativo detectaba la cámara, se realizó una captura de prueba:

```bash
rpicam-jpeg --output captura.jpg --timeout 2000
```

La imagen fue copiada a la laptop mediante:

```bash
scp chuisa@chuisa.local:~/captura.jpg .
```

La captura fue exitosa y se verificó visualmente que la imagen era reconocible.

Luego se pasó a la prueba desde Python, porque el código principal de visión del robot trabajará con `picamera2` y OpenCV.

Se verificó `picamera2`:

```bash
python3 -c "from picamera2 import Picamera2; print('picamera2 OK')"
```

Se instaló y verificó OpenCV:

```bash
sudo apt install -y python3-opencv
python3 -c "import cv2; print('OpenCV', cv2.__version__)"
```

Se creó el script de prueba:

```text
other/cam_test.py
```

Este script configuró la cámara a resolución de trabajo de 320×240 y capturó un frame como arreglo de imagen.

Resultado esperado y obtenido:

```text
Forma del frame (alto, ancho, canales): (240, 320, 3)
```

Este resultado confirma que la cámara, Python y OpenCV ya pueden trabajar juntos. La resolución 320×240 se adopta como resolución inicial de trabajo porque reduce la carga computacional y permite mantener mayor velocidad de procesamiento para visión en tiempo real.

Estado del Bloque 2B:

* [x] Cámara detectada por Raspberry Pi OS.
* [x] Captura realizada con `rpicam-jpeg`.
* [x] Imagen copiada exitosamente a laptop.
* [x] `picamera2` verificado.
* [x] OpenCV instalado y verificado.
* [x] Script `other/cam_test.py` creado.
* [x] Frame capturado desde Python con forma `(240, 320, 3)`.
* [x] Script agregado al repositorio mediante commit.

---

##### 2C. Calibración del lente ultra wide de 152°

La cámara seleccionada tiene un lente de 152°, lo cual permite observar pilares y líneas con mayor anticipación. Sin embargo, este tipo de lente genera distorsión de barril, especialmente en los bordes de la imagen. Para corregir ese efecto, se realizó una calibración usando un tablero de ajedrez de 9×6 esquinas internas.

Primero se creó un script para capturar imágenes de calibración:

```text
other/capture_calibration.py
```

El script capturó imágenes del tablero en diferentes posiciones, ángulos y zonas del encuadre. Se obtuvieron:

```text
20 fotos en calib_images/
```

Luego se creó el script de calibración estándar:

```text
other/calibrate_camera.py
```

Resultado de calibración estándar:

```text
19 imágenes usables.
Error de reproyección: 2.3949 px
Guardado: config/camera_calibration.npz
Comparación lado a lado: comparacion_calibracion.jpg
```

El error de reproyección fue considerado alto para una calibración final. Esto indicó que el modelo estándar de cámara no era el más adecuado para el lente ultra wide de 152°.

##### Iteración técnica: cambio a modelo fisheye

Debido al alto error del modelo estándar, se creó una segunda calibración usando el modelo fisheye de OpenCV:

```text
other/calibrate_fisheye.py
```

Resultado de calibración fisheye:

```text
19 imágenes usables.
Error de reproyección FISHEYE: 0.6139 px
Guardado: config/camera_calibration_fisheye.npz
Comparación: comparacion_fisheye.jpg
```

##### Decisión final de calibración

Se decidió utilizar la calibración fisheye como calibración principal del sistema de visión, porque redujo el error de reproyección de 2.3949 px a 0.6139 px.

| Modelo de calibración | Imágenes usables | Error de reproyección | Archivo generado                        | Decisión                              |
| --------------------- | ---------------: | --------------------: | --------------------------------------- | ------------------------------------- |
| Estándar / pinhole    |               19 |             2.3949 px | `config/camera_calibration.npz`         | Descartado como calibración principal |
| Fisheye               |               19 |             0.6139 px | `config/camera_calibration_fisheye.npz` | Elegido                               |

Esta comparación representa una iteración basada en datos. No se eligió el modelo fisheye por suposición, sino porque produjo un error de reproyección significativamente menor.

Estado del Bloque 2C:

* [x] Tablero de calibración preparado.
* [x] 20 imágenes capturadas.
* [x] 19 imágenes usables.
* [x] Calibración estándar ejecutada.
* [x] Calibración fisheye ejecutada.
* [x] Error estándar registrado: 2.3949 px.
* [x] Error fisheye registrado: 0.6139 px.
* [x] Archivo `camera_calibration_fisheye.npz` generado.
* [x] Modelo fisheye elegido para el pipeline de visión.

---

##### 2D. Calibración inicial de colores HSV

Después de calibrar la geometría de la cámara, se inició la calibración de colores HSV para detectar pilares verdes y rojos.

Se creó una herramienta interactiva de calibración HSV:

```text
other/hsv_calibrator.py
```

La herramienta permite visualizar tres paneles:

1. Imagen original.
2. Máscara blanco/negro.
3. Resultado filtrado.

La calibración se hizo con sliders para ajustar:

* H min
* H max
* S min
* S max
* V min
* V max

##### Observación importante durante pruebas

Durante la calibración se observó que el comportamiento del color cambiaba cuando el objeto se movía hacia los bordes del encuadre o cuando la cámara era inclinada. En verde, el objeto se detectaba correctamente en el centro, pero podía perderse en los bordes. En rojo, el comportamiento fue más crítico: bajo ciertas inclinaciones, el rojo se detectaba mejor en los bordes que en el centro.

El diagnóstico fue que no se trataba de un bug directo del código, sino de una combinación de factores físicos y de imagen:

* Viñeteo del lente ultra wide.
* Cambios de brillo según la zona del encuadre.
* Auto-exposición de la cámara.
* Reflejos sobre el material del pilar.
* Recorte o zonas negras generadas por la corrección de distorsión.

##### Ajustes aplicados durante la calibración

Se decidió calibrar color sin aplicar undistort, porque la corrección geométrica puede generar bordes negros y no es necesaria para medir rangos de color. La corrección geométrica se utilizará posteriormente en el pipeline de visión para estimar posiciones, pero la calibración HSV puede realizarse directamente sobre la imagen sin corregir.

También se decidió ampliar los rangos de saturación y brillo para crear un perfil más robusto:

* Mantener Hue relativamente controlado.
* Bajar `S min` para tolerar zonas menos saturadas.
* Bajar `V min` para tolerar sombras o zonas más oscuras.
* Mantener `S max` y `V max` en 255.

##### Valores HSV calibrados

Valores iniciales calibrados para verde:

```python
GREEN_HSV_LOWER = np.array([35, 70, 50])
GREEN_HSV_UPPER = np.array([85, 255, 255])
```

Valores iniciales calibrados para rojo:

```python
RED_HSV_LOWER_1 = np.array([0, 70, 34])
RED_HSV_UPPER_1 = np.array([10, 255, 255])

RED_HSV_LOWER_2 = np.array([170, 70, 34])
RED_HSV_UPPER_2 = np.array([179, 255, 255])
```

El rojo se maneja con doble rango porque en OpenCV el Hue va de 0 a 179, y el rojo se encuentra en los dos extremos del círculo de color: cerca de 0 y cerca de 179.

##### Archivo actualizado

Los valores fueron agregados al archivo:

```text
src/raspberry_pi/config.py
```

Esto cumple la regla de arquitectura de mantener las constantes de configuración en un solo lugar y evitar números mágicos dispersos en el código.

Estado del Bloque 2D:

* [x] Herramienta HSV creada.
* [x] Verde calibrado.
* [x] Rojo calibrado usando doble rango.
* [x] Valores guardados en `config.py`.
* [x] Problemas de iluminación y bordes identificados.
* [x] Necesidad de recalibración in-situ documentada.
* [ ] Validación pendiente con pilares oficiales y luz de competencia.

---

##### Resultado general del Bloque 2

El Bloque 2 se considera completado a nivel de configuración inicial de visión. La cámara fue conectada, detectada, probada desde sistema y Python, calibrada geométricamente con modelo fisheye, y se generaron rangos HSV iniciales para verde y rojo.

Resultado final:

* Cámara IMX708 detectada correctamente.
* Captura de imagen validada.
* Script de prueba Python creado.
* Calibración fisheye seleccionada por menor error.
* Rangos HSV iniciales definidos.
* Configuración centralizada en `config.py`.
* Procedimiento de recalibración para competencia identificado.

##### Relación con la rúbrica

Este bloque aporta evidencia directa a:

* **Criterio 2:** integración de sensor principal de visión y validación de funcionamiento.
* **Criterio 3:** creación de herramientas de software para captura, calibración y configuración.
* **Criterio 4:** iteración basada en datos al comparar calibración estándar contra fisheye.
* **Criterio 5:** reproducibilidad, porque los scripts, archivos `.npz` y valores HSV quedan documentados en el repositorio.


#### Bloque 3 — Cierre documental, prueba de vida del Arduino Nano Every e inicio de sensores I2C

Después de completar la integración inicial de visión, se realizó el cierre documental del trabajo realizado y se inició el siguiente bloque técnico del proyecto: la puesta en marcha del Arduino Nano Every y la preparación para integrar sensores I2C.

Este bloque marca el inicio de la arquitectura distribuida del robot. Hasta este punto, la Raspberry Pi 5 había sido configurada como cerebro principal para visión y toma de decisiones. A partir de este bloque se comienza a validar el Arduino Nano Every como microcontrolador de bajo nivel, encargado de leer sensores con mayor regularidad temporal y posteriormente comunicarse con la Raspberry Pi.

---

##### 3A. Organización de archivos, documentación y commits al repositorio

Antes de continuar con nuevos sensores, se realizó una revisión del estado del repositorio para asegurar que el trabajo de visión quedara guardado y documentado correctamente.

Se definió separar los cambios en dos grupos:

1. Código y archivos técnicos.
2. Documentos de soporte y decisiones de ingeniería.

Esta separación permite mantener un historial de commits más claro y facilita demostrar avance progresivo del proyecto dentro de GitHub.

###### Verificación previa de `config.py`

Antes de subir los cambios, se verificó que `src/raspberry_pi/config.py` siguiera siendo válido y que Python pudiera importar correctamente los rangos HSV calibrados.

Comando utilizado:

```bash
cd ~/wro2026_CHUISA-ARCITEP
python3 -c "import sys; sys.path.insert(0,'src/raspberry_pi'); import config; print('verde', config.GREEN_HSV_LOWER, config.GREEN_HSV_UPPER); print('rojo1', config.RED_HSV_LOWER_1, config.RED_HSV_UPPER_1); print('rojo2', config.RED_HSV_LOWER_2, config.RED_HSV_UPPER_2)"
```

El objetivo de este paso fue evitar subir un archivo de configuración con errores de sintaxis o constantes mal definidas.

###### Creación/actualización de `.gitignore`

También se preparó el archivo `.gitignore` para evitar subir archivos temporales o pesados generados durante calibración.

Contenido agregado:

```bash
cat >> .gitignore << 'EOF'

# Imagenes de calibracion/diagnostico (no recargar el repo)
calib_images/
calib_check/
comparacion_*.jpg
captura*.jpg
__pycache__/
*.pyc
EOF
```

La decisión de no subir `calib_images/` y `calib_check/` se tomó porque esas carpetas contienen imágenes temporales de captura y diagnóstico. El resultado reproducible de la calibración queda guardado en los archivos `.npz`, que sí deben permanecer en el repositorio.

###### Commit de código

Se preparó un commit para incluir los scripts, configuraciones y archivos de calibración generados durante el trabajo de visión:

```bash
git add -A
git status
git commit -m "feat: calibrador HSV y rangos de color verde/rojo en config.py"
```

Este commit agrupa los cambios funcionales relacionados con:

* herramienta de calibración HSV;
* valores HSV reales para rojo y verde;
* archivos de calibración de cámara;
* `.gitignore`;
* configuración centralizada en `config.py`.

###### Documentos regenerados y organizados

También se regeneraron tres documentos de soporte para dejar evidencia metodológica del trabajo realizado:

| Documento                             | Ubicación en el repo | Propósito                                                           |
| ------------------------------------- | -------------------- | ------------------------------------------------------------------- |
| `journal_2026-06-10.md`               | `docs/journal/`      | Documentar el cierre del Bloque 2, incluyendo cámara, fisheye y HSV |
| `decision_vision_hsv_vs_camara_ia.md` | `other/decisions/`   | Documentar la decisión HSV vs cámara IA/ML                          |
| `calibracion_hsv_plan_competencia.md` | `docs/`              | Documentar metodología de calibración HSV y plan de competencia     |

Carpetas creadas:

```bash
mkdir -p docs/journal other/decisions
```

Comandos usados para copiar documentos desde la laptop hacia la Raspberry Pi:

```bash
scp journal_2026-06-10.md chuisa@chuisa.local:~/wro2026_CHUISA-ARCITEP/docs/journal/
scp decision_vision_hsv_vs_camara_ia.md chuisa@chuisa.local:~/wro2026_CHUISA-ARCITEP/other/decisions/
scp calibracion_hsv_plan_competencia.md chuisa@chuisa.local:~/wro2026_CHUISA-ARCITEP/docs/
```

Commit documental sugerido:

```bash
git add -A
git status
git commit -m "docs: journal, decision de vision HSV y plan de calibracion en competencia"
git push
```

##### Resultado de esta fase

* [x] Se definió una estrategia clara para separar commits de código y documentación.
* [x] Se verificó `config.py` antes de subirlo.
* [x] Se agregó `.gitignore` para evitar subir archivos temporales.
* [x] Se organizaron documentos técnicos en carpetas del repositorio.
* [x] Se documentó la decisión HSV vs cámara IA.
* [x] Se documentó la metodología de calibración HSV para competencia.

---

##### 3B. Inicio del Bloque 3: Arduino Nano Every

Después del cierre del bloque de visión, se inició el Bloque 3 enfocado en sensores I2C y microcontrolador. El primer objetivo fue confirmar que el equipo podía programar el Arduino Nano Every desde la laptop.

El Arduino Nano Every será usado como microcontrolador de bajo nivel. Su función será leer sensores como el MPU-6050 y los VL53L1X con una frecuencia estable, procesar datos cercanos al hardware y posteriormente comunicarse con la Raspberry Pi mediante UART.

###### Justificación de usar Arduino para sensores

Aunque la Raspberry Pi 5 tiene alta capacidad de cómputo, no es ideal para tareas de bajo nivel que requieren tiempos de respuesta constantes. El Arduino Nano Every ofrece mejor control temporal para lectura de sensores, interrupciones y señales físicas.

Arquitectura esperada:

```text
Raspberry Pi 5  → visión, lógica principal, decisión
Arduino Nano Every → lectura de sensores, señales rápidas, comunicación de bajo nivel
```

Sensores previstos para este bloque:

| Sensor         | Función dentro del robot                                   |
| -------------- | ---------------------------------------------------------- |
| 2× VL53L1X ToF | Medir distancia a paredes laterales para wall-following    |
| 1× MPU-6050    | Medir giro/yaw para detección de giros y conteo de vueltas |

---

##### 3C. Prueba de vida del Arduino Nano Every

Se instaló y configuró Arduino IDE en la laptop. Luego se seleccionó la placa correspondiente:

```text
Tools → Board → Arduino Nano Every
```

También se revisó el puerto USB correspondiente al Arduino en la laptop.

La primera prueba realizada fue el ejemplo básico `Blink`, que permite comprobar si el Arduino compila, sube y ejecuta código.

Inicialmente se observó que el Arduino tenía:

| LED                  | Observación                                                |
| -------------------- | ---------------------------------------------------------- |
| Verde fijo           | Indica alimentación por USB                                |
| Amarillo parpadeando | Indica que ya existía un programa Blink cargado de fábrica |

Se aclaró que el parpadeo inicial no era evidencia suficiente de que el equipo hubiera subido su propio código, porque muchos Arduino vienen con Blink precargado.

###### Verificación real del upload

Para confirmar que el código sí estaba siendo cargado por el equipo, se modificó el tiempo de parpadeo del programa Blink.

Cambio realizado:

```cpp
delay(100);
```

Luego se probó también un parpadeo más lento:

```cpp
delay(2000);
```

Resultado observado:

```text
El LED amarillo obedeció los cambios de velocidad.
```

Esto confirmó que:

* el Arduino Nano Every era reconocido por la laptop;
* el código compilaba correctamente;
* el código se subía a la placa;
* el Arduino ejecutaba el programa cargado.

###### Mensaje `avrdude` observado

Durante la carga apareció el siguiente mensaje:

```text
Sketch uses 1118 bytes (2%) of program storage space. Maximum is 49152 bytes.
Global variables use 22 bytes (0%) of dynamic memory, leaving 6122 bytes for local variables. Maximum is 6144 bytes.
avrdude: jtagmkII_initialize(): Cannot locate "flash" and "boot" memories in description
```

Inicialmente se interpretó como posible error, pero luego se verificó experimentalmente que el código sí se estaba subiendo porque el LED cambiaba de ritmo según el programa cargado.

Conclusión: para este caso, el mensaje no impidió la carga del sketch. La evidencia real fue el comportamiento físico del LED.

###### Sketch vacío para detener el parpadeo

Después de comprobar el funcionamiento del Arduino, se cargó un sketch vacío para detener el parpadeo del LED amarillo:

```cpp
void setup() {

}

void loop() {

}
```

Este paso dejó el Arduino energizado, pero sin ejecutar parpadeo visible.

Estado de la prueba Arduino:

* [x] Arduino Nano Every conectado por USB.
* [x] Placa seleccionada en Arduino IDE.
* [x] Programa Blink cargado.
* [x] LED amarillo obedeció cambios de velocidad.
* [x] Mensaje `avrdude` interpretado correctamente.
* [x] Sketch vacío cargado para detener el parpadeo.
* [x] Cadena de herramientas Arduino validada.

---

##### 3D. Identificación del sensor disponible: MPU-6050

El siguiente paso planificado era conectar un sensor ToF VL53L1X. Sin embargo, al revisar el módulo disponible, se identificaron los siguientes pines:

```text
VCC
GND
SCL
SDA
XDA
XCL
ADO
INT
```

A partir de estas etiquetas se determinó que el módulo no correspondía al VL53L1X, sino al IMU MPU-6050.

La identificación se realizó porque los pines `XDA`, `XCL` y `AD0/ADO` son característicos del MPU-6050. El sensor ToF VL53L1X normalmente incluye pines como `VIN`, `GND`, `SDA`, `SCL`, `XSHUT` y `GPIO1`.

##### Decisión tomada

Se decidió cambiar temporalmente el orden del Bloque 3 y comenzar por el MPU-6050 antes de conectar los ToF.

Esta decisión es razonable porque el MPU-6050 también usa I2C y es una buena primera prueba del bus. Además, no requiere resolver todavía el problema de direcciones repetidas que sí aparece cuando se conectan múltiples VL53L1X.

---

##### 3E. Plan de conexión del MPU-6050 al Arduino Nano Every

Se definió el cableado esperado para conectar el MPU-6050 al Arduino Nano Every por I2C:

| MPU-6050 | Arduino Nano Every | Función                          |
| -------- | ------------------ | -------------------------------- |
| VCC      | 5V                 | Alimentación del módulo          |
| GND      | GND                | Tierra común                     |
| SDA      | A4                 | Línea de datos I2C               |
| SCL      | A5                 | Línea de reloj I2C               |
| XDA      | Sin conectar       | No se usa en esta fase           |
| XCL      | Sin conectar       | No se usa en esta fase           |
| AD0/ADO  | Sin conectar       | Dirección por defecto 0x68       |
| INT      | Sin conectar       | No se usa en esta prueba inicial |

Se definió usar un escáner I2C para verificar si el Arduino detecta el MPU-6050 en la dirección esperada:

```text
0x68
```

Sin embargo, antes de realizar la conexión física se identificó una limitación importante.

---

##### 3F. Bloqueo actual: pines del MPU-6050 no soldados

Al revisar el módulo MPU-6050, se confirmó que los pines/header no estaban soldados a la placa del sensor.

Esto impide realizar una conexión confiable con cables Dupont o protoboard, porque sin pines soldados no hay contacto firme ni seguro entre el sensor y el Arduino.

También se identificó que el equipo tiene placas universales 3×7 tipo PCB/perfboard. Estas placas no son equivalentes a una protoboard, ya que no tienen conexiones internas automáticas. Para usarlas correctamente se requiere soldadura.

##### Decisión tomada

No se debe intentar una conexión improvisada del MPU-6050 sin soldar los headers. El siguiente paso correcto es soldar los pines del sensor o conseguir una protoboard/cables adecuados antes de continuar con la prueba I2C.

Estado actual del Bloque 3:

* [x] Arduino Nano Every probado con Blink.
* [x] Upload de sketches verificado mediante cambio físico del LED.
* [x] Se identificó correctamente el módulo MPU-6050.
* [x] Se definió el cableado I2C esperado.
* [x] Se detectó que los pines del MPU-6050 no están soldados.
* [ ] Soldar headers del MPU-6050.
* [ ] Conectar MPU-6050 al Arduino Nano Every.
* [ ] Ejecutar escáner I2C.
* [ ] Confirmar dirección `0x68`.
* [ ] Leer datos reales del IMU.

##### Resultado del Bloque 3 hasta este punto

El Bloque 3 no se considera completado todavía. Sí se completó la prueba de vida del Arduino Nano Every, pero la integración del primer sensor I2C quedó pendiente por falta de headers soldados en el MPU-6050.

Este hallazgo se documenta porque evita un error de montaje físico y muestra una decisión correcta de ingeniería: no forzar una conexión débil o insegura antes de preparar adecuadamente el hardware.


### Semana 4 — Junio 14-20 | SENSORES I2C Y COMUNICACIÓN PI-ARDUINO

Durante esta semana se avanzó en la integración electrónica de bajo nivel del robot. Después de haber completado la configuración inicial de visión en la Raspberry Pi 5, el trabajo se enfocó en habilitar el Arduino Nano Every como microcontrolador encargado de la lectura de sensores y de la comunicación con la Raspberry Pi.

El objetivo principal fue validar físicamente los sensores I2C del robot, confirmar que podían convivir en un mismo bus y comenzar la comunicación UART entre la Raspberry Pi y el Arduino de forma segura. Este avance es importante porque conecta los dos niveles principales de la arquitectura: la Raspberry Pi como cerebro de alto nivel y el Arduino como controlador de sensores y señales rápidas.

---

#### Bloque 3 — Soldadura, sensores I2C y validación del sistema sensorial

##### Objetivo del bloque

El objetivo del Bloque 3 fue preparar físicamente los módulos electrónicos, soldar los headers necesarios, conectar los sensores al Arduino Nano Every y validar la lectura de los dispositivos principales por I2C.

Sensores trabajados:

| Componente         | Función dentro del robot                                                |
| ------------------ | ----------------------------------------------------------------------- |
| MPU-6050           | Medición de giro/yaw para orientación, giros de 90° y conteo de vueltas |
| VL53L1X ToF #1     | Medición de distancia a una pared lateral                               |
| VL53L1X ToF #2     | Medición de distancia a la otra pared lateral                           |
| Arduino Nano Every | Lectura de sensores y comunicación de bajo nivel                        |

---

##### 3A. Soldadura de headers del MPU-6050

Al iniciar el trabajo con el MPU-6050 se observó que el módulo no tenía los pines/header soldados. Esto impedía realizar una conexión confiable, ya que los cables Dupont no podían hacer contacto firme con la placa del sensor.

Se decidió soldar los headers antes de continuar. Para ello se utilizó un soldador de punta fija y una protoboard como soporte para mantener los pines alineados durante la soldadura.

El proceso consistió en:

1. Colocar la tira de pines en la protoboard para mantenerla recta.
2. Ubicar el MPU-6050 sobre los pines.
3. Soldar primero una esquina para fijar la posición.
4. Revisar que la placa quedara alineada.
5. Soldar el resto de los pines.
6. Verificar visualmente que no hubiera puentes de estaño.
7. Comprobar que los pines quedaran firmes.

Resultado:

* [x] Headers del MPU-6050 soldados.
* [x] Pines firmes y listos para conexión.
* [x] Sensor preparado para prueba I2C.

Este paso se documenta porque fue la primera intervención física permanente sobre un módulo electrónico del robot.

---

##### 3B. Soldadura de headers del Arduino Nano Every

Después de soldar el MPU-6050, se revisó el Arduino Nano Every y se identificó que tampoco tenía sus pines laterales soldados. Se decidió soldarlos porque el Arduino será el nodo central de conexión de sensores, comunicación y señales de bajo nivel.

La decisión de soldar los pines del Arduino fue tomada por confiabilidad. Intentar conectar cables a una placa sin headers produciría falsos contactos, lecturas intermitentes y errores difíciles de diagnosticar.

Se soldaron las dos tiras laterales del Arduino Nano Every usando la protoboard como guía para mantener los pines rectos y paralelos.

Resultado:

* [x] Headers del Arduino Nano Every soldados.
* [x] Pines alineados y firmes.
* [x] Arduino listo para conexión con sensores.

Esta soldadura desbloqueó la integración física del Arduino con el resto del sistema.

---

##### 3C. Conexión y detección del MPU-6050 por I2C

Con los pines del MPU-6050 y del Arduino soldados, se conectó el sensor al Arduino Nano Every usando cables Dupont hembra-hembra.

Cableado utilizado:

| MPU-6050 | Arduino Nano Every | Función               |
| -------- | ------------------ | --------------------- |
| VCC      | 5V                 | Alimentación          |
| GND      | GND                | Tierra común          |
| SDA      | A4                 | Datos I2C             |
| SCL      | A5                 | Reloj I2C             |
| XDA      | Sin conectar       | No usado              |
| XCL      | Sin conectar       | No usado              |
| AD0/ADO  | Sin conectar       | Dirección por defecto |
| INT      | Sin conectar       | No usado              |

Se ejecutó un escáner I2C para verificar si el Arduino detectaba el sensor.

Resultado esperado:

```text
Dispositivo en 0x68
```

Resultado obtenido:

```text
0x68 detectado
```

También se observó que el LED del MPU-6050 encendió al conectar el Arduino, lo cual confirmó alimentación correcta del módulo.

Conclusión:

El MPU-6050 fue detectado correctamente en el bus I2C con dirección `0x68`.

Estado:

* [x] MPU-6050 alimentado.
* [x] Comunicación I2C validada.
* [x] Dirección `0x68` confirmada.
* [x] Sensor listo para lectura de yaw.

---

##### 3D. Lectura de yaw y medición de drift del giroscopio

Después de detectar el MPU-6050, se instaló y utilizó la librería `MPU6050_light` para leer el ángulo de giro sobre el eje Z, utilizado como yaw.

Se realizó una prueba dejando el sensor quieto durante 1 minuto para observar el drift del giroscopio.

Resultado medido:

```text
Drift del giroscopio: aproximadamente 0.5° en 1 minuto
```

Interpretación:

El drift observado es bajo para la aplicación del robot. Los giros principales son de aproximadamente 90°, por lo que un desplazamiento de 0.5° por minuto no representa un problema crítico para las pruebas iniciales. De todos modos, este valor deberá considerarse al diseñar la lógica de conteo de vueltas y corrección de orientación.

Estado:

* [x] MPU-6050 lee yaw.
* [x] Drift inicial medido.
* [x] Drift registrado con método de medición.
* [ ] Validar comportamiento del yaw con el sensor montado en el chasis final.

---

##### 3E. Identificación, soldadura y prueba individual del primer ToF VL53L1X

Luego se trabajó con el sensor ToF VL53L1X. Se identificó correctamente el módulo por sus pines:

```text
VIN, GND, SDA, SCL, INT, SHUT
```

Se soldaron los headers del primer ToF y se probó individualmente, desconectando temporalmente el MPU-6050.

Cableado para prueba individual:

| VL53L1X ToF | Arduino Nano Every | Función                     |
| ----------- | ------------------ | --------------------------- |
| VIN         | 5V                 | Alimentación                |
| GND         | GND                | Tierra común                |
| SDA         | A4                 | Datos I2C                   |
| SCL         | A5                 | Reloj I2C                   |
| INT         | Sin conectar       | No usado en prueba inicial  |
| SHUT        | Sin conectar       | No usado con un solo sensor |

Se ejecutó el escáner I2C.

Resultado esperado:

```text
Dispositivo en 0x29
```

Resultado obtenido:

```text
0x29 detectado
```

Después se instaló la librería `VL53L1X` de Pololu y se probó la lectura de distancia en milímetros.

Resultado:

* [x] Sensor detectado en `0x29`.
* [x] Sensor leyó distancias en milímetros.
* [x] Las lecturas cambiaron al acercar y alejar objetos.
* [x] Precisión inicial medida con error aproximado de ±3 mm contra una distancia de 100 mm.

Se observó que el sensor no mide por debajo de aproximadamente 20 mm. Esto fue identificado como una limitación normal del sensor, no como una falla. Para el robot esta limitación no representa un problema, ya que las distancias útiles de wall-following estarán mucho más arriba, alrededor de 250–300 mm.

---

##### 3F. Soldadura y prueba del segundo ToF

Luego se soldaron los headers del segundo VL53L1X. El objetivo fue preparar dos sensores ToF para funcionar simultáneamente en el mismo bus I2C.

El problema técnico identificado fue que ambos sensores VL53L1X salen de fábrica con la misma dirección I2C:

```text
0x29
```

Dos dispositivos con la misma dirección no pueden convivir directamente en el mismo bus I2C. Para resolverlo se utilizó el pin `SHUT` o `XSHUT`, que permite apagar y encender cada sensor individualmente durante el arranque.

---

##### 3G. Dos ToF simultáneos usando XSHUT

Se conectaron los dos sensores ToF a una protoboard blanca, compartiendo alimentación y las líneas I2C.

Conexiones compartidas:

| Línea       | Conexión                       |
| ----------- | ------------------------------ |
| 5V Arduino  | Riel positivo de la protoboard |
| GND Arduino | Riel negativo de la protoboard |
| A4 Arduino  | Columna SDA compartida         |
| A5 Arduino  | Columna SCL compartida         |

Cableado de cada ToF:

| Pin del ToF | Conexión      |
| ----------- | ------------- |
| VIN         | Riel positivo |
| GND         | Riel negativo |
| SDA         | Columna SDA   |
| SCL         | Columna SCL   |
| SHUT ToF #1 | D2 Arduino    |
| SHUT ToF #2 | D3 Arduino    |
| INT         | Sin conectar  |

La estrategia aplicada fue:

1. Apagar ambos ToF usando `SHUT`.
2. Encender solo el ToF #1.
3. Cambiar su dirección de `0x29` a `0x2A`.
4. Encender el ToF #2.
5. Dejar el ToF #2 en su dirección de fábrica `0x29`.

Resultado final:

| Sensor | Dirección I2C final |
| ------ | ------------------- |
| ToF #1 | `0x2A`              |
| ToF #2 | `0x29`              |

Se verificó que ambos sensores podían medir distancias de forma independiente. Al tapar o acercar un objeto frente a uno de los sensores, solo cambiaba la lectura correspondiente a ese sensor.

Estado:

* [x] Segundo ToF soldado.
* [x] Ambos ToF conectados al mismo bus I2C.
* [x] XSHUT usado para evitar conflicto de direcciones.
* [x] ToF #1 reasignado a `0x2A`.
* [x] ToF #2 mantenido en `0x29`.
* [x] Lecturas independientes verificadas.

---

##### 3H. Integración de 3 dispositivos I2C en el mismo bus

Después de validar los dos ToF, se volvió a conectar el MPU-6050 al mismo bus I2C. El MPU comparte las líneas SDA y SCL, pero no genera conflicto porque su dirección es distinta:

```text
MPU-6050: 0x68
```

Direcciones finales en el bus:

| Dispositivo | Dirección |
| ----------- | --------- |
| ToF #2      | `0x29`    |
| ToF #1      | `0x2A`    |
| MPU-6050    | `0x68`    |

Resultado esperado del escáner:

```text
Dispositivo en 0x29
Dispositivo en 0x2A
Dispositivo en 0x68
Total encontrados: 3
```

Resultado:

```text
Los 3 dispositivos fueron detectados correctamente.
```

Luego se probó la lectura conjunta de:

* distancia del ToF izquierdo;
* distancia del ToF derecho;
* yaw del MPU-6050.

Resultado:

* [x] Dos distancias leídas simultáneamente.
* [x] Yaw leído simultáneamente.
* [x] Al tapar cada ToF, solo cambiaba su lectura.
* [x] Al girar el conjunto, cambiaba el yaw.
* [x] El bus I2C con 3 dispositivos quedó validado.

Conclusión del Bloque 3:

El sistema sensorial principal quedó validado a nivel de prototipo. El Arduino Nano Every puede leer simultáneamente dos sensores ToF VL53L1X y un IMU MPU-6050 en el mismo bus I2C. Esto cumple el objetivo de integrar sensores de distancia y orientación antes de pasar a la comunicación con la Raspberry Pi.

---

#### Bloque 4 — Comunicación UART Raspberry Pi 5 ↔ Arduino Nano Every

##### Objetivo del bloque

El objetivo del Bloque 4 fue establecer comunicación serial UART entre la Raspberry Pi 5 y el Arduino Nano Every. Esta comunicación permitirá que la Raspberry Pi envíe comandos de alto nivel y que el Arduino reporte datos de sensores o ejecute acciones de bajo nivel.

Arquitectura de comunicación esperada:

```text
Raspberry Pi 5 → comandos de dirección y velocidad → Arduino Nano Every
Arduino Nano Every → telemetría de sensores → Raspberry Pi 5
```

---

##### 4A. Riesgo de voltaje y decisión de protección

Antes de cablear la Raspberry Pi con el Arduino, se identificó un riesgo crítico: el Arduino Nano Every trabaja con lógica de 5V, mientras que la Raspberry Pi usa lógica de 3.3V en sus pines GPIO.

La línea peligrosa es:

```text
Arduino TX → Raspberry Pi RX
```

Esto se debe a que el Arduino transmite señales de 5V, pero el pin RX de la Raspberry Pi no debe recibir 5V. Para proteger la Raspberry Pi se decidió usar un divisor de voltaje en esa línea.

La otra dirección no requiere divisor:

```text
Raspberry Pi TX → Arduino RX
```

Esto es seguro porque la señal de 3.3V de la Raspberry Pi puede ser interpretada por el Arduino como nivel alto.

---

##### 4B. Divisor de voltaje con resistencias

Se revisaron las resistencias disponibles y se eligió la combinación:

| Resistencia | Valor | Posición en el divisor         |
| ----------- | ----: | ------------------------------ |
| R1          |   1kΩ | Entre Arduino TX y punto medio |
| R2          | 2.2kΩ | Entre punto medio y GND        |

Cálculo teórico:

```text
Vout = Vin × R2 / (R1 + R2)
Vout = 5V × 2200 / (1000 + 2200)
Vout ≈ 3.44V
```

El divisor se armó en la protoboard.

Estructura del divisor:

```text
Arduino TX1 → R1 1kΩ → punto medio → R2 2.2kΩ → GND
                           |
                           └── Raspberry Pi RX
```

Antes de conectar el punto medio al RX de la Raspberry Pi, se midió el voltaje con multímetro.

Resultado medido:

```text
Voltaje en punto medio: 3.294 V
```

Conclusión:

El divisor de voltaje funcionó correctamente y redujo la señal a un nivel seguro para la Raspberry Pi.

Estado:

* [x] Riesgo 5V vs 3.3V identificado.
* [x] Divisor resistivo diseñado.
* [x] Divisor armado en protoboard.
* [x] Voltaje medido con multímetro.
* [x] Valor real medido: 3.294 V.
* [x] Raspberry Pi protegida antes de conectar UART.

---

##### 4C. Cableado UART entre Raspberry Pi y Arduino

Se identificaron los pines UART de la Raspberry Pi:

| Raspberry Pi 5 | Pin físico | Función                 |
| -------------- | ---------: | ----------------------- |
| GPIO14 / TXD   |          8 | Transmite hacia Arduino |
| GPIO15 / RXD   |         10 | Recibe desde Arduino    |
| GND            |      6 / 9 | Tierra común            |

En el Arduino Nano Every se utilizaron los pines físicos:

| Arduino Nano Every | Función                      |
| ------------------ | ---------------------------- |
| TX1                | Transmite hacia Raspberry Pi |
| RX0                | Recibe desde Raspberry Pi    |
| GND                | Tierra común                 |

Cableado aplicado:

| Desde                          | Hacia                           | Protección                     |
| ------------------------------ | ------------------------------- | ------------------------------ |
| Arduino TX1                    | Divisor de voltaje              | Baja 5V a aproximadamente 3.3V |
| Punto medio del divisor        | Raspberry Pi RXD, pin físico 10 | Señal segura para Pi           |
| Raspberry Pi TXD, pin físico 8 | Arduino RX0                     | Directo                        |
| Arduino GND                    | Raspberry Pi GND                | Tierra común                   |
| GND del divisor                | Raspberry Pi GND                | Tierra del divisor             |

Se usaron dos pines GND de la Raspberry Pi para mantener el cableado más ordenado.

---

##### 4D. Configuración del puerto serial en Raspberry Pi

Antes de probar UART, se configuró la Raspberry Pi para liberar el puerto serial de los pines GPIO.

Configuración realizada con:

```bash
sudo raspi-config
```

Opciones seleccionadas:

```text
Interface Options → Serial Port
Login shell over serial: NO
Serial port hardware enabled: YES
```

Luego se reinició la Raspberry Pi.

Este paso fue necesario porque la Raspberry Pi puede usar el puerto serial como consola del sistema. Para el robot, ese puerto debe quedar libre para comunicación de datos con el Arduino.

---

##### 4E. Prueba inicial Arduino → Raspberry Pi

Primero se probó la comunicación en una sola dirección: Arduino enviando mensajes hacia la Raspberry Pi.

Arduino enviaba:

```text
Hola Pi, soy el Arduino
```

La Raspberry Pi ejecutó un script Python con `pyserial` para leer el puerto serial.

Resultado obtenido:

```text
Recibido: Hola Pi, soy el Arduino
```

Conclusión:

La comunicación Arduino → Raspberry Pi funcionó correctamente. Esto validó el divisor de voltaje, el cableado TX/RX y la configuración serial de la Raspberry Pi.

---

##### 4F. Prueba bidireccional

Después se probó comunicación en ambas direcciones. La Raspberry Pi enviaba comandos con formato similar al protocolo real:

```text
S0,0
S0,10
S0,20
...
```

El Arduino recibía el mensaje y respondía:

```text
OK, recibi: S0,0
```

Resultado:

```text
Ambos recibieron correctamente.
```

Conclusión:

La comunicación UART quedó validada en ambas direcciones:

* Raspberry Pi → Arduino.
* Arduino → Raspberry Pi.

Esto confirmó que el cruce TX/RX estaba correcto y que la tierra común funcionaba adecuadamente.

---

##### 4G. Protocolo con checksum y failsafe

Después de validar la comunicación básica, se implementó una versión inicial del protocolo con checksum y failsafe.

Formato probado para comandos de la Raspberry Pi hacia el Arduino:

```text
S<steer>,<speed>*<checksum>
```

Ejemplos enviados por la Raspberry Pi:

```text
S0,0*127
S0,10*78
S0,20*77
S0,30*76
S0,40*75
S0,50*74
S0,60*73
S0,70*72
S0,80*71
S0,90*70
S0,100*126
```

El checksum utilizado fue un XOR de los caracteres del cuerpo del mensaje.

El Arduino validó correctamente los mensajes recibidos:

```text
VALIDO -> steer=0 speed=90
VALIDO -> steer=0 speed=100
VALIDO -> steer=0 speed=0
VALIDO -> steer=0 speed=10
...
```

No se observaron mensajes descartados por checksum durante la prueba.

---

##### 4H. Ajuste del failsafe

Inicialmente el script de la Raspberry Pi enviaba comandos cada 1 segundo, mientras que el timeout del failsafe estaba configurado en 500 ms. Esto provocaba que el failsafe se activara entre comandos, aunque la comunicación estuviera funcionando.

Se identificó que el problema no era del protocolo, sino de la frecuencia de envío de la prueba.

Ajuste realizado:

```python
time.sleep(0.1)
```

Con este cambio, la Raspberry Pi envía comandos cada 100 ms, es decir, 10 comandos por segundo. Esto es más parecido al comportamiento esperado del robot real.

También se ajustó el código del Arduino para que el failsafe no imprimiera mensajes repetidos de forma continua, sino que avisara solo al entrar en estado de failsafe y al restaurarse la comunicación.

Resultado final:

* Con comandos llegando cada 100 ms, el failsafe no se activó durante operación normal.
* Al detener el script de la Raspberry Pi, el failsafe se activó después de aproximadamente 500 ms.
* Al reiniciar el script, el Arduino reportó restauración de comunicación.

Conclusión:

El failsafe quedó funcionando correctamente como mecanismo de seguridad ante pérdida de comunicación.

---

##### Resultado general del Bloque 4

El Bloque 4 validó la comunicación UART entre Raspberry Pi 5 y Arduino Nano Every. Se completaron las pruebas básicas de envío, recepción, comunicación bidireccional, checksum y failsafe.

Estado final:

* [x] Riesgo de nivel lógico 5V vs 3.3V identificado.
* [x] Divisor de voltaje diseñado con 1kΩ y 2.2kΩ.
* [x] Voltaje seguro medido: 3.294 V.
* [x] UART configurado en Raspberry Pi.
* [x] Comunicación Arduino → Pi validada.
* [x] Comunicación Pi → Arduino validada.
* [x] Comunicación bidireccional confirmada.
* [x] Checksum XOR implementado y probado.
* [x] Failsafe implementado y probado.
* [x] Código subido al repositorio.

Pendiente para cierre total del protocolo:

* [ ] Prueba continua de 10 minutos sin errores.
* [ ] Integrar telemetría real de sensores en formato `T<tof_l>,<tof_r>,<yaw>`.
* [ ] Integrar comandos reales de velocidad y dirección con actuadores.

##### Relación con la rúbrica

Este bloque aporta evidencia directa a:

* **Criterio 2:** integración electrónica segura entre Raspberry Pi y Arduino, considerando diferencias de voltaje.
* **Criterio 3:** implementación de protocolo de comunicación, checksum y failsafe.
* **Criterio 4:** decisiones de ingeniería basadas en riesgo, especialmente divisor resistivo vs level shifter y ajuste del timeout del failsafe.
* **Criterio 5:** reproducibilidad, porque el código de prueba y la documentación fueron subidos al repositorio.

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

---------
**Actualización de criterio**
*Semana 4*
Durante la Semana 4 se avanzó significativamente en la integración física de sensores y comunicación electrónica.

Evidencias agregadas:
- Se soldaron los headers del MPU-6050.
- Se soldaron los headers del Arduino Nano Every.
- Se soldaron los headers de dos sensores VL53L1X.
- Se validó el MPU-6050 en dirección I2C 0x68.
- Se validó un ToF individual en dirección 0x29.
- Se integraron dos ToF en el mismo bus usando XSHUT.
- Se reasignó un ToF a 0x2A para evitar conflicto de direcciones.
- Se integraron tres dispositivos en el mismo bus I2C: 0x29, 0x2A y 0x68.
- Se midió drift del giroscopio: aproximadamente 0.5° en 1 minuto.
- Se midió precisión inicial del ToF: error aproximado de ±3 mm a 100 mm.
- Se identificó la distancia mínima útil del ToF, aproximadamente 20 mm.
- Se construyó un divisor de voltaje para proteger la Raspberry Pi del TX de 5V del Arduino.
- Se verificó el divisor con multímetro antes de conectar la Raspberry Pi.
- Voltaje real medido del divisor: 3.294 V.

Conclusión del criterio:

La Semana 4 aporta evidencia fuerte de integración electrónica segura. El equipo no solo conectó sensores, sino que identificó riesgos físicos, soldó componentes, validó direcciones I2C y protegió la Raspberry Pi antes de establecer UART.




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

**Avances adicionales del Bloque 3:**
- Se validó la cadena de herramientas del Arduino Nano Every mediante prueba Blink.
- Se confirmó que el equipo puede compilar, subir y ejecutar sketches desde Arduino IDE.
- Se identificó una advertencia recurrente de `avrdude` que no bloqueó la subida del sketch.
- Se preparó el siguiente paso de software: escáner I2C para detectar sensores en el bus.

**Actualización de criterio**
*Semana 4*
Durante esta semana se validaron dos componentes importantes de software de bajo nivel: lectura multisensor por I2C y comunicación UART con protocolo.

Evidencias agregadas:

- Se usó escáner I2C para diagnóstico de sensores.
- Se probó lectura de yaw con MPU6050_light.
- Se probó lectura de distancia con librería VL53L1X.
- Se implementó secuencia XSHUT para evitar conflicto entre dos ToF.
- Se probó lectura simultánea de dos distancias y yaw.
- Se configuró el puerto serial de Raspberry Pi con raspi-config.
- Se instaló y usó pyserial.
- Se probó comunicación Arduino → Pi.
- Se probó comunicación Pi → Arduino.
- Se implementó formato inicial S<steer>,<speed>*<checksum>.
- Se implementó checksum XOR.
- Se implementó failsafe de 500 ms.
- Se ajustó la frecuencia de comandos para evitar activaciones falsas del failsafe.

Conclusión del criterio:

El software de bajo nivel comenzó a tomar forma como sistema integrado. Ya no se tienen pruebas aisladas, sino comunicación real entre sensores, Arduino y Raspberry Pi.

### Criterio 4: Pensamiento Sistémico

**Evidencia:**

1. Estrategia dos prototipos — gestión riesgo a nivel proyecto
2. Mount modular eje trasero — diseño para evolución (v1 → v2)
3. Aislamiento baterías — comprensión ruido eléctrico motor
4. Sensores ToF + IMU separados — sensor correcto para cada problema
5. Arquitectura Pi + Arduino — comprensión limitaciones Python tiempo real
6. Metodología iterativa con IA múltiple — proceso documentado y replicable

**Trade-offs documentados:** Cada decisión en sección 4 incluye tabla comparativa. 24 decisiones revisadas en Apéndice D.

**Nueva evidencia de pensamiento sistémico:**
- Se evitó asumir que el LED parpadeando del Arduino era evidencia de upload propio, y se verificó modificando el ritmo de parpadeo.
- Se identificó correctamente que el módulo con pines `XDA`, `XCL` y `AD0/ADO` correspondía al MPU-6050 y no al sensor ToF.
- Se ajustó el orden del bloque para comenzar con el IMU antes del ToF.
- Se decidió no conectar el MPU-6050 sin headers soldados, evitando una conexión física insegura.

**Actualización de criterio**
*Semana 4*
La Semana 4 contiene varias decisiones importantes basadas en riesgo, evidencia y restricciones reales.

Decisiones documentadas:

- Soldar headers antes de conectar sensores. Se decidió no improvisar conexiones con pines sueltos para evitar falsos contactos.
- Comenzar con el MPU-6050 antes del ToF. Al identificar que el primer módulo disponible era un MPU-6050 y no un ToF, se ajustó el orden de trabajo sin bloquear el avance.
- Usar XSHUT para dos ToF. Se resolvió el conflicto de direcciones I2C entre dos sensores VL53L1X mediante control individual de encendido.
- Aceptar la distancia mínima del ToF como limitación normal. Se observó que el sensor no mide correctamente por debajo de aproximadamente 20 mm, pero se determinó que esto no afecta el uso real del robot.
- Usar divisor resistivo en lugar de level shifter para la regional. Se eligió un divisor con resistencias porque era suficiente, disponible y rápido de implementar. El level shifter queda como mejora futura para un montaje más limpio.
- Medir el divisor antes de conectar la Pi. Se verificó el voltaje con multímetro antes de conectar el pin RX de la Raspberry Pi, reduciendo el riesgo de daño.
- Ajustar el failsafe según frecuencia de comandos. Se observó que enviar comandos cada 1 segundo activaba el failsafe de 500 ms. Se corrigió enviando comandos cada 100 ms, representando mejor la operación real.
  
Este bloque demuestra pensamiento sistémico porque las decisiones no se tomaron por ensayo ciego, sino por diagnóstico, medición y control de riesgos.

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

**Avances de repositorio:**
- Se verificó `config.py` antes de subirlo al repositorio.
- Se agregó `.gitignore` para excluir imágenes temporales, capturas de diagnóstico y archivos Python compilados.
- Se separaron commits de código y documentación para mantener historial claro.
- Se organizaron documentos técnicos en `docs/`, `docs/journal/` y `other/decisions/`.


## REGISTRO DE PRUEBAS

*(Esta sección se completa a medida que se ejecutan las pruebas)*

### Pruebas de microcontrolador — Arduino Nano Every

| Fecha         | Prueba                              | Método                                                       | Resultado                                                                                  | Conclusión                                                                       |
| ------------- | ----------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| 12 junio 2026 | Conexión del Arduino Nano Every     | USB a laptop + Arduino IDE                                   | Arduino energizado, LED verde fijo                                                         | Placa recibe alimentación correctamente                                          |
| 12 junio 2026 | Blink inicial                       | Ejemplo `Blink` en Arduino IDE                               | LED amarillo parpadeaba desde conexión                                                     | El parpadeo inicial podía ser programa precargado, no evidencia de upload propio |
| 12 junio 2026 | Verificación de upload              | Cambio de `delay(1000)` a `delay(100)` y luego `delay(2000)` | LED amarillo cambió de ritmo                                                               | Confirmado que el equipo puede subir código al Arduino                           |
| 12 junio 2026 | Interpretación de mensaje `avrdude` | Observación del resultado de upload                          | Mensaje `Cannot locate "flash" and "boot" memories` apareció, pero el sketch sí se ejecutó | Mensaje tratado como advertencia no bloqueante para esta placa                   |
| 12 junio 2026 | Sketch vacío                        | `setup()` y `loop()` sin instrucciones                       | LED amarillo dejó de parpadear                                                             | Arduino quedó listo para la siguiente prueba                                     |
| 13 junio 2026 | Identificación de sensor disponible | Revisión de pines: VCC, GND, SCL, SDA, XDA, XCL, ADO, INT    | Sensor identificado como MPU-6050, no ToF                                                  | Se corrigió el orden del bloque y se decidió iniciar con IMU                     |
| 13 junio 2026 | Revisión física del MPU-6050        | Inspección del módulo                                        | Pines/header no soldados                                                                   | Integración I2C queda pendiente hasta soldar headers                             |

### Pruebas I2C pendientes

| Prueba pendiente                | Resultado esperado                                             |
| ------------------------------- | -------------------------------------------------------------- |
| Soldar headers del MPU-6050     | Pines firmes y listos para conexión                            |
| Conectar MPU-6050 al Nano Every | VCC→5V, GND→GND, SDA→A4, SCL→A5                                |
| Ejecutar escáner I2C            | Detección de dispositivo en `0x68`                             |
| Leer datos del IMU              | Valores de acelerómetro/giroscopio visibles por Serial Monitor |
| Calcular yaw                    | Base para giros de 90° y conteo de vueltas                     |

### Capturas recomendadas para subir al repositorio

Guardar en:

```text
other/images/week03_arduino_i2c/
```

| Evidencia                                               | Nombre sugerido                                           |
| ------------------------------------------------------- | --------------------------------------------------------- |
| Arduino Nano Every conectado por USB                    | `week03_nano_every_connected.jpg`                         |
| Arduino IDE con placa Nano Every seleccionada           | `week03_arduino_board_selected.png`                       |
| Blink modificado con `delay(100)` o `delay(2000)`       | `week03_blink_modified.png`                               |
| Mensaje de compilación/upload con advertencia `avrdude` | `week03_avrdude_warning.png`                              |
| LED amarillo parpadeando rápido/lento                   | `week03_blink_led_test.mp4` o `week03_blink_led_test.jpg` |
| Sketch vacío cargado                                    | `week03_empty_sketch.png`                                 |
| Foto del MPU-6050 con pines visibles                    | `week03_mpu6050_pins.jpg`                                 |
| Foto mostrando que los headers no están soldados        | `week03_mpu6050_unsoldered_headers.jpg`                   |
| Foto de la PCB universal 3×7                            | `week03_perfboard_3x7.jpg`                                |

### Pruebas de sensores I2C — Semana 4

| Fecha         | Prueba                           | Método                                     | Resultado                                        | Conclusión                                    |
| ------------- | -------------------------------- | ------------------------------------------ | ------------------------------------------------ | --------------------------------------------- |
| 15 junio 2026 | Soldadura de MPU-6050            | Headers soldados con soporte de protoboard | Pines firmes y sensor listo                      | Se desbloqueó la conexión física del IMU      |
| 15 junio 2026 | Soldadura de Arduino Nano Every  | Headers laterales soldados                 | Pines firmes y placa lista para cableado         | Arduino preparado como nodo central           |
| 15 junio 2026 | Detección MPU-6050               | Escáner I2C                                | Dirección `0x68` detectada                       | IMU responde correctamente                    |
| 15 junio 2026 | Lectura de yaw                   | Librería `MPU6050_light`                   | Yaw leído correctamente                          | IMU funcional para orientación                |
| 15 junio 2026 | Drift del giroscopio             | Sensor quieto durante 1 minuto             | Drift aproximado de `0.5°`                       | Drift bajo para pruebas iniciales             |
| 15 junio 2026 | Soldadura ToF #1                 | Headers soldados                           | Sensor listo                                     | ToF preparado para prueba individual          |
| 15 junio 2026 | Detección ToF #1                 | Escáner I2C                                | Dirección `0x29` detectada                       | ToF responde correctamente                    |
| 15 junio 2026 | Lectura de distancia ToF #1      | Librería Pololu `VL53L1X`                  | Distancia en mm cambia al acercar/alejar objetos | Sensor funcional                              |
| 15 junio 2026 | Precisión ToF                    | Comparación contra distancia de 100 mm     | Error aproximado de ±3 mm                        | Cumple criterio inicial de precisión          |
| 15 junio 2026 | Límite mínimo ToF                | Acercar objeto por debajo de 20 mm         | No mide correctamente por debajo de ~20 mm       | Limitación normal, no afecta el uso del robot |
| 15 junio 2026 | Soldadura ToF #2                 | Headers soldados                           | Sensor listo                                     | Segundo ToF preparado                         |
| 15 junio 2026 | Dos ToF con XSHUT                | XSHUT en D2 y D3                           | ToF #1 en `0x2A`, ToF #2 en `0x29`               | Conflicto de direcciones resuelto             |
| 15 junio 2026 | Lectura independiente de dos ToF | Tapar/acercar objetos a cada sensor        | Cada sensor cambió su propia lectura             | Ambos ToF funcionan de forma independiente    |
| 15 junio 2026 | Bus I2C con 3 dispositivos       | Escáner I2C después de sumar MPU           | `0x29`, `0x2A`, `0x68` detectados                | Sistema sensorial I2C validado                |
| 15 junio 2026 | Lectura conjunta                 | Dos ToF + yaw por Serial Monitor           | Dos distancias + yaw visibles                    | Sistema sensorial integrado                   |

### Pruebas UART — Semana 4

| Fecha         | Prueba                       | Método                                   | Resultado                                         | Conclusión                                         |
| ------------- | ---------------------------- | ---------------------------------------- | ------------------------------------------------- | -------------------------------------------------- |
| 15 junio 2026 | Diseño del divisor           | Resistencias de 1kΩ y 2.2kΩ              | Cálculo teórico ≈ 3.44 V                          | Protección adecuada para RX de la Pi               |
| 15 junio 2026 | Medición del divisor         | Multímetro en punto medio                | `3.294 V`                                         | Voltaje seguro antes de conectar a la Pi           |
| 15 junio 2026 | Configuración serial de Pi   | `raspi-config`                           | Serial hardware activado, login shell desactivado | UART libre para comunicación                       |
| 15 junio 2026 | Arduino → Pi                 | Arduino envía mensaje, Pi lee con Python | `Recibido: Hola Pi, soy el Arduino`               | Comunicación en una dirección validada             |
| 15 junio 2026 | Pi → Arduino → Pi            | Pi envía `S0,n`, Arduino responde `OK`   | Ambos recibieron correctamente                    | Comunicación bidireccional validada                |
| 15 junio 2026 | Checksum XOR                 | Mensajes `S<steer>,<speed>*<checksum>`   | Arduino aceptó mensajes como `VALIDO`             | Checksum funcional                                 |
| 15 junio 2026 | Failsafe inicial             | Timeout 500 ms con envío cada 1 s        | Failsafe se activaba entre comandos               | Se identificó desajuste entre frecuencia y timeout |
| 15 junio 2026 | Failsafe ajustado            | Envío cada 100 ms                        | No se activó durante comunicación normal          | Frecuencia de prueba corregida                     |
| 15 junio 2026 | Pérdida de comunicación      | Detener script de Pi                     | Failsafe activado después de ~500 ms              | Seguridad ante pérdida de comandos validada        |
| 15 junio 2026 | Restauración de comunicación | Reiniciar script de Pi                   | Comunicación restaurada                           | Failsafe se recupera al volver comandos válidos    |

### Capturas y evidencias recomendadas

Guardar en:

```text
other/images/week04_i2c_uart/
```

| Evidencia                            | Nombre sugerido                       |
| ------------------------------------ | ------------------------------------- |
| MPU-6050 antes de soldar             | `week04_mpu_unsoldered.jpg`           |
| MPU-6050 después de soldar           | `week04_mpu_soldered.jpg`             |
| Arduino Nano Every después de soldar | `week04_nano_soldered.jpg`            |
| Escáner I2C mostrando `0x68`         | `week04_i2c_mpu_0x68.png`             |
| Lectura de yaw                       | `week04_mpu_yaw_reading.png`          |
| ToF individual mostrando `0x29`      | `week04_tof_single_0x29.png`          |
| Lectura de distancia ToF             | `week04_tof_distance_mm.png`          |
| Dos ToF en protoboard con XSHUT      | `week04_dual_tof_xshut_setup.jpg`     |
| Escáner con `0x29`, `0x2A`, `0x68`   | `week04_i2c_three_devices.png`        |
| Lectura conjunta ToF + yaw           | `week04_sensor_fusion_serial.png`     |
| Divisor de voltaje en protoboard     | `week04_uart_voltage_divider.jpg`     |
| Medición multímetro 3.294 V          | `week04_divider_multimeter_3294v.jpg` |
| Primer mensaje recibido en Pi        | `week04_uart_arduino_to_pi.png`       |
| Prueba bidireccional                 | `week04_uart_bidirectional.png`       |
| Checksum válido en Arduino           | `week04_uart_checksum_valid.png`      |
| Failsafe activado                    | `week04_uart_failsafe.png`            |

### Commits sugeridos

```bash
git add src/arduino/sensores_i2c_test.ino docs/journal/journal_2026-06-15.md
git commit -m "feat: integra 3 sensores I2C con dos ToF y MPU"
git push
```

```bash
git add src/arduino/uart_protocolo_test.ino src/raspberry_pi/uart_comm_test.py docs/journal/journal_2026-06-15_bloque4_uart.md
git commit -m "feat: protocolo UART con checksum y failsafe"
git push
```

Si ya subieron todo junto, dejarlo como está. Lo importante es que el repositorio tenga evidencia de código y documentación.


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
