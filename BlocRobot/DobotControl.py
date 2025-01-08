#!/usr/bin/env python

import time
from serial.tools import list_ports
import pydobot

cible_x = 220
cible_y = 0
cible_z = 0

class DobotControl:
    
    def __init__(self, home_x=220, home_y=0, home_z=0):
        #Initialise le contrôle Dobot.
        self.ERROR_NOT_CONNECTED = "Le Dobot n'est pas connecte."
        available_ports = list_ports.comports()
        if not available_ports:
            raise RuntimeError("Aucun port disponible pour connecter le Dobot.")
        print(f'available ports: {[x.device for x in available_ports]}')

        self.port = available_ports[4].device  # Choisir le port approprié
        print(f"Connexion au port : {self.port}")
        self.device = pydobot.Dobot(port=self.port, verbose=True)
        self.connected = True
        self.home_x = home_x
        self.home_y = home_y
        self.home_z = home_z

    def deplacer_vers_colonne_gauche(self, r=0, wait=True):
        #Déplacement vers une position spécifique.
        cible_x = 220
        cible_y = -150
        cible_z = -20
        if not self.connected:
            raise RuntimeError(self.ERROR_NOT_CONNECTED)

        print(f"Déplacement vers x={cible_x}, y={cible_y}, z={cible_z}, r={r}")
        self.device.move_to(cible_x, cible_y, 100, r, wait)
        self.device.move_to(cible_x, cible_y, cible_z, r, wait)

    def deplacer_vers_colonne_centre(self, r=0, wait=True):
        #Déplacement vers une position spécifique.
        cible_x = 220
        cible_y = 0
        cible_z = -20
        if not self.connected:
            raise RuntimeError(self.ERROR_NOT_CONNECTED)

        print(f"Déplacement vers x={cible_x}, y={cible_y}, z={cible_z}, r={r}")
        self.device.move_to(cible_x, cible_y, 100, r, wait)
        self.device.move_to(cible_x, cible_y, cible_z, r, wait)
    
    def deplacer_vers_colonne_droite(self, r=0, wait=True):
        #Déplacement vers une position spécifique.
        cible_x = 220
        cible_y = 150
        cible_z = -20
        if not self.connected:
            raise RuntimeError(self.ERROR_NOT_CONNECTED)

        print(f"Déplacement vers x={cible_x}, y={cible_y}, z={cible_z}, r={r}")
        self.device.move_to(cible_x, cible_y, 100, r, wait)
        self.device.move_to(cible_x, cible_y, cible_z, r, wait)

    def activate_ventouse(self, activate=True):
        #Activer ou désactiver la ventouse.
        if not self.connected:
            raise RuntimeError(self.ERROR_NOT_CONNECTED)

        self.device.suck(activate)
        print("Ventouse activee" if activate else "Ventouse désactivee")

    def get_pose(self):
        #Obtenir la position actuelle du Dobot.
        if not self.connected:
            raise RuntimeError(self.ERROR_NOT_CONNECTED)

        pose = self.device.pose()
        print(f"Position actuelle: x={pose[0]}, y={pose[1]}, z={pose[2]}, r={pose[3]}")
        return pose

    def return_to_home(self):
        #Retour a la position initiale (home).
        print(f"Retour à la position de depart : x={self.home_x}, y={self.home_y}, z={self.home_z}")
        self.device.move_to(self.home_x, self.home_y, self.home_z, r=0, wait=True)

    def disconnect(self):
        """Deconnexion propre du Dobot."""
        if self.connected:
            print("Deconnexion du Dobot.")
            self.device.close()
            self.connected = False

    def __del__(self):
        """Destructeur pour deconnecter proprement."""
        self.disconnect()


# if __name__ == "__main__":
    # try:
    #     # Initialisation du contrôleur
    #     dobot = DobotControl()

    #     # Obtenir la position actuelle
    #     pose = dobot.get_pose()

    #     # Déplacement test
    #     dobot.move_to(pose[0] + 20, pose[1], pose[2])
    #     dobot.move_to(pose[0], pose[1], pose[2])

    #     # Activer et désactiver la ventouse
    #     dobot.activate_ventouse(True)
    #     time.sleep(2)
    #     dobot.activate_ventouse(False)

    #     # Retour à la position initiale
    #     dobot.return_to_home()

    # except Exception as e:
    #     print(f"Erreur : {e}")

    # finally:
    #     # Nettoyage final
    #     if 'dobot' in locals():
    #         dobot.disconnect()