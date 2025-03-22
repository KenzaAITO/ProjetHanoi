import sys
from PyQt6.QtWidgets import QApplication
import time
from BlocAlgo.HanoiIterative import HanoiIterative
from BlocVision.vision import CameraProcessor, DetectionInterface
from BlocRobot.DobotControl import DobotControl
from BlocRobot.InitPos import Robot
from BlocAlgo.SimulationMoves import SimulationMoves

def main():
    """
    Programme principal pour résoudre la Tour de Hanoï avec un robot et une caméra.
    """

    print("Program Start:")
    
    # === 1. INITIALISATION DES COMPOSANTS === 
    print("Initialisation du robot...")
    #robot = Robot()  # Création de l'instance du robot
    #robot.execute_init()

    print("Initialisation de la caméra...")
    processor = CameraProcessor()

    # === 2. ACQUISITION DE L'ÉTAT INITIAL ===
    print("Prise de photo pour analyser la tour d'origine...")
    frame = processor.capture_image()

    if frame is not None:
        detection_id = int(time.time())
        num_discs, _ = processor.detect_discs(frame, detection_id)
        print(f"Nombre de palets détectés : {num_discs}")
    
    #On valide mtn le nombre de palets par l'utilisateur 
    interface = DetectionInterface(num_discs)
    validated_count = interface.show_interface()


    # === 3. CALCUL DES DÉPLACEMENTS SELON L'ALGORITHME DE HANOÏ ===
    print("Calcul des déplacements...")
    #mouvements = hanoi_iteratif(validated_count)  # Génération de la liste des déplacements
    algo = HanoiIterative(validated_count)# print la matrice dans l'init

    app = QApplication(sys.argv)
    simulation = SimulationMoves(algo)
    simulation.show()

    # === 4. EXÉCUTION DES DÉPLACEMENTS PAR LE ROBOT ===
    #for move in mouvements:
        #coup, origine, destination, restants = move
        #print(f"Déplacement {coup}: {origine} → {destination} ({restants} palets restants)")
        
        # Déplacer le robot en fonction du mouvement généré

        #robot.DobotControl.deplacer_vers_colonne_gauche()
        #robot.DobotControl.deplacer_vers_colonne_droite()
        #robot.DobotControl.deplacer_vers_colonne_centre()
    
    sys.exit(app.exec())
    print("Résolution de la Tour de Hanoï terminée !")

if __name__ == "__main__":
    main()
    
#TODO: Fonction Déplacer
#TODO: Généré les données en transit


