#!/usr/bin/env python

import sys
import time
sys.path.insert(1, './DLL')
import DobotDllType as dType

AXE_X = 220

# Définir les messages de connexion
CON_STR = {
    dType.DobotConnect.DobotConnect_NoError: "Connexion réussie",
    dType.DobotConnect.DobotConnect_NotFound: "Dobot non trouvé",
    dType.DobotConnect.DobotConnect_Occupied: "Port occupé"
}

class DobotControl:
    def __init__(self, port="COM7", baudrate=115200, home_x=AXE_X, home_y=0, home_z=50):
        """
        Initialise le contrôle Dobot.
        :param port: Port COM pour la connexion
        :param baudrate: Taux de transfert en bauds
        :param home_x, home_y, home_z: Position initiale du bras
        """
        self.api = dType.load()
        self.connected = False
        self.port = port
        self.baudrate = baudrate
        self.home_x = home_x
        self.home_y = home_y
        self.home_z = home_z

    def connect(self):
        """Connexion au Dobot."""
        try:
            state = dType.ConnectDobot(self.api, self.port, self.baudrate)[0]
            if state == dType.DobotConnect.DobotConnect_NoError:
                print(CON_STR[state])
                self._initialize_parameters()
                self.connected = True
            else:
                print(CON_STR[state])
            return self.connected
        except Exception as e:
            print(f"Erreur lors de la connexion : {e}")
            return False

    def disconnect(self):
        """Déconnexion du Dobot."""
        try:
            if self.connected:
                dType.DisconnectDobot(self.api)
                print("Dobot déconnecté.")
                self.connected = False
        except Exception as e:
            print(f"Erreur lors de la déconnexion : {e}")

    def _initialize_parameters(self):
        """Initialisation des paramètres du bras."""
        try:
            dType.SetQueuedCmdClear(self.api)
            dType.SetCmdTimeout(self.api, 1000)
            dType.SetPTPJointParams(self.api, 200, 200, 200, 200, 200, 200, 200, 200)
            dType.SetPTPCoordinateParams(self.api, 100, 100, 100, 100)
            dType.SetPTPCommonParams(self.api, 200, 200)
            dType.SetHOMECmd(self.api, temp=0, isQueued=1)
        except Exception as e:
            print(f"Erreur lors de l'initialisation des paramètres : {e}")

    def move_to(self, x, y, z, r=0, wait=True):
        """Déplacement vers une position spécifique."""
        try:
            dType.SetPTPCmd(self.api, 2, x, y, z, r, isQueued=1)
            if wait:
                self.attente_position(x, y, z)
        except Exception as e:
            print(f"Erreur lors du déplacement : {e}")

    def attente_position(self, cible_x, cible_y, cible_z, tolerance=1.0):
        """Attendre que le bras atteigne une position donnée."""
        try:
            while True:
                pose = dType.GetPose(self.api)
                current_x, current_y, current_z = pose[0], pose[1], pose[2]
                if (abs(current_x - cible_x) < tolerance and
                    abs(current_y - cible_y) < tolerance and
                    abs(current_z - cible_z) < tolerance):
                    break
                time.sleep(0.1)
        except Exception as e:
            print(f"Erreur lors de l'attente de position : {e}")

    def activate_ventouse(self, activate=True):
        """Activer ou désactiver la ventouse."""
        try:
            dType.SetEndEffectorSuctionCup(self.api, enableCtrl=1, on=1 if activate else 0, isQueued=1)
            print("Ventouse activée" if activate else "Ventouse désactivée")
        except Exception as e:
            print(f"Erreur lors de l'activation de la ventouse : {e}")

    def __del__(self):
        """Destructeur pour déconnecter proprement."""
        self.disconnect()
