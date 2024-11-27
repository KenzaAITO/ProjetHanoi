#Magician
import time
import sys
sys.path.insert(1,'./DLL')
import DobotDllType as dType

# Fonction pour attendre que le bras arrive � la position cible
def attendre_position(api, cible_x, cible_y, cible_z, tolerance=1.0):
    while True:
        pose = dType.GetPose(api)
        current_x, current_y, current_z = pose[0], pose[1], pose[2]

        # V�rifier si la position actuelle est proche de la cible avec une tol�rance
        if (abs(current_x - cible_x) < tolerance and 
            abs(current_y - cible_y) < tolerance and 
            abs(current_z - cible_z) < tolerance):
            break
        time.sleep(0.1)  # Attendre un peu avant de v�rifier � nouveau

#Initialisation des positions
def InitPos():
    api = dType.load()  # Charger l'API

    # D�finir la vitesse et l'acc�l�ration des mouvements
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200)  # Vitesse et acc�l�ration des joints
    dType.SetPTPCoordinateParams(api, 300, 300, 300, 300)  # Vitesse et acc�l�ration en coordonn�es

	# D�finir les positions X, Y sur une m�me ligne avec Z = -80 mm (au sol)
    positions = [
        (220, -200, -70),  # Emplacement 1
        (220, 0, -70),  # Emplacement 2
        (220, 200, -70),  # Emplacement 3
    ]

    # Boucle sur chaque emplacement
    for index, (x, y, z) in enumerate(positions):
        pos = dType.GetPose(api)
        rHead = pos[3]
        print("D�placement vers l'emplacement ", index + 1, " : X=", x, ", Y=", y, ", Z=", z, "rHead = ", rHead)

        # D�placement vers la position d�finie
        dType.SetPTPCmd(api, 2, float(x), float(y), float(z), 0, isQueued=1)
        time.sleep(2)  # Attendre que le bras se d�place

        # Attendre que le bras atteigne la position
        attendre_position(api, float(x), float(y), float(z))

        # D�placement vers la position d�finie
        dType.SetPTPCmd(api, 2, 200, 0, 20, 0, isQueued=1)

        # Attendre que le bras atteigne la position
        attendre_position(api, 200, 0, 20)

    # Retour au point de d�part (facultatif)
    dType.SetPTPCmd(api, 2, 200, 0, 50, 0, isQueued=1)
    print("Retour au point de d�part.")
    time.sleep(2)

InitPos()
