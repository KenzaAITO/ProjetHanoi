#Magician
import time
import sys
sys.path.insert(1,'./DLL')
import DobotDllType as dType

# Fonction pour attendre que le bras arrive a la position cible
def attendre_position(api, cible_x, cible_y, cible_z, tolerance=1.0):
    while True:
        pose = dType.GetPose(api)
        current_x, current_y, current_z = pose[0], pose[1], pose[2]

        # Verifier si la position actuelle est proche de la cible avec une tolerance
        if (abs(current_x - cible_x) < tolerance and 
            abs(current_y - cible_y) < tolerance and 
            abs(current_z - cible_z) < tolerance):
            break
        time.sleep(0.1)  # Attendre un peu avant de verifier a nouveau

#Initialisation des positions
def init_pos():
    api = dType.load()  # Charger l'API

    # Definir la vitesse et l'acceleration des mouvements
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200)  # Vitesse et acceleration des joints
    dType.SetPTPCoordinateParams(api, 300, 300, 300, 300)  # Vitesse et acceleration en coordonnees

	# Definir les positions X, Y sur une meme ligne avec Z = -80 mm (au sol)
    positions = [
        (220, -200, -70),  # Emplacement 1
        (220, 0, -70),  # Emplacement 2
        (220, 200, -70),  # Emplacement 3
    ]

    # Boucle sur chaque emplacement
    for index, (x, y, z) in enumerate(positions):
        pos = dType.GetPose(api)
        rhead = pos[3]
        print("Deplacement vers l'emplacement ", index + 1, " : X=", x, ", Y=", y, ", Z=", z, "rhead = ", rhead)

        # Deplacement vers la position definie
        dType.SetPTPCmd(api, 2, float(x), float(y), float(z), 0, isQueued=1)
        time.sleep(2)  # Attendre que le bras se deplace

        # Attendre que le bras atteigne la position
        attendre_position(api, float(x), float(y), float(z))

        # Deplacement vers la position definie
        dType.SetPTPCmd(api, 2, 200, 0, 20, 0, isQueued=1)

        # Attendre que le bras atteigne la position
        attendre_position(api, 200, 0, 20)

    # Retour au point de depart (facultatif)
    dType.SetPTPCmd(api, 2, 200, 0, 50, 0, isQueued=1)
    print("Retour au point de depart.")
    time.sleep(2)

if __name__ == "__main__":
    init_pos()
