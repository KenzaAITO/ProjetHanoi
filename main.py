""" 
import sys
import os


import BlocVision.vision as vision
from BlocVision.vision import initialize_game
import BlocRobot.InitPos as init

def main():
    print("Program Start:")
    #partie initialisation 
    intialisation = init.Robot()
    #intialisation.init() 

    initialize_game()

    #lancement de l'interface
    

    
if __name__ == "__main__":
    main()
   """  



import BlocVision.vision as vision            # Importation de la classe Vision
import BlocRobot.InitPos as init              # Importation de la classe Robot
from BlocAlgo.algo import hanoi_iteratif  # Importation de l'algorithme de la tour de Hanoï
import BlocRobot.DobotControl as robot

def main():
    """
    Programme principal pour résoudre la Tour de Hanoï avec un robot et une caméra.
    """

    print("Program Start:")
    
    # === 1. INITIALISATION DES COMPOSANTS === 
    print("Initialisation du robot...")
    #robot = Robot()  # Création de l'instance du robot
    init.Robot()
    #boucle pour afficher que tous est correct 

    print("Initialisation de la caméra...")
    #camera = Vision()  # La camera n'a pas encore de classe TO DO 
    #intialisation.init() 
    vision.initialize_game()

    # === 2. ACQUISITION DE L'ÉTAT INITIAL ===
    print("Prise de photo pour analyser la tour d'origine...")
    #vision = vision.capture_initial_image()

    nb_palet_camera = vision.display_nb_disques()

    if nb_palet_camera == 0:
        print("Erreur : Aucun palet détecté. Vérifiez la caméra.")
        return

    print(f"Nombre de palets détectés : {nb_palet_camera}")

    # === 3. CALCUL DES DÉPLACEMENTS SELON L'ALGORITHME DE HANOÏ ===
    print("Calcul des déplacements...")
    mouvements = hanoi_iteratif(nb_palet_camera)  # Génération de la liste des déplacements

    #print(f"{len(mouvements)} déplacements générés.")

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
#TODO: Fonction 
#TODO: Généré les données en transit
#TODO: Généré la liste des mouvements (position)

