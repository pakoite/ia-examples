# pip install easyocr opencv-python-headless
#
import cv2
import easyocr
import matplotlib.pyplot as plt

# Cargar la imagen
ruta_imagen = "texto.jpg"
imagen = cv2.imread(ruta_imagen)

# Convertir la imagen de BGR a RGB (para visualización)
imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

# Crear el lector de EasyOCR especificando el idioma ('en' para inglés, 'es' para español)
lector = easyocr.Reader(["es", "en"])

# Leer texto de la imagen
resultado = lector.readtext(imagen)

# Mostrar resultados
print("Texto extraído de la imagen:")
for bbox, texto, prob in resultado:
    print(f"{texto} (Confianza: {prob:.2f})")

    # Dibujar el cuadro delimitador en la imagen
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = bbox
    cv2.rectangle(imagen_rgb, (int(x0), int(y0)), (int(x2), int(y2)), (0, 255, 0), 2)
    cv2.putText(
        imagen_rgb,
        texto,
        (int(x0), int(y0) - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 0, 0),
        2,
    )

# Mostrar la imagen con los resultados
plt.imshow(imagen_rgb)
plt.axis("off")
plt.show()
