# pip install opencv-python opencv-python-headless
import cv2

# Leer una imagen
imagen = cv2.imread("fuego.jpg")

# Mostrar la imagen
cv2.imshow("Imagen", imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()
