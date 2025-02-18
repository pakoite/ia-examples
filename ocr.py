"""
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-eng
pip install pytesseract opencv-python-headless Pillow
sudo apt install tesseract-ocr-spa
"""

import cv2
import pytesseract
from PIL import Image

# Ruta a la imagen
ruta_imagen = "texto.jpg"

# Cargar imagen con OpenCV
imagen = cv2.imread(ruta_imagen)

# Convertir a escala de grises
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar umbral para mejorar el contraste
_, umbral = cv2.threshold(gris, 150, 255, cv2.THRESH_BINARY)

# Guardar imagen preprocesada (opcional, para verificar el preprocesamiento)
cv2.imwrite("imagen_procesada.png", umbral)

# Convertir la imagen procesada para usar con Pytesseract
imagen_pil = Image.fromarray(umbral)

# Leer texto de la imagen usando Tesseract
texto = pytesseract.image_to_string(imagen_pil, lang="spa")

# Imprimir el texto extraído
print("Texto extraído de la imagen:")
print(texto)
