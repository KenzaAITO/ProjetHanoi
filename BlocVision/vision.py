import cv2
import numpy as np
import time
import os
from PyQt6.QtWidgets import QApplication, QInputDialog

# Paramètres pour le traitement des palets
CIRCULARITY_MIN = 0.6  # Seuil de circularité pour considérer une forme comme un palet
AREA_MIN = 100         # Taille minimale d'un palet pour éviter les faux positifs

class CameraProcessor:
    """
    Classe pour capturer une image depuis la caméra et détecter les palets présents dans l'image.
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

    def detect_discs(self, frame, detection_id):
        """
        Détecte les palets présents dans une image et sauvegarde les étapes du traitement.
        :param frame: Image capturée
        :param detection_id: Identifiant unique pour la détection
        :return: Nombre total de palets détectés, Liste des palets sous la forme [(rayon, (x, y))]
        """
        folder_name = f"detections/detection_{detection_id}"
        os.makedirs(folder_name, exist_ok=True)

        cv2.imwrite(os.path.join(folder_name, "step_0_raw.png"), frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.join(folder_name, "step_1_gray.png"), gray)

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        cv2.imwrite(os.path.join(folder_name, "step_2_blur.png"), blurred)

        thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY_INV, 11, 2)
        cv2.imwrite(os.path.join(folder_name, "step_3_threshold.png"), thresholded)
        
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        contour_frame = frame.copy()
        cv2.drawContours(contour_frame, contours, -1, (0, 255, 0), 2)
        cv2.imwrite(os.path.join(folder_name, "step_4_contours.png"), contour_frame)

        palets = []
        valid_contours_frame = frame.copy()
        
        for contour in contours:
            if self.classify_contour(contour):
                (x, y), radius = cv2.minEnclosingCircle(contour)
                palets.append((int(radius), (int(x), int(y))))
                cv2.drawContours(valid_contours_frame, [contour], -1, (0, 255, 0), 2)
            else:
                cv2.drawContours(valid_contours_frame, [contour], -1, (0, 0, 255), 2)
        
        cv2.imwrite(os.path.join(folder_name, "step_5_validated_contours.png"), valid_contours_frame)
        
        palets = sorted(palets, key=lambda d: d[0])
        return len(palets), palets
    
    
    def classify_contour(self, contour):
        """
        Vérifie si un contour correspond aux critères d'un palet valide.
        :param contour: Contour détecté
        :return: True si le contour est un palet valide, False sinon
        """
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if area < AREA_MIN or perimeter == 0:
            return False
        
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        return circularity > CIRCULARITY_MIN

class DetectionInterface:
    """
    Interface utilisateur avec PyQt6 pour afficher le nombre de palets détectés
    et permettre la validation ou modification.
    """
    def __init__(self, detected_count):
        self.detected_count = detected_count
        self.validated_count = None

    def show_interface(self):
        """
        Affiche une boîte de dialogue permettant à l'utilisateur de valider ou modifier le nombre de palets détectés.
        """
        app = QApplication([])  # Création de l'application PyQt6

        user_input, ok = QInputDialog.getInt(
            None, "Validation",
            f"Nombre de palets détectés : {self.detected_count}\n"
            "Confirmez ou entrez le nombre correct :",
            min= self.detected_count
        )
        
        if ok:
            self.validated_count = user_input
        else:
            self.validated_count = self.detected_count
        
        print(f"Nombre de palets validé par l'utilisateur : {self.validated_count}")
        return self.validated_count

if __name__ == "__main__":
    processor = CameraProcessor()
    frame = processor.capture_image()
    print(f"Capture image")
    if frame is not None:
        num_discs, _ = processor.detect_discs(frame)
        print(f"Nombre de palets détectés : {num_discs}")

        interface = DetectionInterface(num_discs)
        validated_count = interface.show_interface()