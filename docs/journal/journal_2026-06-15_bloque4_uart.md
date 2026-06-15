# REGISTRO DE EJECUCIÓN — JOURNAL TÉCNICO
## WRO 2026 Future Engineers | Equipo CHUISA ARCITEP
*Ubicación sugerida: `docs/journal/2026-06-15_bloque4_uart.md` (o anexar al journal del día)*

---

## 2026-06-15 — Semana 1 · Bloque 4 (UART Pi ↔ Arduino) ✅ casi completo (ver pendientes)

### Conexión física con divisor de voltaje (protección de la Pi)
- **Riesgo:** el Nano Every trabaja a 5 V y su pin TX manda 5 V; la Raspberry Pi 5 trabaja a 3.3 V y sus GPIO **NO toleran 5 V**. Conexión directa dañaría la Pi.
- **Solución:** divisor de voltaje en la línea Arduino-TX1 → Pi-RX, con R1 = 1 kΩ (arriba) y R2 = 2.2 kΩ (abajo).
  - Cálculo teórico: V = 5 × 2200/(1000+2200) = **3.44 V**.
  - **Medido con multímetro antes de energizar la Pi: 3.294 V** (dentro del rango seguro, ≤3.3 V). ✅
- La otra dirección, Pi-TX (3.3 V) → Arduino-RX0, va **directa** (3.3 V basta para nivel alto en el Nano).
- Tierra común entre placas: pin 6 y pin 9 (GND) de la Pi.
- **Verificación de seguridad:** se midió el divisor con el cable de la Pi desconectado, antes de energizar. Buena práctica para no arriesgar la pieza cara.

### Configuración del puerto serial en la Pi
- `raspi-config` → Serial Port: login shell over serial = **NO**; serial hardware = **YES**; reinicio.
- Librería: `pyserial`. Puerto: `/dev/ttyAMA0` (alternativa `/dev/serial0`).
- (Ajuste de configuración necesario, análogo al `dtoverlay` de la cámara.)

### Protocolo
- **Pi → Arduino:** `S<steer>,<speed>*<checksum>`.
- El Arduino usa **Serial1** (pines físicos TX1/RX0), independiente del USB de depuración → permite depurar por USB sin interferir con el enlace a la Pi.
- **Checksum XOR** sobre el cuerpo del mensaje; mensajes corruptos se descartan, no se interpretan.
- Comunicación **bidireccional** confirmada (la Pi ordena, el Arduino recibe/responde).
- Checksum verificado: en la prueba, todos los mensajes válidos se aceptaron, sin falsos descartes.

### Failsafe
- Si no llega comando válido en `TIMEOUT_MS` (500 ms; coincide con `config.py` COMM_TIMEOUT_MS) → steer = 0, speed = 0 (motor parado, dirección centrada).
- Entra al estado de failsafe **una sola vez** y avisa "Comunicación restaurada" al volver los comandos.
- **Aprendizaje (diseño de tiempo real):** el timeout debe calibrarse contra la frecuencia de comandos. A 50 Hz (cada 20 ms), 500 ms tolera perder ~25 comandos seguidos antes de frenar. En la prueba a 1 cmd/s el failsafe saltaba de más (esperado); a 10 cmd/s se mantiene callado con comunicación y solo salta al cortarla.
- Nota: la arquitectura sugería ~200 ms como punto de partida; se usa 500 ms (config.py). **A validar contra la frecuencia real de comandos.**

### Decisiones de ingeniería (X y no Y)
- **Divisor resistivo vs level shifter:** divisor para la regional (barato, suficiente para una sola dirección, ya disponible). Level shifter como mejora futura para el montaje final (más limpio y robusto a vibración).
- **Checksum XOR vs CRC/sumas:** XOR es simple y suficiente para detectar corrupción de bytes en este enlace corto.

### Código
- `src/arduino/uart_protocolo_test.ino`: recepción con checksum + failsafe (semilla de `main.ino`).
- `src/raspberry_pi/uart_comm_test.py`: envío con checksum (semilla de `uart_comm.py`).

### Pendientes (cero datos inventados — marcar pendientes)
- [ ] **Prueba sostenida de 10 minutos** de tráfico sin error de checksum (criterio del Hito S1 "UART 10 min sin error"). **AÚN NO REALIZADA.**
- [ ] **Integrar la telemetría real** Arduino → Pi con formato `T<tof_l>,<tof_f>,<tof_r>,<yaw>,<enc>` (combinar los sensores del Bloque 3 con el UART). Hasta ahora el canal se probó con eco simple, no con datos de sensores.

### Próximo
- Cerrar las dos validaciones de arriba; luego, resto de la S1 (servo) y tareas en paralelo (CAD de soportes, campo).
