#Magician
import time

# Fonction pour attendre que le bras arrive à la position cible
def attendre_position(api, cible_x, cible_y, cible_z, tolerance=1.0):
    while True:
        pose = dType.GetPose(api)
        current_x, current_y, current_z = pose[0], pose[1], pose[2]

        # Vérifier si la position actuelle est proche de la cible avec une tolérance
        if (abs(current_x - cible_x) < tolerance and 
            abs(current_y - cible_y) < tolerance and 
            abs(current_z - cible_z) < tolerance):
            break
        time.sleep(0.1)  # Attendre un peu avant de vérifier à nouveau

#Initialisation des positions
def InitPos():
    # Définir la vitesse et l'accélération des mouvements
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200)  # Vitesse et accélération des joints
    dType.SetPTPCoordinateParams(api, 300, 300, 300, 300)  # Vitesse et accélération en coordonnées

	# Définir les positions X, Y sur une même ligne avec Z = -80 mm (au sol)
    positions = [
        (220, -200, -70),  # Emplacement 1
        (220, 0, -70),  # Emplacement 2
        (220, 200, -70),  # Emplacement 3
    ]

    # Boucle sur chaque emplacement
    for index, (x, y, z) in enumerate(positions):
        pos = dType.GetPose(api)
        rHead = pos[3]
        print("Déplacement vers l'emplacement ", index + 1, " : X=", x, ", Y=", y, ", Z=", z, "rHead = ", rHead)

        # Déplacement vers la position définie
        dType.SetPTPCmd(api, 2, float(x), float(y), float(z), 0, isQueued=1)
        time.sleep(2)  # Attendre que le bras se déplace

        # Attendre que le bras atteigne la position
        attendre_position(api, float(x), float(y), float(z))

        # Déplacement vers la position définie
        dType.SetPTPCmd(api, 2, 200, 0, 20, 0, isQueued=1)

        # Attendre que le bras atteigne la position
        attendre_position(api, 200, 0, 20)

    # Retour au point de départ (facultatif)
    dType.SetPTPCmd(api, 2, 200, 0, 50, 0, isQueued=1)
    print("Retour au point de départ.")
    time.sleep(2)

InitPos()
