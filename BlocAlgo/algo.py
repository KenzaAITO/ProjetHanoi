def hanoi_iteratif(nb_disques):
    """
    Algorithme itératif pour résoudre le problème des Tours de Hanoï.
    
    Paramètres :
    nb_disques (int) : Nombre total de disques à déplacer.
    
    Retourne :
    list of tuple : Liste des mouvements sous la forme
                    (numéro_du_coup, axe_d'origine, axe_destination, nb_disques_restants_sur_origine)
    """
    mouvements = []  # Liste pour enregistrer les mouvements effectués
    source, auxiliaire, destination = 1, 2, 3  # Définition des axes

    # Si le nombre de disques est pair, on échange les rôles de l'auxiliaire et de la destination
    if nb_disques % 2 == 0:
        auxiliaire, destination = destination, auxiliaire

    # Initialisation des tours :
    # - La tour 1 contient tous les disques, du plus grand (en bas) au plus petit (en haut)
    # - Les tours 2 et 3 sont vides au départ
    tours = {1: list(reversed(range(1, nb_disques + 1))), 2: [], 3: []}

    total_mouvements = (2 ** nb_disques) - 1  # Nombre total de déplacements requis

    # Boucle principale pour effectuer les déplacements
    for coup in range(1, total_mouvements + 1):
        if coup % 3 == 1:
            origine, destination = source, destination
        elif coup % 3 == 2:
            origine, destination = source, auxiliaire
        else:
            origine, destination = auxiliaire, destination

        # Vérification avant de déplacer un disque
        if tours[origine] and (not tours[destination] or tours[origine][-1] < tours[destination][-1]):
            disque = tours[origine].pop()
            tours[destination].append(disque)
        elif tours[destination] and (not tours[origine] or tours[destination][-1] < tours[origine][-1]):
            disque = tours[destination].pop()
            tours[origine].append(disque)
            origine, destination = destination, origine  # Correction de l'ordre si nécessaire

        # Enregistrement du mouvement
        mouvements.append((coup, origine, destination, len(tours[origine])))

    return mouvements


def afficher_mouvements(mouvements):
    """
    Affiche la séquence des mouvements sous forme de tableau.
    
    Paramètres :
    mouvements (list) : Liste des mouvements sous forme de tuples.
    """
    print("\n=== Mouvements du jeu de Hanoï ===")
    print(f"{'Coup':<6}{'Origine':<8}{'Destination':<12}{'Restants'}")
    print("-" * 35)

    for mouvement in mouvements:
        print(f"{mouvement[0]:<6}{mouvement[1]:<8}{mouvement[2]:<12}{mouvement[3]}")


# Test avec 4 disques
if __name__ == "__main__":
    n_disques = 4  # Modifier ce nombre pour tester avec plus ou moins de disques
    resultat = hanoi_iteratif(n_disques)

    afficher_mouvements(resultat)
