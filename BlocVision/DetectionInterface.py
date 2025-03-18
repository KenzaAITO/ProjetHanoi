from PyQt6.QtWidgets import QApplication, QInputDialog
from CameraProcessor import CameraProcessor

# Paramètres pour le traitement des palets
CIRCULARITY_MIN = 0.8  # Seuil de circularité pour considérer une forme comme un palet
AREA_MIN = 100         # Taille minimale d'un palet pour éviter les faux positifs

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