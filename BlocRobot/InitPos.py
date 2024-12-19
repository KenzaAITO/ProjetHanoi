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

class Robot:
    def __init__(self):
        self.dobot = DobotControl()
        self.image = Image()

    def execute(self):
        try:
            if self.dobot.connect():
                for index, (x, y, z) in enumerate(positions):
                    print("Déplacement vers l'emplacement {} : X={}, Y={}, Z={}".format(index + 1, x, y, z))
                    
                    # Mouvement au-dessus de la position
                    self.dobot.move_to(x, y, 100)

                    # Initialisation de l'image
                    if index == 0:
                        self.image.initialize_game()
                    
                    # Mouvement à la position cible
                    self.dobot.move_to(x, y, z)
                    
                    # Activer la ventouse
                    self.dobot.activate_ventouse(True)
                    time.sleep(2)
                    
                    # Désactiver la ventouse
                    self.dobot.activate_ventouse(False)
                    
                    # Retour à une position sécurisée
                    self.dobot.move_to(x, y, 100)

                # Retour au point de départ
                print("Retour au point de départ.")
                self.dobot.move_to(self.dobot.home_x, self.dobot.home_y, self.dobot.home_z)

        except Exception as e:
            print("Une erreur s'est produite : {}".format(e))

if __name__ == "__main__":
    robot = Robot()
    robot.execute()
