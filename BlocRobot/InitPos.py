#!/usr/bin/env python

import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'BlocRobot')))
from DobotControl import DobotControl
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from BlocVision.vision import Image


AXE_X = 220

# Définir les positions
positions = [
    (AXE_X, -200, -70),  # Emplacement Gauche
    (AXE_X, 0, -70),     # Emplacement Centre
    (AXE_X, 200, -70)    # Emplacement Droite
]
class Robot :
    def init(self):
        dobot = DobotControl()
        image = Image()
        try:
            if dobot.connect():
                for index, (x, y, z) in enumerate(positions):
                    print("Déplacement vers l'emplacement {} : X={}, Y={}, Z={}".format(index + 1, x, y, z))
                    
                    # Mouvement au-dessus de la position
                    dobot.move_to(x, y, 100)

                    # Initialisation de l'image
                    if(index == 0):
                        image.initialize_game()
                    
                    # Mouvement à la position cible
                    dobot.move_to(x, y, z)
                    
                    # Activer la ventouse
                    dobot.activate_ventouse(True)
                    time.sleep(2)
                    
                    # Désactiver la ventouse
                    dobot.activate_ventouse(False)
                    
                    # Retour à une position sécurisée
                    dobot.move_to(x, y, 100)

                # Retour au point de départ
                print("Retour au point de départ.")
                dobot.move_to(dobot.home_x, dobot.home_y, dobot.home_z)

        except Exception as e:
            print("Une erreur s'est produite : {}".format(e))

if __name__ == "__main__":
    Robot.Init()
