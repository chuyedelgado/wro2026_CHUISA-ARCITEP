# DECISIÓN DE INGENIERÍA — VISIÓN: HSV CLÁSICO vs CÁMARA DE IA (ML)
## WRO 2026 Future Engineers | Equipo CHUISA ARCITEP
*Documento de decisión para `other/decisions/`. Fecha: 10 jun 2026. Estado: DECIDIDO.*

---

## Contexto del problema
La robustez de la visión ante cambios de luz y sombra es el **riesgo #1** del proyecto (tabla de riesgos: probabilidad Alta, impacto Alto). Surgió la propuesta de reemplazar la visión HSV clásica por una **cámara de IA con modelo de ML entrenado con miles de fotos**, con la expectativa de que "funcione perfectamente en cualquier iluminación". Este documento registra por qué se mantiene HSV para la regional y dónde se reubica la idea de ML.

## Decisión
1. **Para la regional (16 jul 2026): se mantiene HSV clásico**, tal como está congelado en la arquitectura. No se rediseña.
2. **La cámara de IA con ML (Sony IMX500) se reclasifica como línea de trabajo POST-regional**, condicionada a clasificar a la final internacional.

## Justificación (por qué HSV y no ML, ahora)
1. **Ajuste herramienta–problema.** El ML profundo aporta su mayor valor con objetos complejos/variados y fondos impredecibles. La pista WRO es lo opuesto y, por tanto, el mejor escenario para visión clásica: colores **especificados en el reglamento** (pilar rojo RGB 238,39,55; verde 68,214,44; magenta 255,0,255; líneas naranja/azul en CMYK), objetos **geométricos sólidos** y fondo **controlado** (campo blanco, muros negros). No hace falta "aprender" qué es rojo: el reglamento lo define.
2. **Depurabilidad en competencia.** Con HSV se ve la máscara en pantalla y se ajusta un rango en segundos; una falla es diagnosticable. Un modelo de ML es una caja negra: cuando falla, no se sabe por qué. En el turno de práctica (~4 min) hay que recalibrar a la luz real del recinto — trivial con HSV, inviable con un modelo entrenado.
3. **Calendario, presupuesto y logística.** A 5 semanas de la regional, con chasis y baterías aún sin llegar, 34.5% sobre presupuesto y la arquitectura explícitamente congelada, un pivote a ML añade costo, riesgo de envío (riesgo logístico #1) y una curva de aprendizaje nueva justo cuando toca endurecer la confiabilidad. Contradice la estrategia maestra: **confiabilidad > puntos nuevos > velocidad.**
4. **Hardware: pérdida de campo de visión.** La cámara de IA natural para la Pi 5 (Raspberry Pi AI Camera, sensor Sony IMX500, ~$70, inferencia en el propio sensor, precargada con MobileNet) tiene un campo de visión de **~76°**. El diseño actual eligió un lente de **152°** precisamente para ver pilares y líneas temprano sin girar la cámara. Cambiar reduciría el FOV casi a la mitad, anulando una decisión de diseño bien fundamentada.

## Alternativa considerada: cámara de IA con ML entrenado
Costo real, no evidente al inicio:
- **Etiquetado manual** de miles de imágenes (caja por cada pilar/línea en cada foto).
- **Datos representativos**: para tolerar "cualquier luz" se necesitan datos que contengan esa variación, imposibles de capturar hoy sin el robot final, la cámara en su posición definitiva ni la luz del recinto.
- **Entrenar y convertir** un modelo propio al pipeline del IMX500 (el MobileNet de fábrica es de clasificación genérica, no detecta nuestros pilares).
- **Opacidad** ante fallas. Ninguna ganancia de robustez compensa, a este plazo, la pérdida de depurabilidad.

## Sobre fusionar ambos sistemas ("redundancia para más seguridad")
La redundancia solo suma seguridad si (a) hay una regla clara para resolver desacuerdos entre sistemas y (b) los sistemas fallan de forma **independiente**. Dos cámaras mirando la misma escena bajo la misma luz fallan por las mismas causas (fallas **correlacionadas**) → poca ganancia real. El diseño actual ya hace la **mejor clase de fusión**: cámara (color/dirección) + ToF (distancia a muros) + IMU (yaw/vueltas), modalidades distintas que fallan por razones distintas. Esa es la red de seguridad de la regional.

## Consecuencias
- **Robustez para la regional** vía: HSV en modo robusto (rangos ampliados), recalibración en tiempo de práctica (legal; regla 9.9 solo prohíbe calibrar en la mesa), matriz de luz (mañana/tarde/artificial/mixta × normal/robusto) y la fusión multi-sensor existente.
- **Riesgo aceptado**: dependencia de una buena calibración HSV el día D → mitigado con el modo robusto y el procedimiento de recalibración ensayado.

## Roadmap post-regional (si clasificamos a la final)
1. **Definir la falla específica y medida** del HSV que el ML deba resolver (p. ej. "bajo luz mixta con sombras duras, el rojo se sale del rango y se confunde el lado del pilar"). Sin falla medida, no se añade ML.
2. Evaluar opciones (IMX500 on-sensor — vigilando el FOV de 76° — o un acelerador externo en la Pi).
3. Entrenar/convertir un modelo propio y **verificar que arregla la falla medida** antes de integrarlo.
4. Si se integra, hacerlo como complemento con regla de conflicto explícita, no como fusión a ciegas.
