from PIL import ImageGrab
from datetime import datetime

# Crear nombre de archivo con la fecha y hora actual
nombre_archivo = datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.png")

# Tomar captura de pantalla
screenshot = ImageGrab.grab()

# Guardar la captura de pantalla
screenshot.save(nombre_archivo)

print(f"¡Captura de pantalla guardada como {nombre_archivo}!")
