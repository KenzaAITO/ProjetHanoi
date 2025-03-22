import cv2
import numpy as np
import time
import os
from datetime import datetime

# Paramètres pour le traitement des palets
CIRCULARITY_MIN = 0.8  # Seuil de circularité pour considérer une forme comme un palet
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

    def detect_discs(self, frame):
        """
        Détecte les palets présents dans une image et affiche les étapes du traitement.
        :param frame: Image capturée
        :return: Nombre total de palets détectés, Liste des palets sous la forme [(rayon, (x, y))]
        """
        cv2.imshow("Étape 0 : Image brute", frame)
        cv2.waitKey(1000)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Étape 1 : Conversion en niveaux de gris", gray)
        cv2.waitKey(1000)

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        cv2.imshow("Étape 2 : Flou gaussien", blurred)
        cv2.waitKey(1000)

        thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY_INV, 11, 2)
        cv2.imshow("Étape 3 : Seuil adaptatif", thresholded)
        cv2.waitKey(1000)
        
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        contour_frame = frame.copy()
        cv2.drawContours(contour_frame, contours, -1, (0, 255, 0), 2)
        cv2.imshow("Étape 4 : Contours détectés", contour_frame)
        cv2.waitKey(1000)

        palets = []
        valid_contours_frame = frame.copy()
        
        for contour in contours:
            if self.classify_contour(contour):
                (x, y), radius = cv2.minEnclosingCircle(contour)
                palets.append((int(radius), (int(x), int(y))))
                cv2.drawContours(valid_contours_frame, [contour], -1, (0, 255, 0), 2)
            else:
                cv2.drawContours(valid_contours_frame, [contour], -1, (0, 0, 255), 2)
        
        cv2.imshow("Étape 5 : Contours validés et rejetés", valid_contours_frame)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()

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

    def save_detection_images(self, frame, detection_id):
        """
        Sauvegarde l'image de la détection dans un dossier spécifique.
        :param frame: Image capturée
        :param detection_id: Identifiant unique pour la détection
        """
        folder_name = f"detections/detection_{detection_id}"
        os.makedirs(folder_name, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(folder_name, f"capture_{timestamp}.png")
        
        cv2.imwrite(file_path, frame)
        print(f"Image sauvegardée : {file_path}")

if __name__ == "__main__":
    processor = CameraProcessor()
    frame = processor.capture_image()
    print(f"Capture image")
    if frame is not None:
        num_discs, _ = processor.detect_discs(frame)
        print(f"Nombre de palets détectés : {num_discs}")
        processor.save_detection_images(frame, int(time.time()))
