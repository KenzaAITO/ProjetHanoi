import cv2
import numpy as np
import time

class CameraProcessor:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.detected_discs = []

    def capture_image(self):
        """Capture une image brute depuis la caméra."""
        cap = cv2.VideoCapture(self.camera_index)
        time.sleep(1)

        for _ in range(5):
            ret, frame = cap.read()

        cap.release()

        if not ret or frame is None or not np.any(frame):
            print("Erreur : Impossible de capturer une image valide.")
            return None
        
        cv2.imshow("Étape 0 : Image brute", frame)
        cv2.waitKey(0)
        return frame

    def detect_discs(self, frame):
        """Détecte et valide les disques dans une image."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Étape 1 : Conversion en niveaux de gris", gray)
        cv2.waitKey(0)

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        cv2.imshow("Étape 2 : Application du flou gaussien", blurred)
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
        
        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            
            if area < 100 or perimeter == 0:
                continue
            
            circularity = (4 * np.pi * area) / (perimeter ** 2)
            if circularity > 0.8:
                (x, y), radius = cv2.minEnclosingCircle(contour)
                disques.append((int(radius), (int(x), int(y))))
        
        self.detected_discs = sorted(disques, key=lambda d: d[0])
        return self.detected_discs

    def display_detected_discs(self, frame):
        """Affiche les disques détectés avec des croix au centre."""
        frame_copy = frame.copy()
        for radius, (x, y) in self.detected_discs:
            cv2.drawMarker(frame_copy, (x, y), (0, 0, 255), cv2.MARKER_CROSS, markerSize=20, thickness=2)
        
        cv2.imshow('Étape 5 : Disques détectés', frame_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    processor = CameraProcessor()
    frame = processor.capture_image()
    if frame is not None:
        discs = processor.detect_discs(frame)
        if discs:
            processor.display_detected_discs(frame)
        else:
            print("Aucun disque détecté.")
