import cv2
import numpy as np

# Cargar la imagen
imagen = cv2.imread("auto-pilot.jpg")

# Obtener tamaño
alto, ancho, canales = imagen.shape
print(f"Tamaño: {ancho}x{alto}, Canales: {canales}")

# Leer y modificar un píxel
color_original = imagen[150, 100]
print(f"Píxel original en (100, 150): {color_original}")

# Cambiar el color a verde
imagen[150, 100] = [0, 255, 0]

# Obtener solo el canal rojo de toda la imagen
canal_rojo = imagen[:, :, 2]

# Mostrar imagen modificada
cv2.imshow("Imagen Modificada", imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()
