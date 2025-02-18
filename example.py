# pip install Pillow
from PIL import Image

# Cargar la imagen
imagen = Image.open("fuego.jpg")

# Obtener tamaño de la imagen
ancho, alto = imagen.size
print(f"Ancho: {ancho}, Alto: {alto}")

# Obtener el color de un píxel (en la posición x=100, y=150)
color_pixel = imagen.getpixel((100, 150))
print(f"Color del píxel: {color_pixel}")
