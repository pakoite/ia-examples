# pip install opencv-python opencv-python-headless
import cv2

# Leer una imagen
imagen = cv2.imread("fuego.jpg")
cv2.namedWindow("Imagen", cv2.WINDOW_NORMAL)
# Convertir a escala de grises
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

cv2.imshow("Imagen", imagen_gris)
# Detección de bordes con Canny
# bordes = cv2.Canny(imagen_gris, 100, 200)

# Mostrar los bordes
# cv2.imshow('Bordes', bordes)

# Mostrar la imagen en gris
cv2.waitKey(0)
cv2.destroyWindow("Imagen")
cv2.waitKey(1)
cv2.waitKey(1)
exit()
