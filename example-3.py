# pip install Pillow
from PIL import Image

# Cargar la imagen
imagen = Image.open("fuego.jpg")

# Obtener tamaño de la imagen
ancho, alto = imagen.size
print(f"Ancho: {ancho}, Alto: {alto}")

# Convertir a escala de grises
imagen_gris = imagen.convert("L")

# Obtener el valor de luminosidad del píxel
luminosidad = imagen_gris.getpixel((100, 150))
print(f"Luminosidad del píxel: {luminosidad}")
