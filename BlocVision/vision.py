import cv2
import numpy as np
import time
import tkinter as tk
from tkinter import simpledialog

# Paramètres pour le traitement des disques
CIRCULARITY_MIN = 0.8  # Seuil de circularité pour considérer une forme comme un disque
AREA_MIN = 100         # Taille minimale d'un disque pour éviter les faux positifs

class CameraProcessor:
    """
    Classe pour capturer une image depuis la caméra et détecter les disques présents dans l'image.
    """
    def __init__(self, camera_index=0):
        """
        Initialise la caméra.
        :param camera_index: Index de la caméra à utiliser
        """
        self.camera_index = camera_index

    def capture_image(self):
        """
        Capture une image brute depuis la caméra et effectue des vérifications pour s'assurer de sa validité.
        :return: L'image capturée sous forme de tableau NumPy ou None en cas d'erreur
        """
        cap = cv2.VideoCapture(self.camera_index)
        time.sleep(1)

        frame = None
        for _ in range(5):
            ret, frame = cap.read()
            if not ret or frame is None:
                print("Erreur : Impossible de capturer une image valide.")
                cap.release()
                return None
        
        cap.release()
        
        if not np.any(frame):
            print("Erreur : L'image capturée est vide ou noire.")
            return None
        
        return frame

    def detect_discs(self, frame):
        """
        Détecte les disques présents dans une image et affiche les étapes du traitement.
        :param frame: Image capturée
        :return: Nombre total de disques détectés, Liste des disques sous la forme [(rayon, (x, y))]
        """
        cv2.imshow("Étape 0 : Image brute", frame)
        cv2.waitKey(0)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Étape 1 : Conversion en niveaux de gris", gray)
        cv2.waitKey(0)

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        cv2.imshow("Étape 2 : Flou gaussien", blurred)
        cv2.waitKey(0)

        thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY_INV, 11, 2)
        cv2.imshow("Étape 3 : Seuil adaptatif", thresholded)
        cv2.waitKey(0)
        
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        contour_frame = frame.copy()
        cv2.drawContours(contour_frame, contours, -1, (0, 255, 0), 2)
        cv2.imshow("Étape 4 : Contours détectés", contour_frame)
        cv2.waitKey(0)

        disques = []
        valid_contours_frame = frame.copy()
        
        for contour in contours:
            if self.classify_contour(contour):

                (x, y), radius = cv2.minEnclosingCircle(contour)
                disques.append((int(radius), (int(x), int(y))))
                cv2.drawContours(valid_contours_frame, [contour], -1, (0, 255, 0), 2)
            else:
                cv2.drawContours(valid_contours_frame, [contour], -1, (0, 0, 255), 2)
        
        cv2.imshow("Étape 5 : Contours validés et rejetés", valid_contours_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        disques = sorted(disques, key=lambda d: d[0])
        return len(disques), disques
    
    def classify_contour(self, contour):
        """
        Vérifie si un contour correspond aux critères d'un disque valide.
        :param contour: Contour détecté
        :return: True si le contour est un disque valide, False sinon
        """
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if area < AREA_MIN or perimeter == 0:
            return False
        
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        return circularity > CIRCULARITY_MIN

class DetectionInterface:
    """
    Interface utilisateur pour afficher le nombre de disques détectés et permettre la validation ou modification.
    """
    def __init__(self, detected_count):
        self.detected_count = detected_count
        self.validated_count = None

    def show_interface(self):
        """
        Affiche une boîte de dialogue permettant à l'utilisateur de valider ou modifier le nombre de disques détectés.
        """
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre principale

        user_input = simpledialog.askinteger("Validation", 
                                             f"Nombre de disques détectés : {self.detected_count}\n"
                                             "Confirmez ou entrez le nombre correct :",
                                             minvalue=0)
        
        self.validated_count = user_input if user_input is not None else self.detected_count
        print(f"Nombre de disques validé par l'utilisateur : {self.validated_count}")
        return self.validated_count

if __name__ == "__main__":
    processor = CameraProcessor()
    frame = processor.capture_image()
    if frame is not None:
        num_discs, discs = processor.detect_discs(frame)
        interface = DetectionInterface(num_discs)
        # On considère validated_count comme le chiffre validé par l'user donc à utiliser pour notre jeu
        validated_count = interface.show_interface()
