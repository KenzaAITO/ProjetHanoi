import cv2
import numpy as np
from tkinter import Tk, Label, Button, messagebox

# Paramètres de marge d'erreur pour la comparaison de taille
MARGE_ERREUR = 5  # Par exemple 5 pixels

class Image:

def capture_initial_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Erreur : Impossible de capturer l'image depuis la caméra.")
        return None
    return frame

def detect_and_classify_discs(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Détecte les contours des disques
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Gestion de l'erreur si aucun contour n'est détecté
        if len(contours) == 0:
            print("Erreur : Aucun contour détecté, veuillez vérifier l'image.")
            return None

    # Stocke les tailles et positions des disques
    disques = []
    for contour in contours:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        area = cv2.contourArea(contour)
        # Ajouter la taille avec une marge d'erreur pour les variations
        disques.append((int(radius), (int(x), int(y))))

    # Classer les disques par taille en utilisant une marge d'erreur
    disques = sorted(disques, key=lambda d: d[0])
    print("Tailles des disques détectés (triés):", [d[0] for d in disques])

        return disques

    def display_centers_with_crosses(frame, disques):
        for radius, (x, y) in disques:
            # Dessine une croix au centre de chaque disque détecté
            cv2.drawMarker(frame, (x, y), (0, 0, 255), cv2.MARKER_CROSS, markerSize=20, thickness=2)
        cv2.imshow('Disques avec centres marqués', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def initialize_game():
    # Capture l'image initiale
    frame = capture_initial_image()
    if frame is None:
        print("Erreur : L'image initiale n'a pas pu être capturée.")
        return

        # Détecte et classe les disques
        disques = self.detect_and_classify_discs(frame)
        if disques is None:
            print("Erreur : La détection des disques a échoué.")
            return

    # Si tout est bon, lance le jeu en affichant les centres des disques avec des croix
    print("Initialisation réussie ! Les disques ont été détectés et classés.")
    display_centers_with_crosses(frame, disques)

