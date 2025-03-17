def hanoi_iteratif(nb_palets):
    """
    Algorithme itératif pour résoudre le problème des Tours de Hanoï.
    
    Paramètres :
    nb_palets (int) : Nombre total de palets à déplacer.
    
    Retourne :
    list of tuple : Liste des mouvements sous la forme
                    (numéro_du_coup, axe_d'origine, axe_destination, nb_palets_restants_sur_origine, nb_palets_restants_sur_destination)
    """
    mouvements = []  # Liste pour enregistrer les mouvements effectués
    source, auxiliaire, destination = 1, 2, 3  # Définition des axes

    # Si le nombre de palets est pair, on échange les rôles de l'auxiliaire et de la destination
    if nb_palets % 2 == 0:
        auxiliaire, destination = destination, auxiliaire

    # Initialisation des tours :
    # - La tour 1 contient tous les palets, du plus grand (en bas) au plus petit (en haut)
    # - Les tours 2 et 3 sont vides au départ
    tours = {1: list(reversed(range(1, nb_palets + 1))), 2: [], 3: []}

    total_mouvements = (2 ** nb_palets) - 1  # Nombre total de déplacements requis

    # Boucle principale pour effectuer les déplacements
    for coup in range(1, total_mouvements + 1):
        if coup % 3 == 1:
            origine, destination = source, destination
        elif coup % 3 == 2:
            origine, destination = source, auxiliaire
        else:
            origine, destination = auxiliaire, destination

        # Calcul du nombre de palets sur les axes d'origine et destination avant le mouvement
        nb_palets_origine = len(tours[origine])
        nb_palets_destination = len(tours[destination])

        # Vérification avant de déplacer un palet
        if tours[origine] and (not tours[destination] or tours[origine][-1] < tours[destination][-1]):
            palet = tours[origine].pop()
            tours[destination].append(palet)
        elif tours[destination] and (not tours[origine] or tours[destination][-1] < tours[origine][-1]):
            palet = tours[destination].pop()
            tours[origine].append(palet)
            origine, destination = destination, origine  # Correction de l'ordre si nécessaire

        # Enregistrement du mouvement avec les informations supplémentaires
        mouvements.append((coup, origine, destination, nb_palets_origine, nb_palets_destination))

    return mouvements


def afficher_mouvements(mouvements):
    """
    Affiche la séquence des mouvements sous forme de tableau.
    
    Paramètres :
    mouvements (list) : Liste des mouvements sous forme de tuples.
    """
    print("\n=== Mouvements du jeu de Hanoï ===")
    print(f"{'Coup':<6}{'Origine':<8}{'Destination':<12}{'Restants Origine':<18}{'Restants Destination'}")
    print("-" * 60)

    for mouvement in mouvements:
        print(f"{mouvement[0]:<6}{mouvement[1]:<8}{mouvement[2]:<12}{mouvement[3]:<18}{mouvement[4]}")


# Test avec 4 palets
if __name__ == "__main__":
    n_palets = 4  # Modifier ce nombre pour tester avec plus ou moins de palets
    resultat = hanoi_iteratif(n_palets)

    afficher_mouvements(resultat)
