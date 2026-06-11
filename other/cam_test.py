from picamera2 import Picamera2
import time

# 1. Crear la cámara y configurarla a 320x240, formato de 3 canales (tu resolución de trabajo)
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (320, 240), "format": "RGB888"})
picam2.configure(config)

# 2. Arrancar y dar 2 s al ajuste automático de exposición y balance de blancos
picam2.start()
time.sleep(2)

# 3. Guardar una foto de prueba (picamera2 maneja el color internamente al guardar)
picam2.capture_file("captura_python.jpg")
print("Imagen guardada: captura_python.jpg")

# 4. Capturar un frame como arreglo numpy (así lo recibirá tu vision.py)
frame = picam2.capture_array()
print("Forma del frame (alto, ancho, canales):", frame.shape)

# 5. Apagar la cámara
picam2.stop()
