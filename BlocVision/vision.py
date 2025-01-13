import cv2
import numpy as np
import time
import dearpygui.dearpygui as dpg

# Paramètres de marge d'erreur pour la comparaison de taille
MARGE_ERREUR = 5  # Par exemple 5 pixels

# Variables globales pour stocker les données
detected_discs = []
detected_frame = None



def capture_initial_image():
    cap = cv2.VideoCapture(0)

    # Attendre un moment pour s'assurer que la caméra est prête
    time.sleep(1)  # Attendre 1 seconde

    # Lire plusieurs frames pour stabiliser la capture
    for _ in range(5):
        ret, frame = cap.read()

    if not ret or frame is None:
        print("Erreur : Impossible de capturer l'image depuis la caméra.")
        cap.release()
        return None

    # Vérifier si l'image est noire
    if not np.any(frame):  # Vérifie si tous les pixels sont à 0
        print("Erreur : L'image capturée est noire. Veuillez vérifier la caméra.")
        cap.release()
        return None

    cap.release()
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
        perimeter = cv2.arcLength(contour, True)
        
        # Filtrer les petits contours (bruit) en définissant une taille minimum raisonnable
        if area > 100:  # Ajuster cette valeur si nécessaire
            # Vérifier la circularité du contour
            if perimeter > 0:  # Éviter la division par zéro
                circularity = (4 * np.pi * area) / (perimeter ** 2)
                if circularity > 0.8:  # Seuil pour définir un disque (ajuster si nécessaire)
                    disques.append((int(radius), (int(x), int(y))))
                else:
                    print(f"Contour rejeté (pas assez circulaire) : Circularité = {circularity:.2f}")
            else:
                print("Contour rejeté (périmètre nul).")

    # Vérifier que des disques sont bien détectés
    if len(disques) == 0:
        print("Erreur : Aucun disque détecté après filtrage, vérifiez l'image.")
        return None

    # Classer les disques par taille en utilisant une marge d'erreur
    disques = sorted(disques, key=lambda d: d[0])
    print("Tailles des disques détectés (triés):", [d[0] for d in disques])

        return disques

def display_centers_with_crosses(frame, disques):
    # Vérifier que l'image est valide
    if frame is None or not isinstance(frame, np.ndarray):
        print("Erreur : L'image fournie n'est pas valide.")
        return

    # Dessiner les croix sur une copie de l'image pour éviter des modifications non voulues
    frame_copy = frame.copy()

    for radius, (x, y) in disques:
        # Dessine une croix au centre de chaque disque détecté
        cv2.drawMarker(frame_copy, (x, y), (0, 0, 255), cv2.MARKER_CROSS, markerSize=20, thickness=2)

    # Assurez-vous que les fenêtres OpenCV précédentes sont fermées
    cv2.destroyAllWindows()

    # Afficher l'image avec les croix
    cv2.imshow('Disques avec centres marqués', frame_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Interface avec Dear PyGui 2.0.0
def confirm_detection_callback():
    global detected_discs, detected_frame
    if detected_discs:
        print("Confirmation acceptée.")
        display_centers_with_crosses(detected_frame, detected_discs)
    else:
        print("Aucun disque détecté.")
    dpg.stop_dearpygui()

def cancel_detection_callback():
    print("Confirmation refusée. Relancez l'initialisation.")
    dpg.stop_dearpygui()

def initialize_game():
    global detected_discs, detected_frame

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

    # Si tout est bon, ouvre l'interface graphique pour confirmation
    detected_discs = disques
    detected_frame = frame

    dpg.create_context()
    dpg.create_viewport(title="Confirmation de détection", width=400, height=200)

    with dpg.window(label="Confirmation de détection", width=400, height=200):
        dpg.add_text(f"Nous avons détecté {len(disques)} disques. Est-ce correct ?")
        dpg.add_button(label="Oui", callback=confirm_detection_callback)
        dpg.add_button(label="Non", callback=cancel_detection_callback)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

