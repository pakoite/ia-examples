# pip install Pillow
from PIL import Image

# Cargar la imagen
imagen = Image.open("fuego.jpg")

# Obtener tamaño de la imagen
ancho, alto = imagen.size
print(f"Ancho: {ancho}, Alto: {alto}")

# pip install numpy
import numpy as np

# Convertir la imagen a un arreglo de Numpy
matriz = np.array(imagen)

# Imprimir el color del píxel en (100, 150)
print(matriz[150, 100])
