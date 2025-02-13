import cv2
import numpy as np
import time
import dearpygui.dearpygui as dpg


# Parametres pour le traitement des disques
CIRCULARITY_MIN = 0.8  # Pour definir si une forme est suffisamment ronde
AREA_MIN = 100         # Taille minimale pour filtrer les petits bruits
AREA_MAX_RATIO = 1.5   # Facteur pour eliminer les disques disproportionnes

# Variables globales

# Paramètres de marge d'erreur pour la comparaison de taille
MARGE_ERREUR = 5  # Par exemple 5 pixels

# Variables globales pour stocker les données

detected_discs = []
detected_frame = None


def capture_initial_image():
    """Capture une image brute depuis la camera."""
    cap = cv2.VideoCapture(0)

    # Attente pour stabiliser la camera
    time.sleep(1)

    # Lire plusieurs frames pour une capture stable
    for _ in range(5):
        ret, frame = cap.read()


    if not ret or frame is None:
        print("Erreur : Impossible de capturer l'image.")
        cap.release()
        return None

    # Verifier si l'image est noire
    if not np.any(frame):
        print("Erreur : L'image est noire.")

        cap.release()
        return None

    cap.release()
    return frame


def detect_and_classify_discs(frame):
    """Detecte et valide les disques dans l'image."""
    cv2.imshow("Etape 0 : Image brut", frame)
    cv2.waitKey(0)
    # Conversion en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Etape 1 : Niveaux de gris", gray)
    cv2.waitKey(0)

    # Appliquer un flou pour reduire le bruit
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imshow("Etape 2 : Flou applique", blurred)
    cv2.waitKey(0)

    smoothed = cv2.bilateralFilter(gray, 9, 75, 75)
    cv2.imshow("Filtre bilateral", smoothed)
    cv2.waitKey(0)

    # Appliquer un seuil binaire adaptatif
    thresholded = cv2.adaptiveThreshold(smoothed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 11, 2)
    cv2.imshow("Etape 3 : Seuil binaire", thresholded)

    cv2.waitKey(0)

    # Detecter les contours
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        print("Erreur : Aucun contour detecte.")
        return None

    # Visualisation des contours
    contour_frame = frame.copy()
    cv2.drawContours(contour_frame, contours, -1, (0, 255, 0), 2)
    cv2.imshow("Etape 4 : Contours detectes", contour_frame)
    cv2.waitKey(0)

    # Filtrer les contours pour detecter les disques
    disques = []
    areas = []
    valid_contours_frame = frame.copy()

    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        # Filtrer les petits contours
        if area < AREA_MIN:
            continue

        # Calculer la circularite
        if perimeter > 0:
            circularity = (4 * np.pi * area) / (perimeter ** 2)
            if circularity > CIRCULARITY_MIN:
                areas.append(area)
                (x, y), radius = cv2.minEnclosingCircle(contour)
                disques.append((int(radius), (int(x), int(y))))
                # Dessiner les contours valides
                cv2.drawContours(valid_contours_frame, [contour], -1, (0, 255, 0), 2)
            else:
                # Dessiner les contours rejetes
                cv2.drawContours(valid_contours_frame, [contour], -1, (0, 0, 255), 2)

    # Afficher les contours valides et rejetes
    cv2.imshow("Etape 5 : Contours valides et rejetes", valid_contours_frame)
    cv2.waitKey(0)


    # Trier les disques par rayon
    disques = sorted(disques, key=lambda d: d[0])
    print("Disques detectes :", [d[0] for d in disques])

    if len(disques) == 0:
        print("Erreur : Aucun disque valide detecte.")
        return None

    return disques


def display_centers_with_crosses(frame, disques):
    """Affiche les centres des disques avec des croix."""

    # Vérifier que l'image est valide
    if frame is None or not isinstance(frame, np.ndarray):
        print("Erreur : L'image fournie n'est pas valide.")
        return

    # Dessiner les croix sur une copie de l'image
    frame_copy = frame.copy()

    print(f"Nombre de disques détectés : {len(disques)}")

    for radius, (x, y) in disques:
        print(f"Dessin d'une croix au centre du disque à la position ({x}, {y}) avec un rayon de {radius}")
        # Dessine une croix au centre de chaque disque détecté
        cv2.drawMarker(frame_copy, (x, y), (0, 0, 255), cv2.MARKER_CROSS, markerSize=20, thickness=2)

    # Afficher l'image avec les croix
    cv2.imshow('Disques avec centres marqués', frame_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def send_data_to_other_program(number_of_discs):
    """Fonction simulant l'envoi de données à un autre programme."""
    print(f"Envoi des données : Nombre de disques = {number_of_discs}")


def confirm_detection_callback():
    """Callback pour confirmer la detection."""
    global detected_discs
    if detected_discs:
        print("Confirmation acceptée.")
        # Envoyer les données à un autre programme
        send_data_to_other_program(len(detected_discs))

    else:
        print("Aucun disque détecté.")
    dpg.stop_dearpygui()


def cancel_detection_callback():
    """Callback pour annuler la detection."""
    print("Confirmation refusée.")
    dpg.stop_dearpygui()


def initialize_game():
    """Lance le programme de vision."""
    global detected_discs, detected_frame

    # Capture de l'image

    frame = capture_initial_image()
    if frame is None:
        return

    # Detection et classification
    disques = detect_and_classify_discs(frame)
    if disques is None:
        return

    detected_discs = disques
    detected_frame = frame

    # Afficher les croix immédiatement
    display_centers_with_crosses(frame, disques)

    # Interface utilisateur pour confirmation
    dpg.create_context()
    dpg.create_viewport(title="Confirmation de detection", width=400, height=200)

    with dpg.window(label="Confirmation de detection", width=400, height=200):
        dpg.add_text(f"Nombre de disques detectes : {len(disques)}")
        dpg.add_button(label="Oui", callback=confirm_detection_callback)
        dpg.add_button(label="Non", callback=cancel_detection_callback)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


# Lancer le programme
initialize_game()
