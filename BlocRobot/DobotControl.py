#!/usr/bin/env python

import time
from serial.tools import list_ports
import pydobot


class DobotControl:
    
    def __init__(self, home_x=220, home_y=0, home_z=100):
        #Initialise le contrôle Dobot.
        self.ERROR_NOT_CONNECTED = "Le Dobot n'est pas connecte."
        self.ERROR_INVALID_PALLET_COUNT = "Nombre de palets invalide"
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
        self.cible_x = 220
        self.cible_y = 0
        self.cible_z = 0
        self.device.move_to(home_x, home_y, home_z, 0, True)


    def deplacer_vers_colonne_gauche(self, r=0, wait=True):
        #Déplacement vers une position spécifique.
        self.cible_x = 220
        self.cible_y = -150
            
        if not self.connected:
            raise RuntimeError(self.ERROR_NOT_CONNECTED)

        print(f"Déplacement vers x={self.cible_x}, y={150}, z={self.cible_z}, r={r}")
        self.device.move_to(self.cible_x, self.cible_y, 150, r, wait)

    def deplacer_vers_colonne_centre(self, r=0, wait=True):
        #Déplacement vers une position spécifique.
        self.cible_x = 220
        self.cible_y = 0
            
        if not self.connected:
            raise RuntimeError(self.ERROR_NOT_CONNECTED)

        print(f"Déplacement vers x={self.cible_x}, y={150}, z={self.cible_z}, r={r}")
        self.device.move_to(self.cible_x, self.cible_y, 150, r, wait)
    
    def deplacer_vers_colonne_droite(self, r=0, wait=True):
        #Déplacement vers une position spécifique.
        self.cible_x = 220
        self.cible_y = 150
        
        if not self.connected:
            raise RuntimeError(self.ERROR_NOT_CONNECTED)

        print(f"Déplacement vers x={self.cible_x}, y={150}, z={self.cible_z}, r={r}")
        self.device.move_to(self.cible_x, self.cible_y, 150, r, wait)

    def grab_pallet(self, nb_palet, r=0, wait=True, grab=True):
        print(f"Nombre de palets à saisir : {nb_palet}")
        #Saisir un palet.
        if(grab == False):
            nb_palet += 1;  # Ajout du palet à déposer
        match nb_palet:
            case 0:
                self.cible_z = -80
            case 1:
                self.cible_z = -55
            case 2:
                self.cible_z = -30
            case 3:
                self.cible_z = -5
            case 4:
                self.cible_z = 20
            case 5:
                self.cible_z = 50
            case _:
                raise ValueError(self.ERROR_INVALID_PALLET_COUNT)
        
        print(f"Position actuelle : x={self.cible_x}, y={self.cible_y}, z={self.cible_z}, r={r}")

        if not self.connected:
            raise RuntimeError(self.ERROR_NOT_CONNECTED)
        self.device.move_to(self.cible_x, self.cible_y, self.cible_z, r, wait)
        self.activate_ventouse(grab)
        if grab:
            print("Palet saisi")
        else:
            print("Palet déposé")
        self.device.move_to(self.cible_x, self.cible_y, 150, r, wait)

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
        self.device.move_to(self.home_x, 150, self.home_z, r=0, wait=True)

    def disconnect(self):
        #Deconnexion propre du Dobot.
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