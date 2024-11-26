import cv2
import numpy as np
from tkinter import Tk, Label, Button, messagebox

# Paramètres de marge d'erreur pour la comparaison de taille
MARGE_ERREUR = 5  # Par exemple 5 pixels

def capture_initial_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Erreur : Impossible de capturer l'image depuis la caméra.")
        return None
    cv2.imshow("Image capturée", frame)  # Affiche l'image capturée pour vérifier
    cv2.waitKey(0)
    return frame

def detect_and_classify_discs(frame):
    # Convertir en niveaux de gris et appliquer un flou pour réduire le bruit
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Appliquer un seuil adaptatif pour gérer différents niveaux de lumière
    thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                        cv2.THRESH_BINARY_INV, 11, 2)
    
    # Affiche l'image après seuil pour vérifier visuellement
    cv2.imshow("Image seuil", thresholded)
    cv2.waitKey(0)

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
        
        # Filtrer les petits contours (bruit) en définissant une taille minimum raisonnable
        if area > 100:  # Ajuster cette valeur si nécessaire
            disques.append((int(radius), (int(x), int(y))))

    # Vérifier que des disques sont bien détectés
    if len(disques) == 0:
        print("Erreur : Aucun disque détecté après filtrage, vérifiez l'image.")
        return None

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

# Interface utilisateur avec Tkinter
def create_gui(disques, frame):
    def on_confirm():
        messagebox.showinfo("Confirmation", "Détection validée. Passage à l'étape suivante.")
        root.destroy()
        display_centers_with_crosses(frame, disques)

    def on_cancel():
        messagebox.showerror("Erreur", "Détection non validée. Relancez l'initialisation.")
        root.destroy()

    root = Tk()
    root.title("Confirmation de la détection")
    root.geometry("400x200")

    label = Label(root, text=f"Nous avons détecté {len(disques)} disques. Est-ce correct ?", font=("Arial", 14))
    label.pack(pady=20)

    button_yes = Button(root, text="Oui", command=on_confirm, font=("Arial", 12), bg="green", fg="white", width=10)
    button_yes.pack(side="left", padx=50, pady=20)

    button_no = Button(root, text="Non", command=on_cancel, font=("Arial", 12), bg="red", fg="white", width=10)
    button_no.pack(side="right", padx=50, pady=20)

    root.mainloop()

def initialize_game():
    # Capture l'image initiale
    frame = capture_initial_image()
    if frame is None:
        print("Erreur : L'image initiale n'a pas pu être capturée.")
        return

    # Détecte et classe les disques
    disques = detect_and_classify_discs(frame)
    if disques is None:
        print("Erreur : La détection des disques a échoué.")
        return

    # Si tout est bon, demande confirmation via l'interface utilisateur
    print("Initialisation réussie ! Les disques ont été détectés et classés.")
    create_gui(disques, frame)

# Lancer l'initialisation du jeu
initialize_game()
