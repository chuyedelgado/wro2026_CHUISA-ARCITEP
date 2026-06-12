# CALIBRACIÓN HSV — METODOLOGÍA Y PLAN DE COMPETENCIA
## WRO 2026 Future Engineers | Equipo CHUISA ARCITEP
*Para `docs/`. Alimenta rúbrica criterios 2 (sensores/calibración) y 3 (software/casos límite).*

---

## Principio rector
Los rangos HSV **no son valores universales**: se calibran al pilar y a la luz que la cámara tiene enfrente en ese momento. La utilería de práctica del equipo tiene tonos distintos a los pilares oficiales (RGB normados), y la luz del taller difiere de la del recinto de competencia. Por eso el valor durable **no son los números, sino la herramienta y el procedimiento de calibración**: los rangos se re-derivan in-situ.

## Por qué HSV (no RGB)
HSV separa el tono (Hue) del brillo (Value). El tono se mantiene relativamente estable cuando cambia la iluminación, mientras que en RGB un cambio de luz altera los tres canales a la vez. Esto hace la detección por color mucho más robusta a sombras y cambios de luz. Nota técnica: en OpenCV el Hue va de 0 a 179 (medio círculo de color).

## Herramienta
`other/hsv_calibrator.py`: calibrador en vivo con sliders (H/S/V min y max), que opera sobre la imagen **ya corregida** (undistort fisheye), mostrando tres paneles: original | máscara | resultado. La tecla `p` imprime el rango actual; `q` sale.
- **Verde:** un solo rango de Hue (calibrado: H 35–85, S 70–255, V 50–255 bajo luz de taller; recalibrar in-situ).
- **Rojo:** DOBLE rango, porque el rojo está en los dos extremos del círculo de Hue (cerca de H 0 y cerca de H 179). La máscara roja final = rango_bajo OR rango_alto.

Nota de calibración: para calibrar COLOR conviene apagar el undistort (`USE_UNDISTORT = False`), porque el undistort cambia la geometría pero NO los colores, y su recorte en los bordes mete franjas negras que confunden. El robot SÍ usa undistort (para medir posiciones), pero los rangos HSV son válidos con o sin él.

## Dónde viven los valores
`src/raspberry_pi/config.py`, como constantes nombradas (regla de arquitectura: ninguna constante mágica fuera de `config.py`). Se mantienen varios perfiles:
- **Perfil por condición de luz** (ver matriz de luz).
- **Modo robusto:** rangos ampliados (S y V más amplios, H estrecho) para luz desconocida o variable; red de seguridad. Trade-off: más robusto a la luz pero más riesgo de colar otros colores.

## Matriz de luz (validación)
Tabla de validación: mañana / tarde / artificial / mixta × normal / robusto. Por cada celda se registran los rangos usados y el % de detección estable. Es la evidencia de robustez ante iluminación (rúbrica criterio 2).

## Hallazgo documentado (punto de falla → iteración)
Durante la calibración se observó que la detección por color varía según la posición del objeto en el encuadre:
- **Bordes:** el lente de 152° tiene viñeteo (más oscuro en bordes) y el undistort recorta las orillas → el color "desaparece" ahí.
- **Centro:** zona más brillante → riesgo de sobreexposición/destello que lava el color (baja su saturación).
Mitigaciones aplicadas: bloquear exposición y balance de blancos en el calibrador (`AeEnable=False`, `AwbEnable=False`), y ampliar S y V manteniendo H estrecho.

## Plan de calibración en competencia (in-situ)

**Contexto legal:** calibrar es LEGAL únicamente en tiempo de práctica. La regla 9.9 prohíbe calibrar sensores en la mesa de revisión y en la colocación del robot (sería descalificación de la ronda). Conexión en pista: sesión local (monitor) o Ethernet; WiFi/BT apagados en las rondas puntuadas.

**Procedimiento (durante los ~60 min de práctica / turnos de 4 min):**
1. Colocar el robot en la pista real, con los pilares oficiales bajo la luz del recinto.
2. Ejecutar el calibrador. Verificación rápida de orden de color (un objeto rojo debe verse rojo, no azul).
3. Apuntar a un pilar VERDE; ajustar sliders hasta que solo el verde quede blanco en la máscara; `p` para registrar el rango.
4. Apuntar a un pilar ROJO; registrar sus DOS sub-rangos (wrap del Hue).
5. Guardar los rangos en el **perfil de competencia** de `config.py`; recargar el programa (el cambio de perfil solo se hace en práctica).
6. Validar con 1 vuelta por dirección que la detección es estable a lo largo de la pista.
7. Si la luz es difícil o cambia durante el día: usar el **modo robusto** (rangos ampliados) como red de seguridad.

**Checklist día D (visión):**
- [ ] Monitor o Ethernet listos para la sesión de calibración.
- [ ] Perfil de competencia calibrado y validado (verde + rojo doble rango).
- [ ] Modo robusto disponible como fallback.
- [ ] Verificar configuración antes de decir "Sí" en la mesa (sin recalibrar ahí).

## Cuidado con los vecinos del rojo en el círculo de Hue
- Por el lado bajo (H subiendo desde 0): hacia ~15-20 empieza el **naranja** → riesgo de confundir una línea naranja de dirección con un pilar rojo. Mantener `H max` del rango bajo controlado.
- Por el lado alto (H bajando desde 179): hacia ~150-160 entra el **magenta** → riesgo de atrapar los delimitadores del parking. Mantener `H min` del rango alto controlado.

## Por qué esto suma en la rúbrica
- Criterio 2: calibración documentada, condiciones justificadas, puntos de falla (luz, viñeteo) y su mitigación (modo robusto + recalibración).
- Criterio 3: manejo de casos límite (wrap del rojo, vecinos naranja/magenta, luz variable) y procedimiento de ajuste con método.
