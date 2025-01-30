#!/usr/bin/env python

import sys
import os
import time
from DobotControl import DobotControl
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from BlocVision.vision import Image

class Robot:
    def __init__(self):
        #Initialise le robot en connectant le Dobot et en préparant l'interface image.
        self.dobot = DobotControl()
        #self.image = Image()

    def execute_init(self):
        
        #Exécute les mouvements et opérations nécessaires pour chaque position définie.
        try:
            for index in 0,1,2:

                # Mouvement au-dessus de la position
                if(index == 0):
                    self.dobot.deplacer_vers_colonne_droite()
                    self.dobot.grab_pallet(5, True)
                    self.dobot.grab_pallet(5, False)
                if(index == 1):
                    self.dobot.deplacer_vers_colonne_centre(0)

                if(index == 2):
                    self.dobot.deplacer_vers_colonne_gauche(0)

                # Initialisation de l'image si à la première position
                #if index == 0:
                #     self.image.initialize_game()

                # Activer la ventouse pour ramasser
                self.dobot.activate_ventouse(True)

                time.sleep(1)

                # Désactiver la ventouse pour déposer
                self.dobot.activate_ventouse(False)

            # Retour au point de départ
            print("Retour au point de départ.")
            self.dobot.return_to_home()

        except Exception as e:
            print(f"Une erreur s'est produite : {e}")


if __name__ == "__main__":
    robot = Robot()
    robot.execute_init()
    robot.dobot.disconnect()
