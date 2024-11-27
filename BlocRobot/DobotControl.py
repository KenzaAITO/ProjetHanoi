#!/usr/bin/env python

import sys
import time
sys.path.insert(1,'./DLL')
import DobotDllType as dType

AXE_X = 220

# Définir les messages de connexion
CON_STR = {
    dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
}

class DobotControl:
    def __init__(self, port="COM12", baudrate=115200, home_x=AXE_X, home_y=0, home_z=50):
        self.api = dType.load()
        self.connected = False
        self.port = port
        self.baudrate = baudrate
        self.home_x = home_x
        self.home_y = home_y
        self.home_z = home_z

    def connect(self):
        """Connexion au Dobot."""
        state = dType.ConnectDobot(self.api, self.port, self.baudrate)[0]
        if state == dType.DobotConnect.DobotConnect_NoError:
            print("Connexion réussie : {}".format(CON_STR[state]))
            self._initialize_parameters()
            self.connected = True
        else:
            print("Échec de la connexion : {}".format(CON_STR[state]))
        return self.connected

    def disconnect(self):
        """Déconnexion du Dobot."""
        if self.connected:
            dType.DisconnectDobot(self.api)
            print("Dobot déconnecté.")
            self.connected = False

    def _initialize_parameters(self):
        """Initialisation des paramètres du bras."""
        dType.SetQueuedCmdClear(self.api)
        dType.SetCmdTimeout(self.api, 1000)
        dType.SetPTPJointParams(self.api, 200, 200, 200, 200, 200, 200, 200, 200)
        dType.SetPTPCoordinateParams(self.api, 100, 100, 100, 100)
        dType.SetPTPCommonParams(self.api, 200, 200)
        dType.SetHOMECmd(self.api, temp=0, isQueued=1)

    def move_to(self, x, y, z, r=0, wait=True):
        """Déplacement vers une position spécifique."""
        dType.SetPTPCmd(self.api, 2, x, y, z, r, isQueued=1)
        if wait:
            self.attente_position(x, y, z)

    def attente_position(self, cible_x, cible_y, cible_z, tolerance=1.0):
        """Attendre que le bras atteigne une position donnée."""
        while True:
            pose = dType.GetPose(self.api)
            current_x, current_y, current_z = pose[0], pose[1], pose[2]
            if (abs(current_x - cible_x) < tolerance and
                abs(current_y - cible_y) < tolerance and
                abs(current_z - cible_z) < tolerance):
                break
            time.sleep(0.1)

    def activate_ventourse(self, activate=True):
        """Activer ou désactiver la ventouse."""
        dType.SetEndEffectorSuctionCup(self.api, enableCtrl=1, on=1 if activate else 0, isQueued=1)
        print("Ventouse activée" if activate else "Ventouse désactivée")

