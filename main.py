""" 
import sys
import os

# Ajouter le chemin du dossier contenant DobotDllType.py
sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))

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
from BlocVision.vision import initialize_game
import BlocRobot.InitPos as init              # Importation de la classe Robot
from BlocAlgo.algo import hanoi_iteratif  # Importation de l'algorithme de la tour de Hanoï


def main():
    """
    Programme principal pour résoudre la Tour de Hanoï avec un robot et une caméra.
    """

    print("Program Start:")
    
    # === 1. INITIALISATION DES COMPOSANTS === 
    print("Initialisation du robot...")
    #robot = Robot()  # Création de l'instance du robot
    intialisation = init.Robot()

    print("Initialisation de la caméra...")
    #camera = Vision()  # La camera n'a pas encore de classe TO DO 
    #intialisation.init() 

    initialize_game()

    # === 2. ACQUISITION DE L'ÉTAT INITIAL ===
    print("Prise de photo pour analyser la tour d'origine...")
    nb_palet_camera = camera.detecter_nombre_palets()  # Détection du nombre de palets sur l'axe d'origine

    if nb_palet_camera == 0:
        print("Erreur : Aucun palet détecté. Vérifiez la caméra.")
        return

    print(f"Nombre de palets détectés : {nb_palet_camera}")

    # === 3. CALCUL DES DÉPLACEMENTS SELON L'ALGORITHME DE HANOÏ ===
    print("Calcul des déplacements...")
    mouvements = hanoi_iteratif(nb_palet_camera)  # Génération de la liste des déplacements

    print(f"{len(mouvements)} déplacements générés.")

    # === 4. EXÉCUTION DES DÉPLACEMENTS PAR LE ROBOT ===
    for move in mouvements:
        coup, origine, destination, restants = move
        print(f"Déplacement {coup}: {origine} → {destination} ({restants} palets restants)")
        
        # Déplacer le robot en fonction du mouvement généré
        robot.deplacer(origine, destination)

    print("Résolution de la Tour de Hanoï terminée !")

if __name__ == "__main__":
    main()
