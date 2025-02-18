# pip install Pillow
from PIL import Image

# Cargar la imagen
imagen = Image.open("fuego.jpg")

# Obtener tamaño de la imagen
ancho, alto = imagen.size
print(f"Ancho: {ancho}, Alto: {alto}")

# Recorrer la imagen píxel por píxel
for y in range(alto):
    for x in range(ancho):
        color = imagen.getpixel((x, y))
        print(f"Píxel en ({x}, {y}): {color}")
