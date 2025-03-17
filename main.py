#import BlocVision.vision as vision            # Importation de la classe Vision
#import BlocRobot.DobotControl as robot
#import BlocRobot.InitPos as init              # Importation de la classe Robot

from BlocAlgo.algo import hanoi_iteratif  # Importation de l'algorithme de la tour de Hanoï
from BlocVision.vision import CameraProcessor, DetectionInterface
from BlocRobot.DobotControl import DobotControl
from BlocRobot.InitPos import Robot

def main():
    """
    Programme principal pour résoudre la Tour de Hanoï avec un robot et une caméra.
    """

    print("Program Start:")
    
    # === 1. INITIALISATION DES COMPOSANTS === 
    print("Initialisation du robot...")
    #robot = Robot()  # Création de l'instance du robot
    #init.Robot()
    #boucle pour afficher que tous est correct 

    print("Initialisation de la caméra...")
    #intialisation.init() 
    #vision.initialize_game()
    processor = CameraProcessor()

    # === 2. ACQUISITION DE L'ÉTAT INITIAL ===
    print("Prise de photo pour analyser la tour d'origine...")
    frame = processor.capture_image()

    if frame is not None:
        num_discs, _ = processor.detect_discs(frame)
        print(f"Nombre de palets détectés : {num_discs}")
        # if num_discs == 0:
        #     print("Erreur : Aucun palet détecté. Vérifiez la caméra.")
        #     return
    
    #On valide mtn le nombre de palets par l'utilisateur 
    interface = DetectionInterface(num_discs)
    validated_count = interface.show_interface()

    #nb_palet_camera = vision.display_nb_palets()

    # === 3. CALCUL DES DÉPLACEMENTS SELON L'ALGORITHME DE HANOÏ ===
    print("Calcul des déplacements...")
    mouvements = hanoi_iteratif(validated_count)  # Génération de la liste des déplacements


    print(f"{len(mouvements)} déplacements générés.")

    # === 4. EXÉCUTION DES DÉPLACEMENTS PAR LE ROBOT ===
    #for move in mouvements:
        #coup, origine, destination, restants = move
        #print(f"Déplacement {coup}: {origine} → {destination} ({restants} palets restants)")
        
        # Déplacer le robot en fonction du mouvement généré

        #robot.DobotControl.deplacer_vers_colonne_gauche()
        #robot.DobotControl.deplacer_vers_colonne_droite()
        #robot.DobotControl.deplacer_vers_colonne_centre()

    print("Résolution de la Tour de Hanoï terminée !")

if __name__ == "__main__":
    main()
    
#TODO: Fonction Déplacer
#TODO: Généré les données en transit
#TODO: Généré la liste des mouvements (position)

