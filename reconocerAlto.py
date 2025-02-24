import cv2 as cv
import numpy as np

imagen = cv.imread("stop.jpg")

# Rangos de rojos en hsv
redLow1 = np.array([171,204,135],np.uint8)
redHigh1 = np.array([178,253,166],np.uint8)

#rangos de blanco en hsv
whiteLow = np.array([162,20,217],np.uint8)
whiteHigh = np.array([175,76,245],np.uint8)

# convertir la imagen a hsv
hsv = cv.cvtColor(imagen, cv.COLOR_BGR2HSV)

# Crear las mascaras
mask1 = cv.inRange(hsv, redLow1, redHigh1) # mascara para el rojo
mask2 = cv.inRange(hsv, whiteLow, whiteHigh) # mascara para el blanco
mask = cv.add(mask1, mask2) # mascara para el rojo y blanco

# aplicar color real
maskStopVision = cv.bitwise_and(imagen, imagen, mask=mask)

cv.imshow("Imagen real", maskStopVision)
cv.imshow("Imagen", imagen)
cv.imshow("Mask", mask)
cv.waitKey(0)
cv.destroyAllWindows()    # Cerrar todas las ventanas abiertas

