import cv2
import numpy as np

# Ouvrir la caméra
cap = cv2.VideoCapture(0)

while True:
    # Capture image
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Appliquer un seuil pour segmenter les disques
    _, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Trouver les contours
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    tailles = []
    for contour in contours:
        # Calculer la surface et le rayon des disques
        area = cv2.contourArea(contour)
        (x, y), radius = cv2.minEnclosingCircle(contour)
        tailles.append(radius)
        # Dessiner le contour pour visualisation
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

    # Afficher les tailles des disques triées
    tailles.sort()
    print("Tailles des disques :", tailles)

    # Afficher l'image capturée avec contours
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
